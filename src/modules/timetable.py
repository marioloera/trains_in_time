from datetime import datetime


class Timetable:
    def __init__(self, timetable):
        self.type = timetable.get("type")
        self.station_code = timetable.get("station", {}).get("shortCode")
        self.difference_in_minutes = timetable.get("differenceInMinutes")
        self.scheduled_time = datetime.strptime(timetable.get("scheduledTime"), "%Y-%m-%dT%H:%M:%SZ")
