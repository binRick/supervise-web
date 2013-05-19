import os
from supervise_web.io import svstat

SERVICE_DIR = '/etc/service'


def daemon_info():
    info = {}
    for dir_name in os.listdir(SERVICE_DIR):
        dir_path = os.path.join(SERVICE_DIR, dir_name)
        if not os.path.isdir(dir_path):
            continue
        info[dir_name] = svstat(dir_path)
    return info