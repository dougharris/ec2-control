# EC2 Control

Python script to start and stop a single EC2 instance.

## Set Up

This does not work out of the box. You need to configure your python
environment and you need to specify your Amazon Web Services (AWS)
information.

### Python environment

You need to install the
[boto Python library](http://boto.cloudhackers.com/en/latest/) for
communicating with AWS. The best way to do this is with
[`virtualenv`](https://virtualenv.pypa.io/en/latest/).

Assuming you have `virtualenv` installed, do the following in the
directory where you've checked this out:

    $ virtualenv env                  # create the virtual environment
    $ . env/bin/activate              # activate the environment
    $ pip install < requirements.txt  # install boto, et al.

### AWS Settings

The main script uses `settings.py` to identify the AWS region,
instance id, and authentication credentials - but this file doesn't
exist in the git repository. Copy the `settings.py.sample` to
`settings.py` and edit.

## Running

The script takes an optional argument. If you pass "start" or "stop"
(or some synonyms), the script will try to execute those actions. If
you do not pass an argument, the script will determine the instance's
state and toggle it; _i.e._ if the instance is running, it'll stop the
instance, otherwise it'll start it.

Examples:

    $ ./ec2-control.py start
    $ ./ec2-control.py stop
    $ ./ec2-control.py                # toggle state

## Background

In putting together a Minecraft server running on a
small EC2 instance, I wanted to give my son an easy way to start the
instance remotely.
