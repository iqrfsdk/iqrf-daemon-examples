# #############################################################################
# Author: 2017 Rostislav Spinar <rostislav.spinar@iqrf.com>                   #
#         IQRF Tech s.r.o.                                                    #
# #############################################################################

# #############################################################################
#                                                                             #
# sudo apt-get install python-dev build-essential                             #
# sudo apt-get install python-pip                                             #
# sudo pip install paho-mqtt                                                  #  
#                                                                             #
# #############################################################################

import sys
import getopt
import time
import json

import paho.mqtt.client as paho
 
def on_connect(client, userdata, flags, rc):
  print('CONNACK received with code %d.' % (rc))

def on_publish(client, userdata, mid):
  print('mid: ' + str(mid))

def on_subscribe(client, userdata, mid, granted_qos):
  print('Subscribed: ' + str(mid) + ' ' + str(granted_qos))
 
def on_message(client, userdata, msg):
  print(msg.topic + ' ' + str(msg.qos) + ' ' + str(msg.payload))

def on_log(mqttc, userdata, level, string):
  print(string)

def create_dpa_frame(node_id, pnum, pcmd, hwpid, data=[]):

  byte_str = '%02x.%02x.%02x.%02x.%02x.%02x' % (node_id & 0xFF,
                                                node_id >> 8,
                                                pnum, pcmd,
                                                hwpid & 0xFF,
                                                hwpid >> 8)
  for i in data:
    byte_str += '.%02x' % i

  return byte_str

def create_dpa_json(msg_id, dpa_frame):
  request = {}
  request['ctype'] = 'dpa'
  request['type'] = 'raw'
  request['msgid'] = msg_id
  request['request'] = dpa_frame
  request['request_ts'] = ''
  request['confirmation'] = ''
  request['confirmation_ts'] = ''
  request['response'] = ''
  request['response_ts'] = ''

  return json.dumps(request)

def print_usage():
  print('iqrf_daemon_mqtt.py [-d] [-h hostname] [-p port] [-tp topic_pub] [-ts topic_sub]')

def main(argv):
  #IQRF
  # default hwpid
  hwpid = 0xffff
  # default DPA timeout (in miliseconds)
  timeout = 1000

  #MQTT
  host = 'localhost'
  port = 1883
  keepalive = 60
  client_id = str(time.time())
  #password = None
  #username = None
  debug=False

  topic_pub = 'Iqrf/DpaRequest'
  topic_sub = 'Iqrf/DpaResponse'

  try:
    opts, args = getopt.getopt(argv, 'd:h:p:tp:ts', ['debug', 'host=', 'port=', 'topic_pub=', 'topic_sub='])
  except getopt.GetoptError as s:
    print_usage()
    sys.exit(2)
    
  for opt, arg in opts:
    if opt in ('-d', '--debug'):
      host = arg
    elif opt in ('-h', '--host'):
      host = arg
    elif opt in ('-p', '--port'):
      port = int(arg)
    elif opt in ('-tp', '--topic_pub'):
      topic_pub = arg
      print(topic_pub)
    elif opt in ('-ts', '--topic_sub'):
      topic_sub = arg
      print(topic_sub)

  # client
  client = paho.Client(client_id=client_id, clean_session=True, userdata=None, protocol=paho.MQTTv31)
  #client.username_pw_set(username, password)
  #client.tls_set(“/path/to/ca.crt”)

  # client callbacks
  client.on_connect = on_connect
  client.on_publish = on_publish
  client.on_subscribe = on_subscribe
  client.on_message = on_message

  # debug
  if debug:
    client.on_log = on_log

  # connect
  client.connect(host=host, port=port, keepalive=keepalive, bind_address='')

  # subscribe
  client.subscribe(topic_sub)

  # blocking, good for sub only
  #client.loop_forever()

  # not blocking, background thread, returns
  client.loop_start()
  #client.loop_stop()

  # dpa frame
  dpa_frame = create_dpa_frame(0x0f, 0x06, 0x03, hwpid)

  while True:
    # json dpa
    msg_id = str(time.time())
    json_dpa = create_dpa_json(msg_id, dpa_frame)
  
    # publish
    (rc, mid) = client.publish(topic_pub, json_dpa, qos=1)
  
    # sleep
    time.sleep(10)

if __name__ == "__main__":
  main(sys.argv[1:])
