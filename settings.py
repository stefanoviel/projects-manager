from datetime import datetime
import datetime as dt
import json


class Settings:

    def __init__(self):
        self.real_hours = {}
        with open('settings.json', 'r') as f:
            self.data = json.load(f)
        self.compute_availible_hours()
        # print(self.real_hours)

    def compute_availible_hours(self):
        for i in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            self.real_hours[i] = self.data['working_days'][i] - self.data['school_days'][i]

    def update_json(self):
        # self.compute_availible_hours()  # why should I compute it if I'm not saving it?
        with open('settings.json', 'w') as f:
            json.dump(self.data, f, indent=4)

    def set_working_hours(self, day: str, hours: int):
        self.data['working_days'][day] = hours
        self.update_json()

    def set_school_hourse(self, day: str, hours: int):
        self.data['school_days'][day] = hours
        self.update_json()

    def set_holliday(self, date: datetime) -> object:
        self.data['hollidays'].append(date)
        self.update_json()

    def add_hours(self, hours:int, start_day:datetime, start_hour:int): 
        weekday = start_day.strftime('%A') 

        while hours > 0:
            if hours >= (self.real_hours[weekday] - start_hour):
                # print(hours, self.real_hours[weekday], last_hour)
                hours -= (self.real_hours[weekday] - start_hour)
                start_day += dt.timedelta(days=1)
                weekday = start_day.strftime('%A')
                start_hour = 0
            else:
                start_hour = self.real_hours[weekday] - hours
                hours = 0

        return start_day.strftime("%Y-%m-%d"), start_hour

if __name__ == '__main__':
    s = Settings()

