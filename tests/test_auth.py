from flask import url_for
from tests.base import BaseTestCase


class AuthTestCase(BaseTestCase):
    def test_login_user(self):
        response = self.login()
        data = response.get_data(as_text=True)
        self.assertIn('alphardex', data)

    def test_fail_login_nonexist_user(self):
        response = self.login(username='alphardesa', password='elpsycongroo')
        data = response.get_data(as_text=True)
        self.assertIn('该用户不存在！', data)

    def test_fail_login_wrong_password(self):
        response = self.login(username='alphardex', password='emmmm')
        data = response.get_data(as_text=True)
        self.assertIn('密码错误！', data)

    def test_logout_user(self):
        self.login()
        response = self.logout()
        data = response.get_data(as_text=True)
        self.assertIn('登录', data)

    def test_register_page(self):
        response = self.client.get(url_for('auth.register'))
        data = response.get_data(as_text=True)
        self.assertIn('请注册', data)

    def test_register_account(self):
        response = self.client.post(
            url_for('auth.register'),
            data={
                'username': 'alphardesu',
                'email': '2582347431@qq.com',
                'password': 'elpsycongroo',
                'confirm': 'elpsycongroo'
            },
            follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('注册成功！', data)

    def test_unique_field(self):
        response = self.client.post(
            url_for('auth.register'),
            data={
                'username': 'alphardesu',
                'email': '2582347430@qq.com',
                'password': 'elpsycongroo',
                'confirm': 'elpsycongroo'
            },
            follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('该邮箱已被占用', data)

    def test_already_login(self):
        self.login()
        response = self.client.get(url_for('auth.login'))
        data = response.get_data(as_text=True)
        self.assertNotIn('请登录', data)
