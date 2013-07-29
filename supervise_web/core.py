import os
import ConfigParser
from supervise_web.svio import svstat, svcontrol, supervise

config = None


def daemon_info():
    info = {}
    for dir_name in os.listdir(_service_dir()):
        dir_path = os.path.join(_service_dir(), dir_name)
        if not os.path.isdir(dir_path):
            continue
        info[dir_name] = svstat(dir_path)
    return info


def fetch_log(log_file):
    """
    Try to find a log file definition in the run file
    """
    if not os.path.isfile(log_file):
        return ''
    with open(log_file, 'r') as f:
        return f.read()


def log_file_locations(dir_name, *args):
    """
    Get one or several log file locations for log names
    """
    cfg = _read_daemon_config(dir_name)
    return [cfg.get(dir_name, arg) if cfg.has_option(dir_name, arg) else None for arg in args]


def set_log_file_locations(dir_name, **kwargs):
    """
    Set one or several log file locations for log names
    """
    cfg = _read_daemon_config(dir_name)
    for name, path in kwargs.items():
        if path:
            cfg.set(dir_name, name, path)
        elif cfg.has_option(dir_name, name):
            cfg.remove_option(dir_name, name)
    _write_daemon_config(dir_name, cfg)


def run_file(dir_name, content=None, run_user=False):
    """
    Read or write the supervise 'run' file in the service directory
    If a content is given, write that content to the file, else read the file's content
    If run_user is True, write to the 'run-user' file instead
    """
    filename = 'run-user' if run_user else 'run'
    runfile = os.path.join(_service_dir(), dir_name, filename)
    if content is None:
        if not os.path.isfile(runfile):
            content = ''
        else:
            content = open(runfile, 'r').read()
    else:
        with open(runfile, 'w') as f:
            f.write(content)
        os.chmod(runfile, 0x1C0)  # -rwx------
    return content


def daemon_autostart(dir_name, enabled=None):
    down_file = os.path.join(_service_dir(), dir_name, 'down')
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
    return svcontrol(os.path.join(_service_dir(), dir_name), 'u')


def stop_daemon(dir_name):
    return svcontrol(os.path.join(_service_dir(), dir_name), 'd')


def start_supervise(dir_name):
    supervise(os.path.join(_service_dir(), dir_name))


def stop_supervise(dir_name):
    svcontrol(os.path.join(_service_dir(), dir_name), 'x')


def _service_dir():
    return config.get('Main', 'service_dir')


def _read_daemon_config(dir_name):
    daemon_config = ConfigParser.RawConfigParser()
    cfg_file = os.path.join(_service_dir(), dir_name, '.supervise_web.cfg')
    if os.path.exists(cfg_file):
        with open(cfg_file, 'r') as f:
            daemon_config.readfp(f)
    if not daemon_config.has_section(dir_name):
        daemon_config.add_section(dir_name)
    return daemon_config


def _write_daemon_config(dir_name, daemon_config):
    cfg_file = os.path.join(_service_dir(), dir_name, '.supervise_web.cfg')
    with open(cfg_file, 'w') as f:
        daemon_config.write(f)
