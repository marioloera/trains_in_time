import argparse
import json
import logging
import statistics
from datetime import datetime
from pathlib import Path

from modules.digitraffic_utils import DigiTraffic
from modules.train import Train

# https://www-digitraffic-fi.translate.goog/rautatieliikenne/?_x_tr_sl=fi&_x_tr_tl=en&_x_tr_hl=fi#junien-tiedot-trains
# https://www.digitraffic.fi/ohjeita/#pakkaus
# [schema here](https://rata.digitraffic.fi/api/v2/graphql/schema.svg)
# [test queries](https://rata.digitraffic.fi/api/v2/graphql/graphiql)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--target_date",
        help="target date to predict arrival time",
        default="2022-03-23",
    )
    parser.add_argument(
        "--end_date_str",
        help="start date to fetch data in fomrat YYYY-MM-DD to predict arrival time",
        default="2022-03-18",
    )
    parser.add_argument(
        "--max_days_to_fetch",
        help="days to fetch date retrospective from end_date to predict arrival time",
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
    target_date = datetime.strptime(args.target_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(args.end_date_str, "%Y-%m-%d").date()
    max_days_to_fetch = int(args.max_days_to_fetch)
    process_trains_by_departure_date(data, end_date, max_days_to_fetch, target_date)
    logging.info("process completed!")


def process_trains_by_departure_date(data, end_date, max_days_to_fetch, target_date):
    delays_min = []
    no_data = True
    for date in data:
        for record in date:
            train = Train(record)
            if not train.valid:
                continue
            if not 0 <= (end_date - train.departure_date).days <= max_days_to_fetch:
                continue
            no_data = False
            delays_min.append(train.arrival.difference_in_minutes)

    if no_data:
        logging.warning("no data was found")
        return

    avg_delay_min = statistics.mean(delays_min)
    logging.info(f"avg_delay_min: {avg_delay_min}")

    # estimated arrival time
    estimated_arrival_time = train.estimate_arrival_time(target_date, avg_delay_min, 2)
    result = (
        f"Train no {train.no}, {train.arrival.station_code} Station Estimated Arrival Time: {estimated_arrival_time}"
    )
    logging.info(result)

    earlier_train = find_earlier_train(target_date, train.arrival.scheduled_time)
    logging.info(f"Earlier train: {earlier_train}")


def fetch_data_from_files(datafile_path):
    files = Path(datafile_path).glob("*.json")
    data = []
    for file in files:
        with open(file) as f:
            data.append(json.load(f))
    return data


def find_earlier_train(target_date, arrival_time):
    new_time = arrival_time.replace(year=target_date.year, month=target_date.month, day=target_date.day)
    earlier_trains = {}
    records = DigiTraffic().fetch_all_trains_per_date(str(target_date))
    for record in records:
        train = Train(record)
        if not train.valid:
            continue
        if train.arrival.scheduled_time >= new_time:
            continue
        earlier_trains[train.arrival.scheduled_time] = train

    for key in sorted(earlier_trains, reverse=True):
        return earlier_trains[key]


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
    )
    logging.info("process data started!")
    main()
