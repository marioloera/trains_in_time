import json
import logging

import requests


class DigiTraffic:
    QUERYFILENAME = "queries/trainsByDepartureDate.txt"

    @staticmethod
    def get_request_data_from_file(query_file=QUERYFILENAME):
        with open(query_file, mode="r") as f:
            query = json.dumps(f.read())
            body = f'{{"query":{query}}}'
            return body

    @staticmethod
    def make_request(data):
        url = "https://rata.digitraffic.fi/api/v2/graphql/graphql"
        headers = {
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip",
        }
        return requests.post(url, data=data, headers=headers)

    @staticmethod
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
