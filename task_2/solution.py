import sys
import json
import argparse

from abc import ABC
from os.path import exists
from datetime import datetime

START_OF_NUMERATION = 1


class DatabaseManager:
    def __init__(self, database_filename: str) -> None:
        self._database: dict = {}
        self.database_filename: str = database_filename

        if exists(self.database_filename):
            self.load()
        else:
            self.set_db_default()

    def __del__(self):
        self.save()

    def set_db_default(self):
        self.tasks
        self.done

    def load(self):
        with open(self.database_filename, 'r', encoding='utf8') as db_file:
            try:
                self._database = json.load(db_file)
            except json.decoder.JSONDecodeError as _error:
                print(f'[JSON decoding error]: {_error}')
                self.set_db_default()

    def save(self):
        with open(self.database_filename, 'w', encoding='utf8') as db_file:
            json.dump(self._database, db_file, indent=4)

    @property
    def tasks(self) -> list:
        return self._database.setdefault('tasks', [])

    @property
    def done(self) -> list[dict[str, str]]:
        return self._database.setdefault('done', [])

    def add(self, item: str):
        self.tasks.append(item)

    def remove(self, item_id: int) -> str:
        try:
            task = self.tasks.pop(item_id - START_OF_NUMERATION)
        except IndexError:
            print(f'[IndexError] Task with index {item_id} not exist!')
            sys.exit(1)

        return task

    def set_done(self, item_id: int):
        complete_task = self.remove(item_id)
        date = current_date()

        self.done.append({date: complete_task})


class TaskCommand(ABC):
    def __init__(self, database: DatabaseManager) -> None:
        self._database = database


class AddTasksCommand(TaskCommand):
    def execute(self, tasks: list[str]) -> None:
        for task in tasks:
            self._database.add(task)

        modify_notification(tasks, 'added')


class RemoveTasksCommand(TaskCommand):
    def execute(self, tasks: list[int]) -> None:
        for removed_tasks_num, task_idx in enumerate(tasks, start=0):
            self._database.remove(task_idx - removed_tasks_num)

        modify_notification(tasks, 'removed')


class DoneTasksCommand(TaskCommand):
    def execute(self, tasks: list[int]) -> None:
        for done_tasks_num, task_idx in enumerate(tasks, start=0):
            self._database.set_done(task_idx - done_tasks_num)

        modify_notification(tasks, 'complete')


class ListTasksCommand(TaskCommand):
    def execute(self) -> None:
        tasks = self._database.tasks

        if len(tasks) > 0:
            print('Your tasks:')
            for task_num, task in enumerate(tasks, start=START_OF_NUMERATION):
                print(f'\t [{task_num}]: {task}')
        else:
            print('No Tasks')


class DoneListTasksCommand(TaskCommand):
    def execute(self) -> None:
        tasks = self._database.done

        if len(tasks) > 0:
            print('Your DONE tasks:')
            for task in tasks:
                print(f'\t [*]: {list(task.values())[0]}')
        else:
            print('No DONE Tasks')


class DoneStatisticsTasksCommand(TaskCommand):
    def execute(self) -> None:
        done_tasks = self._database.done
        num_of_done = len(done_tasks)

        if num_of_done > 0:
            last_done = done_tasks[-1]
            print(f'{list(last_done.keys())[0]}: you\'ve completed {num_of_done} tasks! ')

        else:
            print('No DONE Tasks')


def modify_notification(tasks: list, action: str) -> None:
    task_nums = len(tasks)
    print(f'{task_nums} task{"s" if task_nums > 1 else ""} was {action}!')


def current_date() -> str:
    return datetime.today().strftime('%Y.%m.%d')


def main():

    parser = argparse.ArgumentParser(prog='todo',
                                     description='Simple ToDo cli application')
    parser.add_argument('-a', '--add', nargs='+', type=str, help='Adding one or more ToDo tasks. '
                                                                 'Type every task in " "')
    parser.add_argument('-l', '--list', action='store_true', help='Get list of ToDo tasks')
    parser.add_argument('-la', '--all_list', action='store_true', help='Get list of DONE ToDo tasks')
    parser.add_argument('-ld', '--done_list', action='store_true', help='Get list of DONE ToDo tasks')
    parser.add_argument('-ls', '--done_statstic', action='store_true', help='Get statistic of DONE ToDo tasks')

    # for accept only one command, remove or done
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-r', '--remove', nargs='+', type=int, help='Remove one or more ToDo tasks. '
                                                                   'Type id`s of tasks')
    group.add_argument('-d', '--done', nargs='+', type=int, help='Mark one or more ToDo tasks are done. '
                                                                 'Type id of task')
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
    else:

        database = DatabaseManager('todo.json')

        add = args.add
        remove = args.remove
        done = args.done
        is_list = args.list
        is_all_list = args.all_list
        is_done_list = args.done_list
        is_done_stat = args.done_statstic

        if add is not None:
            AddTasksCommand(database).execute(add)

        if remove is not None:
            RemoveTasksCommand(database).execute(remove)

        if done is not None:
            DoneTasksCommand(database).execute(done)

        if is_list is True:
            ListTasksCommand(database).execute()

        if is_all_list is True:
            ListTasksCommand(database).execute()
            DoneListTasksCommand(database).execute()
            DoneStatisticsTasksCommand(database).execute()

        if is_done_list is True:
            DoneListTasksCommand(database).execute()

        if is_done_stat is True:
            DoneStatisticsTasksCommand(database).execute()


if __name__ == '__main__':
    main()
