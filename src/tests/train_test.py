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

    def test_departure_and_arrival(self):
        data = {
            "departureDate": "2022-01-25",
            "timeTableRows": [
                {
                    "type": "ARRIVAL",
                    "scheduledTime": "2022-01-25T09:03:00Z",
                    "station": {"shortCode": "HKI"},
                },
                {
                    "type": "DEPARTURE",
                    "scheduledTime": "2022-01-25T10:53:00Z",
                    "station": {"shortCode": "TPE"},
                },
            ],
        }
        new_train = Train(data)
        assert new_train.arrival.station_code == "HKI"
        assert new_train.daparture.station_code == "TPE"

    def test_process_timetables_empty(self):
        self.train._process_timetables([])
        assert not self.train.valid

    def test_process_timetables_not_list(self):
        assert self.train._process_timetables("") is None

    def test_estimate_arrival_time(self):
        delay_min = 3
        estimated_arrival_time = self.train.estimate_arrival_time(datetime(2022, 1, 25), delay_min)
        assert isinstance(estimated_arrival_time, datetime)
        assert estimated_arrival_time == datetime(2022, 1, 25, 10, 53 + delay_min)

    def test__str__(self):
        print(self.train)
