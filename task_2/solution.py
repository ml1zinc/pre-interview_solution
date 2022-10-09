import sys
import json
import argparse

from os.path import exists


class DatabaseManager:
    def __init__(self, database_filename: str) -> None:
        self._database = {}
        self.database_filename: str = database_filename

        if exists(self.database_filename):
            self.load()
        else:
            self._database = {'tasks': [],
                              'done': {}
                              }

    def __del__(self):
        self.save()

    def load(self):
        pass

    def save(self):
        pass

    def get_todo(self) -> list:
        pass

    def add(self, item: str):
        pass

    def remove(self, item_id: int):
        pass

    def set_done(self, item_id: int):
        pass

    def get_done(self):
        pass



def main():

    parser = argparse.ArgumentParser(prog='todo',
                                     description='Simple ToDo cli application')
    parser.add_argument('-a', '--add', nargs='+', type=str, help='Adding one or more ToDo tasks. '
                                                                 'Type every task in " "')
    parser.add_argument('-l', '--list', action='store_true', help='Get list of ToDo tasks')

    # for accept only one command, remove or done
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-r', '--remove', nargs='+', type=int, help='Remove one or more ToDo tasks. '
                                                                   'Type id`s of task')
    group.add_argument('-d', '--done', nargs='+', type=int, help='Mark one or more ToDo tasks are done. '
                                                                 'Type id`s of task')
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
    else:

        database = DatabaseManager('todo.json')

        if args.add is not None:
            print(args.add)

        if args.remove is not None:
            pass

        if args.done is not None:
            pass

        if args.list is True:
            pass


if __name__ == '__main__':
    main()
