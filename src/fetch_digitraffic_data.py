import argparse
import json
import logging
import time
from datetime import datetime, timedelta

import requests

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
    QUERYFILENAME = "queries/trainsByDepartureDate.txt"
    HARDCORE_DATE = "2022-03-16"
    REQUEST_DATA = get_request_data_from_file(QUERYFILENAME)
    END_DATE = datetime.strptime(end_date_str, "%Y-%m-%d").date()

    for i in range(days_to_fetch):
        target_date = END_DATE - timedelta(days=i)
        logging.info(f"making request for date: {target_date}")
        request_data = REQUEST_DATA.replace(HARDCORE_DATE, str(target_date))
        response = make_request(request_data)
        results = process_response(response)
        save_to_file(results, f"{datafile_path}_{target_date}.json")
        time.sleep(1)  # to avoid to many reques, Too many requests. Only 60 requests per minute per ip per url


def get_request_data_from_file(query_file):
    with open(query_file, mode="r") as f:
        query = json.dumps(f.read())
        body = f'{{"query":{query}}}'
        return body


def save_to_file(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def make_request(data):
    url = "https://rata.digitraffic.fi/api/v2/graphql/graphql"
    headers = {
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip",
    }
    return requests.post(url, data=data, headers=headers)


def process_response(response):
    try:
        response_dict = response.json()
        if response.status_code != 200:
            msg = "invalid status code for processng {response.status_code}"
            logging.warning(msg)
            return

    except Exception as e:
        logging.error(e)
        logging.error(response)
        return

    data = response_dict.get("data")
    if data is None:
        logging.warning("no data in response")
        logging.warning(response_dict)
        return

    results = data.get("trainsByDepartureDate")
    if results is None:
        logging.warning("no trainsByDepartureDate in data")
        logging.warning(data)
        return

    return results


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
    )
    logging.info("fetch data started!")
    main()
