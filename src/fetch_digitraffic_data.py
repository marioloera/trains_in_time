import argparse
import json
import logging
import time
from datetime import datetime, timedelta

from modules.digitraffic_utils import DigiTraffic

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
        default="digitraffic_data/trainsByDepartureDates/results",
    )
    args = parser.parse_args()
    logging.info(args)
    fetch_data(args.end_date_str, int(args.days_to_fetch), args.datafile_path)
    logging.info("fetching completed!")


def fetch_data(end_date_str, days_to_fetch, datafile_path):
    END_DATE = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    digi_traffic = DigiTraffic()
    for i in range(days_to_fetch):
        target_date = END_DATE - timedelta(days=i)
        logging.info(f"making request for date: {target_date}")
        results = digi_traffic.get_data_per_date(str(target_date))
        save_to_file(results, f"{datafile_path}_{target_date}.json")
        time.sleep(1)  # to avoid to many reques, Too many requests. Only 60 requests per minute per ip per url


def save_to_file(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
    )
    logging.info("fetch data started!")
    main()
