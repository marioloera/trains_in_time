import json

from modules.digitraffic_utils import DigiTraffic


class TestFetchDigitrafficData:
    def test_make_request_basic_status_code(self):
        query = json.dumps("{currentlyRunningTrains{trainNumber}}")
        request_data = f'{{"query":{query}}}'
        response = DigiTraffic.make_request(request_data)
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json()["data"] is not None

    def test_get_request_data_from_file(self):
        query = """
        {
            trainsByDepartureDate(
                departureDate:"2022-03-16",
                where:{
                    trainNumber:{lessThan:5}
                }
            ){
                trainNumber
            }
        }
        """
        filename = "/tmp/test_get_request_data_from_file_query.txt"
        with open(filename, "w") as f:
            f.write(query)

        request_data = DigiTraffic.get_request_data_from_file(filename)
        response = DigiTraffic.make_request(request_data)
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json()["data"] is not None

    def test_process_response(self):
        query = """
        {trainsByDepartureDate(
            departureDate:"2022-03-16",
            where:{trainNumber:{lessThan:3}}
        ){trainNumber}}
        """
        expected_results = [
            {"trainNumber": 1},
            {"trainNumber": 2},
        ]
        parsed_query = json.dumps(query)
        request_data = f'{{"query":{parsed_query}}}'
        response = DigiTraffic.make_request(request_data)
        results = DigiTraffic.process_response(response)
        assert results == expected_results

    def test_get_data_per_date(self):
        target_date = "2022-01-01"
        results = DigiTraffic().get_data_per_date(target_date)
        assert results[0]["departureDate"] == target_date

    def test_get_all_trains_per_date(self):
        target_date = "2022-02-02"
        results = DigiTraffic().get_all_trains_per_date(target_date)
        assert results[0]["departureDate"] == target_date
        assert len(results) > 1
