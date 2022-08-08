import datetime
import json


class Setting:

    def __init__(self):
        with open('settings.json', 'r') as f:
            self.data = json.load(f)

    def update_json(self):
        with open('settings.json', 'w') as f:
            json.dump(self.data, f, indent=4)

    def set_working_hours(self, day: str, hours: int):
        self.data['working_days'][day] = hours
        self.update_json()

    def set_school_hourse(self, day: str, hours: int):
        self.data['school_days'][day] = hours
        self.update_json()

    def set_holliday(self, date: datetime.datetime) -> object:
        self.data['hollidays'].append(date)
        self.update_json()



if __name__ == '__main__':
    s = Setting()
    s.set_holliday(datetime.date(2022, 12, 25))
