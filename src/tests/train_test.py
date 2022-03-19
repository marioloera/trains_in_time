from datetime import date, datetime

from modules.train import Train


class TestTrain:
    data = {
        "departureDate": "2022-01-25",
        "trainNumber": 45,
        "timeTableRows": [
            {
                "type": "DEPARTURE",
                "scheduledTime": "2022-01-25T09:03:00Z",
                "differenceInMinutes": 1,
                "station": {"shortCode": "HKI"},
            },
            {
                "type": "ARRIVAL",
                "scheduledTime": "2022-01-25T10:53:00Z",
                "differenceInMinutes": 0,
                "station": {"shortCode": "TPE"},
            },
        ],
    }
    train = Train(data)

    def test_difference_in_minutes(self):
        assert self.train.no == 45

    def test_departure_date(self):
        assert isinstance(self.train.departure_date, date)
        assert self.train.departure_date == datetime(2022, 1, 25).date()

    def test_valid(self):
        assert self.train.valid

    def test_arrival_and_departure(self):
        assert self.train.arrival.station_code == "TPE"
        assert self.train.daparture.station_code == "HKI"

    def test_process_timetablesd(self):
        new_train = Train(self.data)
        new_train._process_timetables([])
        assert not new_train.valid
