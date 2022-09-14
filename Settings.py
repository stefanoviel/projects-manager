from datetime import datetime
import datetime as dt
import json


class Settings:

    def __init__(self):
        self.real_hours = {}
        with open('settings.json', 'r') as f:
            self.data = json.load(f)
        self.computer_hours()
        print(self.real_hours)

    def computer_hours(self):
        for i in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            self.real_hours[i] = self.data['working_days'][i] - self.data['school_days'][i]

    def update_json(self):
        self.computer_hours()
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

    def new_deadline(self, data, hours: int):
        date = datetime.strptime(data['last_day'], '%Y-%m-%d')
        weekday = date.strftime('%A')
        last_hour = data['last_hour']
        if self.real_hours[weekday] < last_hour:
            raise Exception("Hours used exceed the available ones")

        while hours > 0:
            if hours >= (self.real_hours[weekday] - last_hour):
                # print(hours, self.real_hours[weekday], last_hour)
                hours -= (self.real_hours[weekday] - last_hour)
                date += dt.timedelta(days=1)
                weekday = date.strftime('%A')
                last_hour = 0
            else:
                last_hour = self.real_hours[weekday] - hours
                hours = 0

        data['last_day'] = date.strftime('%Y-%m-%d')
        data['last_hour'] = last_hour

        return data


if __name__ == '__main__':
    s = Settings()

