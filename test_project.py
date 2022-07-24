from project import User
import unittest
import datetime
from datetime import datetime
from colorama import Fore


def make_user():
    user = User('Some Name')
    user.add_task('some task')
    return user


class TestUser(unittest.TestCase):

    def test_add_task(self):
        user = make_user()
        result = user.to_do_list
        expect_result = {'1': ['some task', u'\u2606', str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), '~',
                               Fore.BLUE + u'\u2610' + Fore.RESET, '~']}
        self.assertEqual(expect_result, result)

    def test_remove_task(self):
        user = make_user()
        user.remove_task(['1'])
        result = user.to_do_list
        expect_result = {}
        self.assertEqual(expect_result, result)

    def test_check_main(self):
        user = make_user()
        user.check_main('1')
        result = user.to_do_list['1'][1]
        expect_result = Fore.LIGHTYELLOW_EX + u'\u2606' + Fore.RESET
        self.assertEqual(expect_result, result)

    def test_check_task(self):
        user = make_user()
        user.check_task('1')
        result = user.to_do_list['1'][4]
        expect_result = Fore.LIGHTYELLOW_EX + u'\u2611' + Fore.RESET
        self.assertEqual(expect_result, result)

    def test_set_deadline(self):
        user = make_user()
        user.set_deadline('1', '2022-07-03 10:00:00')
        result = user.to_do_list['1'][3]
        expect_result = '2022-07-03 10:00:00'
        self.assertEqual(expect_result, result)

    def test_check_deadline(self):
        user = make_user()
        user.set_deadline('1', '2022-07-03 10:00:00')
        user.check_deadline()
        result = user.to_do_list['1'][5]
        expect_result = Fore.RED + u'\u0021' + Fore.RESET
        self.assertEqual(expect_result, result)

    def test_check_show_list(self):
        user = make_user()
        result = user.show_list()
        expect_result = [['1', 'some task', u'\u2606', str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                          '~', Fore.BLUE + u'\u2610' + Fore.RESET, '~']]
        self.assertEqual(expect_result, result)


if __name__ == '__main__':
    unittest.main()
