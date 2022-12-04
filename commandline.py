from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import prompt
from prompt_toolkit import PromptSession
from prompt_toolkit import print_formatted_text, HTML
import pandas as pd
from calendar_manager import Calendar
import json
from project import Project

class Commands: 

    def __init__(self): 
        f = open('commands.json')
        self.commands_list = json.load(f)
        self.calendar = Calendar()

    def update_commands_list(self): 
        json_object = json.dumps(self.commands_list, indent=4)
 
        with open("commands.json", "w") as outfile:
            outfile.write(json_object)

    def add_command(self,name,n_parameters,help,function_name): 
        if name in self.commands_list: 
            print('ATTENTION: command', name, 'is being overriden')
        self.commands_list[name] = {'n_parameters':n_parameters, 'help':help, 'function_name':function_name}
        self.update_commands_list()


    def execute(self, command_name, *args): 
        if command_name in self.commands_list: 
            command = 'self.' + self.commands_list[command_name]['function_name'] + '('
            for arg in args: 
                command += arg + ','
            
            
        else: 
            print("Sorry! This commands doesn't exist")
        
    def loop(self): 
        pass

    
    def cmd_add_project(self, name: str, hours: int, hard_deadline_day=None): 
        project = Project(name, hours, hard_deadline_day=hard_deadline_day)
        self.calendar.add_new_project(self.calendar.projects, project, True)


if __name__ == '__main__':
    c = Commands()
    # c.add_command('add_project', 3, 'add_project [number of hours] [optional day deadline, format YYYY-MM-DD]', 'cmd_add_project')
    c.execute('add_project')

    