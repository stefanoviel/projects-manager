import datetime
import pandas as pd
import json
from cgi import print_form
import datetime as dt
import pickle
from datetime import datetime
from project import Project
from settings import Settings


class Calender:

    def __init__(self):
        self.projects = pd.read_csv('projects.csv') 
        self.completed = pd.read_csv('completed.csv')
        self.settings = Settings()
        self.p = Project('', 0)

    def update_projects(self):
        self.projects.to_csv('projects.csv',index=False)
        self.completed.to_csv('completed.csv',index=False)

    def last_day_hour(self): 
        if self.projects.empty: 
            return (dt.date.today() + dt.timedelta(days=1)).strftime("%Y-%m-%d"), 0
        else: 
            return self.projects.iloc[-1].estimated_day, self.projects.iloc[-1].estimated_hour

    def add_new_project(self, df, project: Project):
        last_day, last_hour = self.last_day_hour()

        # if project.hard_deadline_day is None or project.hard_deadline_hour is None: 
        soft_day_deadline, soft_hour_deadline = self.settings.add_hours(project.hours, dt.datetime.strptime(last_day, "%Y-%m-%d"), last_hour)
        hard_day_deadline, hard_hour_deadline = self.settings.add_hours(self.settings.data['extra_time'], dt.datetime.strptime(soft_day_deadline, "%Y-%m-%d"), soft_hour_deadline)

        project.start_date = last_day
        project.start_hour = last_hour
        project.estimated_day = soft_day_deadline
        project.estimated_hour = soft_hour_deadline
        project.hard_deadline_day = hard_day_deadline
        project.hard_deadline_hour = hard_hour_deadline

        self.projects = pd.concat([df, project.to_dataframe()])
        self.update_projects()
        return self.projects

    
    # the gap between the estimated deadline and the actual deadline
    def compute_safe_gap(self):
        days_gap = (sum((pd.to_datetime(self.projects.hard_deadline_day, format="%Y-%m-%d")
                       - pd.to_datetime(self.projects.estimated_day, format="%Y-%m-%d")).dt.days))

        hours_gap = sum(self.projects.hard_deadline_hour - self.projects.estimated_hour)
        return days_gap, hours_gap

    def find_optimal_position(self, project): 
        n_availible_positions = len(self.projects.loc[self.projects.start_date < project.hard_deadline_day])
        df = self.projects.copy()
        print(n_availible_positions)
        for i in range(n_availible_positions): 
            print('ok')
            print(self.insert_row_df(df, project, i))

    def insert_row_df(self, df, project, index): 
        # print(df.iloc[:index], project)
        df2 = self.add_new_project(df.iloc[:index], project)
        print(df2)
        for i in range(index, len(df)):
            print(df2)
            df2 = self.add_new_project(df2, self.p.create_from_datframe(df, i))

        return df2

    def empty_projects(self):
        del self.data['projects'][:]

    def mod_deadline(self, item: Project, deadline: datetime.date):
        print(self.data['projects'])
        elem = self.data['projects'].index(item.toJSON())
        project = json.loads(self.data['projects'][elem])
        project['deadline'] = str(deadline)
        self.data['projects'][elem] = json.dumps(project)


if __name__ == "__main__":
    calender = Calender()
    # p = Project('secondo', 70, hard_deadline_day='2022-12-10', hard_deadline_hour=3)
    p = Project('terzo', 20)
    calender.add_new_project(calender.projects, p)
    p = Project('quarto', 100)
    calender.add_new_project(calender.projects, p)
    p = Project('a', 10)
    calender.add_new_project(calender.projects, p)
    p = Project('b', 80)
    calender.add_new_project(calender.projects, p)
    # calender.find_optimal_position(p)



