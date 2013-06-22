from unittest import TestCase
import os
import signal
import shutil
import textwrap
import time
import supervise_web.core
from mock import Mock
from subprocess import Popen, PIPE
from supervise_web.io import svstat


class BaseTestCase(TestCase):
    def setUp(self):
        # create an empty test directory
        self.test_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tmp')
        supervise_web.core._service_dir = Mock(return_value=self.test_dir)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.mkdir(self.test_dir)
        self.supervise_procs = {}

    def tearDown(self):
        # shut down all test daemons and stop their supervise processes
        for num, supervise_proc in self.supervise_procs.items():
            daemon_pid = svstat(self._daemon_dir(num))['daemon_pid']
            supervise_proc.terminate()
            # only kill daemon if still alive (and not killed by some test)
            if os.path.exists('/proc/%d' % daemon_pid):
                os.kill(daemon_pid, signal.SIGTERM)

    def _daemon_dir(self, num):
        return os.path.join(self.test_dir, 'test_daemon_%d' % num)

    def _daemon_supervise_dir(self, num):
        return os.path.join(self._daemon_dir(num), 'supervise')

    def _daemon_run_file(self, num):
        return os.path.join(self._daemon_dir(num), 'run')

    def _create_test_daemon(self, num, sleep_interval=0.2):
        self._create_daemon_config(num, textwrap.dedent("""
            #!/usr/bin/python
            import datetime
            import time
            while True:
                time.sleep(%f)
            """ % sleep_interval)[1:])
        # start a new supervise process for this daemon
        supervise_proc = Popen(['supervise', self._daemon_dir(num)], stdin=PIPE, stderr=PIPE)
        max_wait = 2  # wait for at most 2 seconds for the supervise process to start
        while max_wait > 0:
            if svstat(self._daemon_dir(num))['alive']:
                break
            max_wait -= 0.1
            time.sleep(0.1)
        else:
            raise Exception('Supervise process did not start properly for test daemon <%d>' % num)
        self.supervise_procs[num] = supervise_proc

    def _create_daemon_config(self, num, daemon_code):
        if os.path.exists(self._daemon_dir(num)):
            raise Exception('Daemon path <%s> already exists' % self._daemon_dir(num))
        os.mkdir(self._daemon_dir(num))
        with open(self._daemon_run_file(num), 'w') as f:
            f.write(daemon_code)
        os.chmod(self._daemon_run_file(num), 0700)