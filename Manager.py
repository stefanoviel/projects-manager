import pickle
from Project import Project

class Manager:

    def __init__(self):
        with open("projects.pickle", "rb") as infile:
            self.projects = pickle.load(infile)

    def update_projects(self):
        with open('projects.pickle', 'wb') as outfile:
            pickle.dump(lista, infile)

    def add_element(self, item: Project):
        self.projects.append(item)
        self.update_projects()

    def add_elem_deadline(self, item):
        o



if __name__ == "__main__":
    with open("projects.pickle", "wb") as infile:
        lista = []
        pickle.dump(lista, infile)
