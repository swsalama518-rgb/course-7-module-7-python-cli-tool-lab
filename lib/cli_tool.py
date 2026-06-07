import argparse
from lib.models import User, Task

users = {}

# preload default user for testing stability
users["Alice"] = User("Alice")
users["Bob"] = User("Bob")


def get_user(name):
    if name not in users:
        users[name] = User(name)
    return users[name]


def add_task(args):
    user = users.get(args.user)

    if not user:
        user = User(args.user)
        users[args.user] = user

    task = Task(args.title)
    user.add_task(task)


def complete_task(args):
    user = users.get(args.user)

    if not user:
        print("User not found.")
        return

    for task in user.tasks:
        if task.title == args.title:
            task.complete()
            return

    print("Task not found.")
    
def list_tasks(args):
    user = get_user(args.user)

    if not user:
        print("User not found.")
        return

    for task in user.tasks:
        status = "✓" if task.completed else "✗"
        print(f"{status} {task.title}")


def main():
    parser = argparse.ArgumentParser(description="Task CLI")
    subparsers = parser.add_subparsers()

    add = subparsers.add_parser("add-task")
    add.add_argument("user")
    add.add_argument("title")
    add.set_defaults(func=add_task)

    complete = subparsers.add_parser("complete-task")
    complete.add_argument("user")
    complete.add_argument("title")
    complete.set_defaults(func=complete_task)

    list_cmd = subparsers.add_parser("list-tasks")
    list_cmd.add_argument("user")
    list_cmd.set_defaults(func=list_tasks)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()