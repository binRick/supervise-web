from tests import BaseTestCase
from supervise_web.io import svstat, svcontrol
import datetime
import os
import time


class IoTestCase(BaseTestCase):
    def test_svstat(self):
        self._create_test_daemon(1)
        x = svstat(self._daemon_dir(1))
        self.assertFalse(x['daemon_paused'])
        self.assertTrue(x['daemon_autostart'])
        self.assertTrue(x['alive'])
        self.assertFalse(x['daemon_once'])
        self.assertTrue(x['daemon_up'])

        self.assertAlmostEquals(datetime.datetime.now(), x['daemon_timestamp'], delta=datetime.timedelta(seconds=1))
        self.assertTrue(0 < x['daemon_pid'] < 65536)

    def test_with_down_file(self):
        self._create_test_daemon(1)
        with open(os.path.join(self._daemon_supervise_dir(1), 'down'), 'w'):
            pass
        x = svstat(self._daemon_dir(1))
        self.assertFalse(x['daemon_paused'])
        self.assertFalse(x['daemon_autostart'])

    def test_svcontrol(self):
        self.assertFalse(svcontrol('/some/nonexisting/directory', 'u'))
        self._create_test_daemon(1)
        p = self._daemon_dir(1)
        self.assertTrue(svcontrol(p, 'u'))
        self.assertFalse(svstat(p)['daemon_once'])
        self.assertTrue(svstat(p)['daemon_up'])

        ts1 = svstat(p)['daemon_timestamp']
        svcontrol(p, 'd')  # stop the daemon
        time.sleep(1)
        ts2 = svstat(p)['daemon_timestamp']
        self.assertGreater(ts2, ts1)
        self.assertFalse(svstat(p)['daemon_once'])
        self.assertFalse(svstat(p)['daemon_up'])

        svcontrol(p, 'o')  # start daemon in 'run_once' mode
        time.sleep(1)
        ts3 = svstat(p)['daemon_timestamp']
        self.assertGreater(ts3, ts2)
        self.assertTrue(svstat(p)['daemon_once'])
        self.assertTrue(svstat(p)['daemon_up'])

        svcontrol(p, 'd')  # start the daemon up again
        time.sleep(1)
        self.assertGreater(ts3, ts2)
        self.assertFalse(svstat(p)['daemon_once'])
        self.assertFalse(svstat(p)['daemon_up'])

    def test_many_daemons(self):
        for i in range(15):
            self._create_test_daemon(i)
        for i in range(15):
            self.assertTrue(svstat(self._daemon_dir(i))['alive'])