import os
from supervise_web.io import svstat, svcontrol, supervise

config = None


def daemon_info():
    info = {}
    for dir_name in os.listdir(service_dir()):
        dir_path = os.path.join(service_dir(), dir_name)
        if not os.path.isdir(dir_path):
            continue
        info[dir_name] = svstat(dir_path)
    return info


def log_tail(dir_name, num_lines=100):
    raise NotImplementedError('to be implemented')


def run_file(dir_name, content=None):
    runfile = os.path.join(service_dir(), dir_name, 'run')
    if content is None:
        if not os.path.isfile(runfile):
            return ''
        return open(runfile, 'r').read()
    else:
        with open(runfile, 'w') as f:
            f.write(content)
        os.chmod(runfile, 0x1C0)  # -rwx------


def daemon_autostart(dir_name, enabled=None):
    down_file = os.path.join(service_dir(), dir_name, 'down')
    if enabled is True:
        if daemon_autostart(dir_name):
            return
        os.remove(down_file)
    elif enabled is False:
        if not daemon_autostart(dir_name):
            return
        open(down_file, 'a').close()
    else:
        return not os.path.isfile(down_file)


def start_daemon(dir_name):
    return svcontrol(os.path.join(service_dir(), dir_name), 'u')


def stop_daemon(dir_name):
    return svcontrol(os.path.join(service_dir(), dir_name), 'd')


def start_supervise(dir_name):
    supervise(os.path.join(service_dir(), dir_name))


def stop_supervise(dir_name):
    svcontrol(os.path.join(service_dir(), dir_name), 'x')


def service_dir():
    return config.get('Main', 'service_dir')