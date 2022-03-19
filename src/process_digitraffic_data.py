import argparse
import json
import logging
import statistics
from datetime import datetime, timedelta
from pathlib import Path

# https://www-digitraffic-fi.translate.goog/rautatieliikenne/?_x_tr_sl=fi&_x_tr_tl=en&_x_tr_hl=fi#junien-tiedot-trains
# https://www.digitraffic.fi/ohjeita/#pakkaus
# [schema here](https://rata.digitraffic.fi/api/v2/graphql/schema.svg)
# [test queries](https://rata.digitraffic.fi/api/v2/graphql/graphiql)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--end_date_str",
        help="start date to fetch data in fomrat YYYY-MM-DD",
        default="2022-03-18",
    )
    parser.add_argument(
        "--max_days_to_fetch",
        help="days to fetch date retrospective from end_date",
        default=30,
    )
    parser.add_argument(
        "--datafile_path",
        help="file to store the data",
        default="digitraffic_data/trainsByDepartureDates/",
    )
    args = parser.parse_args()
    logging.info(args)
    data = fetch_data_from_files(args.datafile_path)
    end_date = datetime.strptime(args.end_date_str, "%Y-%m-%d").date()
    process_trains_by_departure_date(data, end_date, int(args.max_days_to_fetch))
    logging.info("process completed!")


class Train:
    def __init__(self, data) -> None:
        self.departure_date = datetime.strptime(data["departureDate"], "%Y-%m-%d").date()
        self.no = data["trainNumber"]
        self._process_timetables(data["timeTableRows"])

    def _process_timetables(self, timetables):
        self.valid = False
        if len(timetables) != 2:
            return

        timetable0 = Timetable(timetables[0])
        timetable1 = Timetable(timetables[1])

        if timetable0.type == "DEPARTURE" and timetable1.type == "ARRIVAL":
            self.valid = True
            self.daparture = timetable0
            self.arrival = timetable1
        elif timetable1.type == "DEPARTURE" and timetable0.type == "ARRIVAL":
            self.valid = True
            self.daparture = timetable1
            self.arrival = timetable0

    def __str__(self):
        msg = (
            f"Train no.{self.no} {self.daparture.station_code} -> {self.arrival.station_code} "
            f"at {self.daparture.scheduled_time}"
        )
        return msg


class Timetable:
    def __init__(self, timetable):
        self.type = timetable.get("type")
        self.station_code = timetable.get("station", {}).get("shortCode")
        self.difference_in_minutes = timetable.get("differenceInMinutes")
        self.scheduled_time = timetable.get("scheduledTime")


def process_trains_by_departure_date(data, end_date, max_days_to_fetch):
    delays_min = []
    for date in data:
        for record in date:
            train = Train(record)
            if not train.valid:
                continue
            if not 0 <= (end_date - train.departure_date).days <= max_days_to_fetch:
                continue
            logging.info(train)
            delays_min.append(train.arrival.difference_in_minutes)

    avg_delay_min = statistics.mean(delays_min)
    logging.info(f"avg_delay_min: {avg_delay_min}")

    # estimated arrival time
    scheduled_datetime = datetime.strptime(train.arrival.scheduled_time, "%Y-%m-%dT%H:%M:%SZ")
    estimated_arrival_time = scheduled_datetime + timedelta(minutes=avg_delay_min)
    result = f'Tampere Estimated Arrival Time: {estimated_arrival_time.strftime("%H:%M:%S")}'
    logging.info(result)


def fetch_data_from_files(datafile_path):
    files = Path(datafile_path).glob("*.json")
    data = []
    for file in files:
        with open(file) as f:
            data.append(json.load(f))
    return data


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
    )
    logging.info("process data started!")
    main()
