from datetime import datetime
from datetime import time
from colorama import Fore, init
import os
import re

os.system('cls')
init()


def check_date(date_time: str) -> str:
    """
    Check user input. If date format is not correct raise ValueError.
    Also if date and time is not correct raise ValueError too.
    :param date_time: date and time in format "yyyy-mm-dd hh:mm:ss"
    :type date_time: str
    :return: date_time
    :type: str
    """

    if not re.search(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})|~$', date_time):
        os.system('cls')
        raise ValueError('Wrong format, must be "yyyy-mm-dd hh:mm:ss"')

    if date_time == '~':
        return date_time

    date, time_ = date_time.split(' ')
    year, month, day = date.split('-')
    hour, minute, second = time_.split(':')

    if not datetime(int(year), int(month), int(day)):
        raise ValueError
    if not time(int(hour), int(minute), int(second)):
        raise ValueError
    os.system('cls')

    return date_time


class User:
    """
    A class used to create user with his task
    """

    def __init__(self, name, to_do_list=None):
        self.name = name
        if to_do_list is None or len(to_do_list) == 0:
            self.to_do_list = {}
            self.id_task = 0
        else:
            self.to_do_list = to_do_list
            self.id_task = max(map(lambda x: int(x), list(to_do_list)))

    def add_task(self, task: str):
        """
        Method adds a new task to the dict of tasks
        :param task: Task which will be added to the dict
        :type task: str
        :return: None
        """
        self.id_task += 1
        self.to_do_list[str(self.id_task)] = [
            task, u'\u2733',
            str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), '~',
            Fore.BLUE + u'\u2610' + Fore.RESET, '~'
        ]

    def remove_task(self, id_tasks: list):
        """
        Method is responsible for remove task from dict and change all tasks id`s in numerical order
        :param id_tasks: id of tasks
        :type id_tasks: list
        :return: None
        """
        for id_task in id_tasks:
            self.to_do_list.pop(id_task)
            self.id_task -= 1
        self.to_do_list = {str(k): v for k, v in zip(range(1, len(self.to_do_list) + 1), self.to_do_list.values())}

    def check_main(self, id_task: str):
        """
        Method is responsible for mark task if it`s important. Method also could remove important mark
        :param id_task: id of task
        :type: str
        :return: None
        """
        if self.to_do_list[id_task][1] == u'\u2733':
            self.to_do_list[id_task][1] = Fore.YELLOW + u'\u2733' + Fore.RESET
        elif self.to_do_list[id_task][1] == Fore.YELLOW + u'\u2733' + Fore.RESET:
            self.to_do_list[id_task][1] = u'\u2733'

    def check_task(self, id_task: str):
        """
        Method marks task if it`s done. We also could change 'done mark'
        :param id_task: id of task
        :type: str
        :return: None
        """
        if self.to_do_list[id_task][4] == Fore.LIGHTYELLOW_EX + u'\u2611' + Fore.RESET:
            self.to_do_list[id_task][4] = Fore.BLUE + u'\u2610' + Fore.RESET
            self.to_do_list[id_task][5] = '~'

        elif self.to_do_list[id_task][4] == Fore.BLUE + u'\u2610' + Fore.RESET:
            self.to_do_list[id_task][4] = Fore.LIGHTYELLOW_EX + u'\u2611' + Fore.RESET

    def set_deadline(self, id_task: str, deadline: str):
        """
        Method is responsible for set deadline date in format '%Y-%m-%d %H:%M:%S'
        :param id_task: id of task
        :type: str
        :param deadline: date in format '%Y-%m-%d %H:%M:%S'
        :type: str
        :return: None
        """
        self.to_do_list[id_task][3] = check_date(deadline)

    def check_deadline(self):
        """
        Method mark task if current date is bigger than deadline  - mark is '!'
        :return: None
        """
        for task in self.to_do_list.keys():
            if self.to_do_list[task][3] < datetime.now().strftime('%Y-%m-%d %H:%M:%S') and self.to_do_list[task][4] \
                    != Fore.LIGHTYELLOW_EX + u'\u2611' + Fore.RESET:
                self.to_do_list[task][5] = Fore.RED + u'\u0021' + Fore.RESET
            else:
                self.to_do_list[task][5] = '~'

    def show_list(self) -> list:
        """
        Method shows the list of task
        :return: list of task
        """
        return [[k] + v for k, v in self.to_do_list.items()]


class Menu:
    """
    Class used to create menu of options
    """

    def __init__(self):
        self.menu = [[
            Fore.GREEN + 'Add task: +' + Fore.RESET,
            Fore.RED + 'Remove task: -' + Fore.RESET,
            Fore.BLUE + 'Check main: m' + Fore.RESET,
            Fore.YELLOW + 'Check task: v' + Fore.RESET,
            Fore.LIGHTCYAN_EX + 'Set deadline: d' + Fore.RESET,
            Fore.CYAN + 'Sort task: s' + Fore.RESET,
            Fore.MAGENTA + 'Exit: Q/q' + Fore.RESET,
        ]]

    def show_menu(self) -> list:
        """
        Method shows  menu of option
        :return: menu -> list
        """
        return self.menu
