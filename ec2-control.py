#!/usr/bin/env python
#
# Adapted from https://mcdee.com.au/nice-and-simple-aws-ec2-start-stop-script-python/
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
    logging.warning("""Settings file doesn't exist.\n
    Copy settings.py.sample to settings.py and change its values""")
    sys.exit(1)

def print_usage(args):
  print 'Usage:', args[0], 'stop|start <instance name>'
  sys.exit(1)
 
def usage(args):
  actions = ['stop', 'start']
  if not len(args) == 3:
    print_usage(args)
  else:
    if not args[1] in arg1:
      print_usage(args)
    else:
      return args[2]
 
conn = boto.ec2.connect_to_region(REGION,
                                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

try:
    inst = conn.get_only_instances(instance_ids=INSTANCE)[0]
except EC2ResponseError, e:
    logging.error("Instance %s not found. Double check instance id in settings"
                  % INSTANCE)
    sys.exit(1)

print(inst.state)

sys.exit(1)
 

if sys.argv[1] == 'start':
  try:
    inst = conn.get_all_instances(filters={'tag:Name': myinstance})[0].instances[0]
  except IndexError:
    print 'Error:', myinstance, 'not found!'
    sys.exit(1)
  if not inst.state == 'running':
    print 'Starting', myinstance
    inst.start()
  else:
    print 'Error:', myinstance, 'already running or starting up!'
    sys.exit(1)
 
if sys.argv[1] == 'stop':
  try:
    inst = conn.get_all_instances(filters={'tag:Name': myinstance})[0].instances[0]
  except IndexError:
    print 'Error:', myinstance, 'not found!'
    sys.exit(1)
  if inst.state == 'running':
    print 'Stopping', myinstance
    inst.stop()
  else:
    print 'Error:', myinstance, 'already stopped or stopping'
    sys.exit(1)
