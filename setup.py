from setuptools import setup, find_packages
from subprocess import check_output


setup(
     name='supervise_web',
     version=check_output(['git', 'describe']).strip(),
     author='Michael Schier',
     author_email='schiermike@gmail.com',
     description='A web interface for processed supervised with DJB daemontools.',
     license='MIT',
     keywords='supervise svc daemontools',
     url='https://github.com/schiermike/supervise-web',
     packages=find_packages(exclude=['tests']),
     package_data={'': [
         'static/img/*',
         'static/js/*',
         'static/css/*.css',
         'static/css/fonts/*',
         'static/css/images/*',
         'templates/*',
         'assets/*'
     ]},
     install_requires=[
         'Flask>=0.9',
         'Flask-Scss>=0.3',
         'pyScss>=1.1.5'
     ]
 )