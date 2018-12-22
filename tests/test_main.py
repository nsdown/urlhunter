from flask import url_for
from tests.base import BaseTestCase


class MainTestCase(BaseTestCase):
    def test_index(self):
        response = self.client.get(url_for('main.index'))
        data = response.get_data(as_text=True)
        self.assertIn('登录', data)

        self.login()
        response = self.client.get(url_for('main.index'))
        data = response.get_data(as_text=True)
        self.assertNotIn('登录', data)

    def test_extract(self):
        self.login()
        response = self.client.post(
            url_for('main.extract'),
            data={'urls': 'http://alphardex.pythonanywhere.com/'},
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_fail_extract(self):
        self.login()
        response = self.client.post(
            url_for('main.extract'),
            data={
                'urls': 'http://alphardex.pythonanywhere.com/',
                'search': 'nothingelse'
            },
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_search_extract(self):
        self.login()
        response = self.client.post(
            url_for('main.extract'),
            data={
                'urls': 'http://alphardex.pythonanywhere.com/',
                'search': 'trending'
            },
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_pattern_extract(self):
        self.login()
        response = self.client.post(
            url_for('main.extract'),
            data={
                'urls': 'http://alphardex.pythonanywhere.com/',
                'search': 'http://alphardex.pythonanywhere.com/photos/.*?',
                'use_regex': True
            },
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_show_urls(self):
        self.login()
        response = self.client.get(url_for('main.show_urls'))
        data = response.get_data(as_text=True)
        self.assertIn('URL', data)

    def test_delete_urls(self):
        self.login()
        response = self.client.post(
            url_for('main.delete_urls'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('还没有URL哦', data)

    def test_show_regexs(self):
        self.login()
        response = self.client.get(url_for('main.show_regexs'))
        self.assertEqual(response.status_code, 200)

    def test_search_urls(self):
        self.login()
        response = self.client.get(url_for('main.search_urls', q='test'))
        self.assertEqual(response.status_code, 200)

    def test_search_none(self):
        self.login()
        response = self.client.get(url_for('main.search_urls', q=''), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('请输入要搜索的URL', data)

    def test_show_help(self):
        response = self.client.get(url_for('main.show_help'))
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('使用说明', data)

    def test_upload_regex(self):
        self.login()
        response = self.client.post(url_for('main.upload_regex'), data={
            'name': 'Github trending',
            'site': 'https://github.com/trending',
            'body': 'https://github.com/(?!(trending|login))\w+/\w+(?!/)'
        }, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('添加成功！', data)

    def test_upload_regex_page(self):
        self.login()
        response = self.client.get(url_for('main.upload_regex'))
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('自定义正则', data)
