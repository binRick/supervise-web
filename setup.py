import os
import subprocess
from setuptools import setup, find_packages


def version():
    p = subprocess.Popen(['git', 'describe'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    v = p.stdout.read()
    if not v:
        if os.path.isfile('VERSION'):
            v = open('VERSION', 'r').read()
        else:
            raise Exception('Could not determine version')
    with open('VERSION', 'w') as f:
        f.write(v)
    return v.strip()


def grab_package_data(*args):
    """ 
    Collecting all assets for the application to be packaged up - if there's a framework helper for that, let me know!
    """
    app_dir = 'supervise_web'
    package_data = []
    for dir_arg in args:
        data_dir = os.path.join(app_dir, dir_arg)
        for root, dir_names, file_names in os.walk(data_dir):
            root = root[(len(app_dir) + 1):]
            package_data += [os.path.join(root, f) for f in file_names]
    print package_data
    return package_data


setup(
     name='supervise_web',
     version=version(),
     author='Michael Schier',
     author_email='schiermike@gmail.com',
     description='A web interface for processes supervised with DJB daemontools.',
     license='MIT',
     keywords='supervise svc daemontools',
     url='https://github.com/schiermike/supervise-web',
     packages=find_packages(exclude=['tests']),
     package_data={'supervise_web': grab_package_data('assets', 'static', 'templates')},
     data_files=[
         ('', ['LICENSE.txt'])
     ],
     install_requires=[
         'Flask>=0.9',
         'Flask-Scss>=0.3',
         'pyScss>=1.1.5'
     ]
 )
