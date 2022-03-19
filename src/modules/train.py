from datetime import datetime

from modules.timetable import Timetable


class Train:
    def __init__(self, data) -> None:
        self.departure_date = datetime.strptime(data["departureDate"], "%Y-%m-%d").date()
        self.no = data["trainNumber"]
        self._process_timetables(data["timeTableRows"])

    def _process_timetables(self, timetables):
        self.valid = False
        if len(timetables) != 2:
            return

        timetable0 = Timetable(timetables[0])
        timetable1 = Timetable(timetables[1])

        if timetable0.type == "DEPARTURE" and timetable1.type == "ARRIVAL":
            self.valid = True
            self.daparture = timetable0
            self.arrival = timetable1
        elif timetable1.type == "DEPARTURE" and timetable0.type == "ARRIVAL":
            self.valid = True
            self.daparture = timetable1
            self.arrival = timetable0

    def __str__(self):
        msg = (
            f"Train no.{self.no} {self.daparture.station_code} -> {self.arrival.station_code} "
            f"at {self.daparture.scheduled_time}"
        )
        return msg
