import json
import pandas as pd
import datetime
import uuid


class Project:

    def __init__(self, name: str, hours: int, hours_used = None , start_hour = None , start_date =None, hard_deadline_day=None, hard_deadline_hour=None) -> None:
        self.id = str(uuid.uuid4())
        self.name = name
        self.hours = hours
        self.hours_used = 0
        self.start_date = start_date
        self.start_hour = start_hour
        self.hard_deadline_day = hard_deadline_day
        self.hard_deadline_hour = hard_deadline_hour
        self.estimated_day = None
        self.estimated_hour = None

    @classmethod
    def create_from_datframe(cls, df: pd.DataFrame, index:int): 
        # print('passed df\n', df.name.iloc[index], df.hours.iloc[index], df.hours_used.iloc[index])
        return cls(df.name.iloc[index], df.hours.iloc[index], hours_used=df.hours_used.iloc[index], hard_deadline_day=df.hard_deadline_day.iloc[index], hard_deadline_hour=df.hard_deadline_hour.iloc[index])

    def to_dataframe(self): 
        l = [self.id, self.name, self.hours, self.hours_used, self.start_date, self.start_hour,  self.hard_deadline_day, self.hard_deadline_hour, self.estimated_day, self.estimated_hour]
        return pd.DataFrame([l], columns=["id","name","hours","hours_used","start_date","start_hour","hard_deadline_day","hard_deadline_hour","estimated_day","estimated_hour"])

        
    def add_hours(self, more_hours: float) -> None:
        self.hours += more_hours

    def change_deadline(self, deadline: datetime.date):
        if deadline < datetime.date.today():
            raise ValueError("Deadline must after today")

        self.deadline = deadline




if __name__ == "__main__":
    p = Project("primo", 33)
    # p.change_deadline(datetime.date(2033, 10, 2))
    print(p.toJSON())
