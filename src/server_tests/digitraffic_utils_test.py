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
