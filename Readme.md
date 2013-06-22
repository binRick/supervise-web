Supervise-Web
=============

Supervise-Web is a web frontend for [Daniel J. Bernstein's supervise tools](http://cr.yp.to/daemontools.html) `svc`,
`svstat`, and `supervise` from the daemontools collection. It was created in an effort to facilitate monitoring the
health and responsiveness of daemons, and to speed up the process of upgrading a set of daemons simulateously.

It allows you to monitor all daemons that are deployed in a directory such as `/service` or `/etc/service` and are
possibly managed by `svscan`. Moreover, you can ...

* start and stop daemons
* start and stop their supervise processes
* change the autostart-settings of daemons
* monitor supervise and daemon log files
* edit the `run` and `run-user` configuration files
* control the monitoring-interval

Supervise-Web is written in python and uses the flask microframework. All communication between Supervise-Web and
supervise processes is done directly via the supervise file queues - `svc` and `svstat` are not needed.

Beware that Supervise-Web is by no means secure, so make sure that access to it is restricted before deployment.


Installation
------------

It is possible to run supervise-web without having to setup a virtual environment for it. However, I recommend doing it
the virtualenv-way:

1. Create a python-2.7 virtual environment at some location
    * `virtualenv --no-site-packages /opt/pyenv_supervise_web`

2. Adjust the `run` and the `supervise_web.cfg` files
    * Set the correct path to your virtualenv in the `run` file
    * Change port and credentials in the `supervise_web.cfg` file

3. Create the directory `/etc/service/supervise_web` and copy the `run` file as well as the `supervise_web.cfg` file
to that place. Be aware that on some systems `/service` is used instead of `/etc/service`.

4. Go to http://localhost:5000 (hostname or port might be different depending on your setup and settings) and check
whether it's working. Supervise-web should show up in the list of supervised daemons.