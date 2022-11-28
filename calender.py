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

    def last_day_hour(self, df: pd.DataFrame): 
        if df.empty: 
            return (dt.date.today() + dt.timedelta(days=1)).strftime("%Y-%m-%d"), 0
        else: 
            return df.iloc[-1].estimated_day, df.iloc[-1].estimated_hour

    def add_new_project(self, df, project: Project, save:bool):
        last_day, last_hour = self.last_day_hour(df)

        soft_day_deadline, soft_hour_deadline = self.settings.add_hours(project.hours, dt.datetime.strptime(last_day, "%Y-%m-%d"), last_hour)
        project.start_date = last_day
        project.start_hour = last_hour
        project.estimated_day = soft_day_deadline
        project.estimated_hour = soft_hour_deadline

        if project.hard_deadline_day is None or project.hard_deadline_hour is None: 
            hard_day_deadline, hard_hour_deadline = self.settings.add_hours(self.settings.data['extra_time'], dt.datetime.strptime(soft_day_deadline, "%Y-%m-%d"), soft_hour_deadline)
            project.hard_deadline_day = hard_day_deadline
            project.hard_deadline_hour = hard_hour_deadline

        if project.hard_deadline_day < project.estimated_day or (project.hard_deadline_day == project.estimated_day and project.hard_deadline_hour < project.estimated_hour): 
            return None

        df = pd.concat([df, project.to_dataframe()])
        if save: 
            self.projects = df
            self.update_projects()
        return df
    
    # the gap between the estimated deadline and the actual deadline
    def compute_safe_gap(self, df:pd.DataFrame):
        
        hours_gap = 0
        for index, row in df.iterrows():
            hours_gap += self.settings.compute_hours_between_days(datetime.strptime(row.estimated_day, "%Y-%m-%d") + dt.timedelta(days=1), datetime.strptime(row.hard_deadline_day, "%Y-%m-%d"))

        hours_gap += sum(df.hard_deadline_hour) + self.settings.compute_remaining_hour_work(df)
        return hours_gap

    # try all position in the list of projects and return the one that reduces the safe_gap
    def find_optimal_position(self, project): 
        n_availible_positions = len(self.projects.loc[self.projects.start_date < project.hard_deadline_day]) 
        df = self.projects.copy()

        max_gap = 0
        ret_df = None
        for i in range(n_availible_positions): 
            new_df = self.insert_row_df(df, project, i)
            if new_df is not None: 
                gap =  self.compute_safe_gap(new_df)
                if max_gap < gap: 
                    max_gap = gap
                    ret_df = new_df

        return ret_df
            

    # insert row in projects dataframe
    def insert_row_df(self, df, project, index): 
        df2 = self.add_new_project(df.iloc[:index], project, False)
        for i in range(index, len(df)):
            if df2 is None: 
                return None
            df2 = self.add_new_project(df2, self.p.create_from_datframe(df, i), False)
        return df2


    def recompute_deadline_setting_changed(): 
        pass

    

if __name__ == "__main__":
    calender = Calender()
    p = Project('secondo', 23, hard_deadline_day='2022-12-20', hard_deadline_hour=3)
    print(calender.find_optimal_position(p))

    # p = Project('a', 10)
    # calender.add_new_project(calender.projects, p, True)
    # p = Project('c', 20)
    # calender.add_new_project(calender.projects, p, True)
    # p = Project('d', 30)
    # calender.add_new_project(calender.projects, p, True)
    # p = Project('b', 80)
    # calender.add_new_project(calender.projects, p, True) 
    # p = Project('terzo', 20)
    # calender.add_new_project(calender.projects, p, True)  
    # p = Project('quarto', 100)
    # calender.add_new_project(calender.projects, p, True)
 