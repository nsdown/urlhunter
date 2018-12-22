import unittest
from flask import url_for
from urlhunter import create_app
from urlhunter.extensions import db
from urlhunter.models import User


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        app = create_app('testing')
        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()
        self.runner = app.test_cli_runner()
        db.create_all()
        user = User(username='alphardex', email='2582347430@qq.com')
        user.set_password('elpsycongroo')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.drop_all()
        self.context.pop()

    def login(self, username=None, password=None):
        if not all([username, password]):
            username = 'alphardex'
            password = 'elpsycongroo'

        return self.client.post(url_for('auth.login'), data={
            'username': username,
            'password': password
        }, follow_redirects=True)

    def logout(self):
        return self.client.get(url_for('auth.log_out'), follow_redirects=True)
