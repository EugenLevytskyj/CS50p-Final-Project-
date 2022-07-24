import sys
from tabulate import tabulate
import json
from colorama import Fore, init
import os
from general import User, Menu


os.system('cls')

init()

sort_dict = {
            '1': 0, '2': 1,
            '3': 2, '4': 3,
            '5': 4, '6': 5,
            '7': 6
            }

tab_header = [Fore.LIGHTWHITE_EX +
              'id', 'task',
              'main', 'date',
              'deadline', 'done',
              'warning mark' + Fore.RESET
              ]


def main():
    if os.path.exists(f'users.json'):
        name, us_dict = help_dow(download())
        user = User(name, us_dict)
    else:
        name, us_dict = help_dow()
        user = User(name, us_dict)

    menu = Menu()
    controller(user.name, user, menu, tab_header)


def show_sorted(list_for_sort: list, key=0, rev=False) -> list:
    """
    Show sorted list
    :param rev:
    :param list_for_sort: List which will be sorted
    :type list_for_sort: list
    :param key: Key (parameter) for sort
    :type key: int
    :return: Sorted list
    :rtype: list
    """
    return sorted(list_for_sort, key=lambda x: x[key], reverse=rev)


def download():
    """
    Download user info from json file

    """
    with open('users.json') as file_obj:
        dict_todo = json.load(file_obj)
        return dict_todo


def help_dow(dict_u=None):
    """
     Function that help to download correct info from the file. If the user is already in file
     it will return  tuple (user name,  dict). If there is no the user with the name it
     propose to make a new user or quit
    :param dict_u:
    :return: tuple or None
    """

    if not dict_u:
        dict_u = {}

    while True:
        name = input(Fore.LIGHTYELLOW_EX + 'Hi! Enter your name or Q/q for exit: ' + Fore.RESET).rstrip().lower()
        os.system('cls')

        if name == 'q':
            os.system('cls')
            sys.exit(Fore.LIGHTYELLOW_EX + '\nGoodbye!\n' + Fore.RESET)
        if name in dict_u.keys():
            os.system('cls')
            return name, dict_u[name]

        print(Fore.LIGHTBLUE_EX + f'There is no user with name "{name.capitalize()}". Do you want to make user'
                                  f' "{name.capitalize()}"? - y/n: ',
              end='' + Fore.RESET)
        if input('') == 'y':
            os.system('cls')
            return name, {}
        else:
            os.system('cls')
            print(Fore.LIGHTBLUE_EX + 'Do you want to quit or continue? - q/c: ', end='' + Fore.RESET)
            if input('') == "q":
                os.system('cls')
                sys.exit(Fore.LIGHTYELLOW_EX + '\nGoodbye!\n' + Fore.RESET)
            else:
                os.system('cls')
                continue


def upload(name: str, dict_todo: dict):
    """
    Upload users tasks ro file
    :param name: Name of user whose data will be upload to file
    :type name: Str
    :param dict_todo: Dict of user tasks
    :type dict_todo: Dict
    :return: None
    """
    try:
        with open('users.json', 'r') as file_obj:
            dict_todo_all = json.load(file_obj)
        with open('users.json', 'w') as file_obj:
            dict_todo_all[name] = dict_todo
            json.dump(dict_todo_all, file_obj)
    except FileNotFoundError:
        with open('users.json', 'w') as file_obj:
            dict_todo_all = {name: dict_todo}
            json.dump(dict_todo_all, file_obj)


def controller(name, user, menu, header):
    """
    Its runs program
    :param name: User name
    :param user: object user
    :param menu: object menu
    :param header: head of the menu
    :return: -
    """
    key = 0
    rev = False

    while True:
        user.check_deadline()
        print(tabulate([[Fore.LIGHTCYAN_EX + 'User: ' + user.name.capitalize() + Fore.RESET]], tablefmt='rst'))
        print(tabulate(menu.show_menu(), tablefmt='rst'))
        print(tabulate(show_sorted(user.show_list(), key, rev), header, tablefmt='grid'))

        option = input('Chose option: ').lower()

        try:
            match option:
                case 'q':
                    upload(name, user.to_do_list)
                    os.system('cls')
                    sys.exit(Fore.LIGHTYELLOW_EX + '\nGoodbye!\n' + Fore.RESET)
                case '+':
                    user.add_task(input('Task: '))
                    os.system('cls')
                case '-':
                    print('Please, enter one or mode id which you want to delete: ' + Fore.MAGENTA + '1 2 3 ....'
                          + Fore.RESET)
                    user.remove_task(input('ID task: ').split())
                    os.system('cls')
                case 'm':
                    user.check_main(input('ID task: '))
                    os.system('cls')
                case 'v':
                    user.check_task(input('ID task: '))
                    os.system('cls')
                case 'd':
                    d_id = input('ID task: ')
                    d_deadline = input('Deadline: ')
                    user.set_deadline(d_id, d_deadline)
                    os.system('cls')
                case 's':
                    print(Fore.CYAN + 'Sort by id - 1, By task - 2, By main task - 3, '
                                      'By date - 4 , By deadline - 5, By status - 6, '
                                      'By warning mark - 7' + Fore.RESET)
                    opt = input('How to sort: ')
                    key = sort_dict[opt]
                    if opt == '6':
                        rev = True
                    else:
                        rev = False
                    os.system('cls')
        except KeyError:
            os.system('cls')
            continue
        except TypeError:
            os.system('cls')
            continue
        except ValueError as e:
            os.system('cls')
            print('\n' + Fore.RED + str(e) + Fore.RESET + '\n')
            continue
        os.system('cls')


if __name__ == '__main__':
    main()
