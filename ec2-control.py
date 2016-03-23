#!/usr/bin/env python
#
 
import sys
import logging
import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import boto.ec2
    from boto.exception import EC2ResponseError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logging.basicConfig(format='%(message)s (%(levelname)s)',
                    level=logging.INFO)
logging.getLogger('boto').propagate = False
boto.set_file_logger('boto', '/tmp/mc-control.log')

try:
    from settings import *
except ImportError:
    logging.warning("Settings file doesn't exist.\n"
    "Copy settings.py.sample to settings.py and change its values")
    sys.exit(1)

conn = boto.ec2.connect_to_region(REGION,
                                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

try:
    inst = conn.get_only_instances(instance_ids=INSTANCE)[0]
except EC2ResponseError, e:
    logging.error("Instance %s not found. Double check instance id in settings"
                  % INSTANCE)
    sys.exit(1)

logging.debug("instance status: %s" % inst.state)
if inst.state not in ['running', 'stopped']:
    logging.warning("Instance currently %s. Please run again when it has "
                    "stopped.")
    sys.exit(1)

action = 'toggle'
try:
    action = sys.argv[1]
except IndexError:
    pass

if action in ['start', 'launch', 'up']:
    action = 'start'
elif action in ['stop', 'kill', 'down']:
    action = 'stop'
else:
    action = 'toggle'

logging.debug("action: %s" % action)

if action == 'start' or (action == 'toggle' and inst.state != 'running'):
    logging.info("Starting up...")
    inst.start()
 
if action == 'stop' or (action == 'toggle' and inst.state == 'running'):
    logging.info("Stopping")
    inst.stop()
