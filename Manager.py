import datetime
import json
from cgi import print_form
import pickle
from datetime import datetime
from Project import Project
from Settings import Settings


class Manager:

    def __init__(self):
        self.settings = Settings()
        with open("projects.json", "r") as infile:
            self.data = json.load(infile)

    def update_projects(self):
        with open('projects.json', 'w') as outfile:
            print(self.data)
            json.dump(self.data, outfile, indent=4)

    def add_element(self, item: Project):
        if item.deadline is None:
            self.data = self.settings.new_deadline(self.data, 14)
            self.data['projects'].append(item.toJSON())
            print(self.data['last_day'])
            print(self.data['last_hour'])

        self.update_projects()

    def empty_projects(self):
        del self.data['projects'][:]

    def mod_deadline(self, item: Project, deadline: datetime.date):
        print(self.data['projects'])
        elem = self.data['projects'].index(item.toJSON())
        project = json.loads(self.data['projects'][elem])
        project['deadline'] = str(deadline)
        self.data['projects'][elem] = json.dumps(project)


if __name__ == "__main__":
    p = Project('primo', 33)
    p1 = Project('secondo', 31)
    m = Manager()
    # print(m.data['projects'][0])
    m.empty_projects()
    m.add_element(p)

    # m.add_element(p1)
    # m.add_elem_deadline(p1, datetime.date(2022, 12, 20))
    # print(m.projects[0].deadline)


# TODO
# add project with a deadline
# compute real deadline (with safety offset) for each project
# get the to do list of projects