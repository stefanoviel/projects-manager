import datetime
import uuid


class Project:

    def __init__(self, name: str, hours: float, deadline=None) -> None:
        self.id = uuid.uuid4()
        self.name = name
        self.hours = hours
        self.deadline = deadline

    def add_hours(self, more_hours: float) -> None:
        self.hours += more_hours

    def change_deadline(self, deadline : datetime.date):
        if deadline < datetime.date.today():
            raise ValueError("Deadline must be later than today")

        self.deadline = deadline


if __name__ == "__main__":
    p = Project("primo", 33)
    p.change_deadline(datetime.date(2033, 10, 2))
    print(p.deadline)