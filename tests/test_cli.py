from urlhunter.extensions import db
from tests.base import BaseTestCase


class CLITestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        db.drop_all()

    def test_ptshell(self):
        result = self.runner.invoke(args=['ptshell'])
        self.assertNotIn('ptpython not installed! Use the default shell instead.', result.output)
        