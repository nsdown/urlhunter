from flask import url_for
from tests.base import BaseTestCase


class UserTestCase(BaseTestCase):
    def test_index(self):
        response = self.client.get(url_for('user.index', username='alphardex'))
        data = response.get_data(as_text=True)
        self.assertIn('alphardex', data)
