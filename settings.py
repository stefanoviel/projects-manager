from datetime import datetime
import datetime as dt
import pandas as pd
import json


class Settings:

    def __init__(self):
        self.real_hours = {}
        with open('settings.json', 'r') as f:
            self.data = json.load(f)
        self.compute_availible_hours()
        # print(self.real_hours)

    # availible hours to work are computed by the total working hours each day - hours of school each day
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
            # print(self.real_hours[weekday], hours, start_hour)
            if hours >= (self.real_hours[weekday] - start_hour):
                # print(hours, self.real_hours[weekday], last_hour)
                hours -= (self.real_hours[weekday] - start_hour)
                start_day += dt.timedelta(days=1)
                weekday = start_day.strftime('%A')
                start_hour = 0
            else:
                start_hour = hours
                hours = 0

        # print(start_day.strftime("%Y-%m-%d"), start_hour)
        return start_day.strftime("%Y-%m-%d"), start_hour

    def compute_remaining_hour_work(self, df : pd.DataFrame): 
        remaining_hours = 0
        for index, row in df.iterrows():
            weekday = datetime.strptime(row.estimated_day, "%Y-%m-%d").strftime('%A')
            remaining_hours += self.real_hours[weekday] - row.estimated_hour
            
        return remaining_hours

    def compute_hours_between_days(self, day1:datetime, day2:datetime):  
        hours = 0
        while day1 < day2: 
            weekday = day1.strftime('%A')
            hours += self.real_hours[weekday] 
            day1 += dt.timedelta(days=1)

        return hours
        


if __name__ == '__main__':
    s = Settings()

    print(s.compute_hours_between_days(datetime.strptime("2022-12-01", "%Y-%m-%d"), datetime.strptime("2022-12-8", "%Y-%m-%d")))

