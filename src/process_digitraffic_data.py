import argparse
import json
import logging
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
        "--days_to_fetch",
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
    process_trains_by_departure_date(data, int(args.days_to_fetch))
    logging.info("process completed!")


def process_trains_by_departure_date(data, days_to_fetch):
    for record in data:
        print(record[0]["departureDate"])


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
