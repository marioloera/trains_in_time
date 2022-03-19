import json

import requests


class DigiTraffic:
    @staticmethod
    def get_request_data_from_file(query_file):
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
