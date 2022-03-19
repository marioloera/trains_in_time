from datetime import datetime

from modules.timetable import Timetable


class TestTimetable:
    data = {
        "type": "ARRIVAL",
        "scheduledTime": "2022-01-24T10:53:00Z",
        "differenceInMinutes": 13,
        "station": {"shortCode": "TPE"},
    }
    t = Timetable(data)

    def test_type(self):
        assert self.t.type == "ARRIVAL"

    def test_station_code(self):
        assert self.t.station_code == "TPE"

    def test_difference_in_minutes(self):
        assert self.t.difference_in_minutes == 13

    def test_scheduled_time(self):
        assert isinstance(self.t.scheduled_time, datetime)
        assert self.t.scheduled_time == datetime(2022, 1, 24, 10, 53)
