from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DATE, Integer
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

weekdays = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday",
}

engine = create_engine("sqlite:///todo.db?check_same_thread=False")

Base = declarative_base()


class Table(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True, autoincrement=True)
    task = Column(String)
    deadline = Column(DATE, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)


def main():
    Session = sessionmaker(bind=engine)
    session = Session()
    while True:
        choice = int(input("1) Today's tasks\n2) Week's tasks\n3) All tasks\n"
                           "4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit\n"))
        if choice == 1:  # Today's tasks
            today = datetime.today().date()
            rows = session.query(Table).filter(Table.deadline == today).all()
            print("Today's tasks")
            if len(rows) == 0:
                print("Nothing to do!")
            else:
                for i in range(len(rows)):
                    print(f"{i + 1}. {rows[i].task}")

        elif choice == 2:  # seven days tasks
            for i in range(7):
                today = datetime.today().date() + timedelta(days=i)
                rows = session.query(Table).filter(Table.deadline == today).all()
                print(weekdays[today.weekday()], today.day, today.strftime("%b") + ":")
                if len(rows) == 0:
                    print("Nothing to do!\n")
                else:
                    for j in range(len(rows)):
                        print(f"{j + 1}. {rows[j].task}\n")

        elif choice == 3:
            rows = session.query(Table).order_by(Table.deadline).all()
            print("All tasks:")
            if len(rows) == 0:
                print("Nothing to do!")
            else:
                for j in range(len(rows)):
                    today = rows[j].deadline
                    print(f"{j + 1}. {rows[j].task}. {today.day} {today.strftime('%b')}")

        elif choice == 4:  # for missed tasks
            rows = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
            print("Missed tasks:")
            if len(rows) == 0:
                print("Nothing is missed!")
            else:
                for i in range(len(rows)):
                    print(f"{i + 1}. {rows[i].task}. {rows[i].deadline.day} {rows[i].deadline.strftime('%b')}")
                print()

        elif choice == 5:  # for adding tasks
            task = input("Enter task")
            deadline = input('Enter deadline')
            deadline = datetime.strptime(deadline, "%Y-%m-%d")
            new_row = Table(task=task, deadline=deadline)
            session.add(new_row)
            session.commit()
            print("The task has been added!")

        elif choice == 6:  # for deleting tasks
            rows = session.query(Table).all()
            print("Choose the number of the task you want to delete:")
            if len(rows) == 0:
                print("Nothing to delete!")
            else:
                for i in range(len(rows)):
                    print(f"{i + 1}. {rows[i].task}. {rows[i].deadline.day} {rows[i].deadline.strftime('%b')}")
                delete = int(input())
                session.delete(rows[delete - 1])
                print("The task has been deleted!")
            session.commit()

        elif choice == 0:
            print("Bye!")
            exit(0)


if __name__ == '__main__':
    main()
