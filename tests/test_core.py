from tests import BaseTestCase
from supervise_web.core import daemon_autostart, run_file


class CoreTestCase(BaseTestCase):

    def test_daemon_autostart(self):
        self._create_test_daemon(1)
        dir_name = 'test_daemon_1'
        self.assertTrue(daemon_autostart(dir_name))

        daemon_autostart(dir_name, enabled=True)
        self.assertTrue(daemon_autostart(dir_name))

        daemon_autostart(dir_name, enabled=False)
        self.assertFalse(daemon_autostart(dir_name))

        daemon_autostart(dir_name, enabled=False)
        self.assertFalse(daemon_autostart(dir_name))

        daemon_autostart(dir_name, enabled=True)
        self.assertTrue(daemon_autostart(dir_name))

    def test_run_file(self):
        self._create_test_daemon(1)
        dir_name = 'test_daemon_1'

        self.assertLess(23, len(run_file(dir_name)))
        run_file(dir_name, content='some new content')

        self.assertEqual('some new content', run_file(dir_name))