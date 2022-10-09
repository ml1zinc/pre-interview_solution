import sys
import json
import argparse

from os.path import exists

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




def main():

    parser = argparse.ArgumentParser(prog='todo',
                                     description='Simple ToDo cli application')
    parser.add_argument('-a', '--add', nargs='+', type=str, help='Adding one or more ToDo tasks. '
                                                                 'Type every task in " "')
    parser.add_argument('-l', '--list', action='store_true', help='Get list of ToDo tasks')
    parser.add_argument('-ld', '--done_list', action='store_true', help='Get list of DONE ToDo tasks')

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
        is_done_stat = args.done_list

        if add is not None:
            pass
          
        if remove is not None:
            pass
          
        if done is not None:
            pass
          
        if is_list is True:
            pass
          
        if is_done_stat is True:
            pass
          

if __name__ == '__main__':
    main()
