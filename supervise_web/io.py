import os
import stat
import struct
import datetime


def svstat(daemon_dir):
    """
    Reads information from supervise's status file and checks whether the daemon and its supervise process are alive.
    Possible dictionary entries:
        * daemon_timestamp: the time the daemon was last started or stopped (datetime)
        * alive: True iff there is a running supervise process
        * daemon_pid: the process id of the daemon process
        * daemon_paused: set when a pause signal was sent to the daemon (and there was no continue after it)
        * daemon_once: True iff the supervise process should not restart the daemon after the daemon dies
        * daemon_up: True iff the supervise process wants the daemon to be running
        * daemon_autostart: False iff there exists a file 'down' in the supervise folder which prevents supervise from
                            starting the daemon

    :param daemon_dir: An abolute filesystem path to a directory containing the daemon script to be run by supervise.
    :rtype: `dict`
    """
    status = {}
    if not os.path.isfile(os.path.join(daemon_dir, 'run')) or not os.path.isdir(os.path.join(daemon_dir, 'supervise')):
        status['alive'] = False
        return status

    status_file = os.path.join(daemon_dir, 'supervise', 'status')
    with open(status_file, 'r') as f:
        status_code = f.read()

    # unpack the supervise status file
    # 8 byte timecode in secs
    # 4 byte timecode in nanosecs
    # 4 byte process id
    # 1 byte paused flag (boolean)
    # 1 byte want character - can be either 'u' for up, 'd' for down or 0x00 for once (supervise won't restart the
    #                         daemon when the daemon dies)
    status_code = '\0' + status_code[1:]
    unpacked = struct.unpack_from('>QI', status_code)
    timestamp = datetime.datetime.fromtimestamp(unpacked[0])
    timestamp = timestamp.replace(microsecond=unpacked[1] / 1000)
    status['daemon_timestamp'] = timestamp

    unpacked = struct.unpack_from('<I?c', status_code, offset=12)
    status['daemon_pid'] = unpacked[0]
    status['daemon_paused'] = unpacked[1]
    status['daemon_once'] = unpacked[2] == '\0'
    status['daemon_up'] = unpacked[2] != 'd'  # else 'u' or 0x00

    status['daemon_autostart'] = not os.path.isfile(os.path.join(daemon_dir, 'supervise', 'down'))
    status['alive'] = True
    try:
        fd = os.open(os.path.join(daemon_dir, 'supervise', 'ok'), os.O_NONBLOCK | os.O_WRONLY)
    except OSError, e:
        if e.errno != 6:  # No such device or address
            raise
        status['alive'] = False
    else:
        os.close(fd)
    return status


def svcontrol(daemon_dir, control_char):
    """
    Writes control information to a pipe that is read by the supervise process (if there is one).
    Returns False if writing the control information fails.

    :rtype: `bool`
    """
    control_file = os.path.join(daemon_dir, 'supervise', 'control')
    if not os.path.exists(control_file) or not stat.S_ISFIFO(os.stat(control_file).st_mode):
        return False
    if control_char not in ['u', 'd', 'o', 'x', 'p', 'c', 'h', 'a', 'i', 't', 'k']:
        raise ValueError('Unrecognized control char <%s>' % control_char)
    try:
        fd = os.open(control_file, os.O_WRONLY | os.O_NONBLOCK)
        os.write(fd, control_char)
        os.close(fd)
        return True
    except OSError, e:
        if e.errno != 6:
            raise
        return False