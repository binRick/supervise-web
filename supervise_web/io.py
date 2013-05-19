import os
import struct
import datetime


def svstat(daemon_dir):
    """
    Reads information from supervise's status file and checks whether the daemon and its supervise process are alive.

    :param daemon_dir: An abolute filesystem path to a directory containing the daemon script to be run by supervise.
    :rtype: `dict`
    """
    status = {}
    if not os.path.isfile(os.path.join(daemon_dir, 'run')) or not os.path.isdir(os.path.join(daemon_dir, 'supervise')):
        status['supervise_alive'] = False
        return status

    status_file = os.path.join(daemon_dir, 'supervise', 'status')
    with open(status_file, 'r') as f:
        status_code = f.read()

    # unpack the supervise status file
    # 8 byte timecode in secs
    # 4 byte timecode in nanosecs
    # 4 byte process id
    # 1 byte paused flag (boolean)
    # 1 byte want character
    status_code = '\0' + status_code[1:]
    unpacked = struct.unpack_from('>QI', status_code)
    started_at = datetime.datetime.fromtimestamp(unpacked[0])
    started_at = started_at.replace(microsecond=unpacked[1] / 1000)
    status['started_at'] = started_at

    unpacked = struct.unpack_from('<I?c', status_code, offset=12)
    status['pid'] = unpacked[0]
    status['paused'] = unpacked[1]
    status['want'] = unpacked[2]

    status['down'] = os.path.isfile(os.path.join(daemon_dir, 'supervise', 'down'))
    status['supervise_alive'] = True
    try:
        fid = os.open(os.path.join(daemon_dir, 'supervise', 'ok'), os.O_NONBLOCK | os.O_WRONLY)
    except OSError, e:
        if e.errno != 6:  # No such device or address
            raise
        status['supervise_alive'] = False
    else:
        os.close(fid)
    return status