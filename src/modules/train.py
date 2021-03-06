from datetime import datetime, timedelta, timezone

from modules.timetable import Timetable


class Train:
    TZ_EET = timezone(timedelta(hours=+2), "EET")

    def __init__(self, data) -> None:
        self.departure_date = datetime.strptime(data.get("departureDate"), "%Y-%m-%d").date()
        self.no = data.get("trainNumber")
        self._process_timetables(data.get("timeTableRows"))

    @staticmethod
    def utc_to_timezone(utc_dt, target_timezone):
        return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=target_timezone)

    @staticmethod
    def FinnishTime(utc_dt):
        return Train.utc_to_timezone(utc_dt, Train.TZ_EET)

    def _process_timetables(self, timetables):
        self.valid = False
        if not isinstance(timetables, list):
            return

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

    def estimate_arrival_time(self, target_date, diff_min):
        new_time = self.arrival.scheduled_time.replace(
            year=target_date.year, month=target_date.month, day=target_date.day
        )
        return new_time + timedelta(minutes=diff_min)

    def __str__(self):
        msg = (
            f"Train no {self.no} {self.daparture.station_code}: {Train.FinnishTime(self.daparture.scheduled_time)} "
            f"-> {self.arrival.station_code}: {Train.FinnishTime(self.arrival.scheduled_time)}"
        )
        return msg
