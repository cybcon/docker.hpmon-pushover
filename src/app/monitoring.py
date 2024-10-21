# -*- coding: utf-8 -*-
""" ***************************************************************************
monitoring.py - is a tool to monitor if a webpage is up and running
outages will be send as pushover messages
Author: Michael Oberdorf
Datum: 2021-11-30
*************************************************************************** """
import os
import sys
import json
import requests
import logging
import time

VERSION = '1.1.0'
"""
###############################################################################
# F U N C T I O N S
###############################################################################
"""

def get_monitoring_configuration(path: str):
    """
    get_monitoring_configuration
    @summary: function to read the monitoring configuration from local filesystem or from remote
    @param path: String, file (file://) or url (http(s)?://) to the monitoring configuration JSON file
    @return: dict(), the JSON from given path as parsed dict()
    """
    monitoring_configuration=dict()
    if path.strip().lower().startswith('file://'):
        filename = path[7:]
        log.debug("Load local configuration file: {}".format(filename))
        if not os.path.isfile(filename):
            log.error('File not found exception: {}'.format(filename))
            raise Exception('File not found exception: {}'.format(filename))

        with open(filename, encoding='utf-8') as f:
            monitoring_configuration = json.load(f)
    if path.strip().lower().startswith('http://') or path.strip().lower().startswith('https://'):
        log.debug("Load  configuration from url: {}".format(path))
        try:
            response = requests.get(path)
        except:
            log.error('Error while retrieving monitoring configuration from URL: {}. URL not reachable!'.format(filename))
        if response.status_code != 200:
            log.error('Error while retrieving monitoring configuration from URL: {}. Return code {}'.format(filename, response.status_code))
            raise Exception('Error while retrieving monitoring configuration from URL: {}. Return code {}'.format(filename, response.status_code))

        monitoring_configuration = json.loads(response.text)

    log.debug("Monitoring configuration loaded:\n{}".format(json.dumps(monitoring_configuration, indent=4)))
    return(monitoring_configuration)

def check_status(url: str, return_code: int = 200, ok_string: str = None, warn_string: str = None):
    """
    check_status
    @summary: function to check if a given webpage is up and running
    @param url: String, the URL of the webpage
    @param return_code: Integer, the HTTP return to validate (default: 200)
    @param ok_string: String, a String to check inside the response.text (default: None)
    @param warning_string: String, a String to check inside the response.text (default: None)
    @return: Integer, String, returns the result of the check (0 for error, 1 for warning, 2 for OK) and an optional information to the state
    """
    try:
        response = requests.get(url)
    except:
        return(0, "URL not reachable")

    if response.status_code != return_code:
        return(0, "URL reachable, but status code {} != {}".format(response.status_code, return_code))

    if ok_string != None:
        if ok_string in response.text:
            return(2, "OK")
        elif warn_string != None and warn_string in response.text:
            return(1, "String found for warning indication in response body: " + warn_string)
        else:
            return(0, "Validation pattern not found in response body")
    else:
        return(2, "OK")


def send_pushover_message(userkey: str, apikey: str, title: str, message: str, priority: int = 0):
    """
    Send the given message via pushover services
    @see: https://pushover.net/api
    @param userkey: string,
    @param apikey: string,
    @param title: string,
    @param message: string,
    @param priority: integer, the PushOver message priority (-2 to 2, default: 0)
    """
    import http.client, urllib
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
      "token": apikey,
      "user": userkey,
      "title": title,
      "message": message,
      "priority": priority
      }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

"""
###############################################################################
# M A I N
###############################################################################
"""
log = logging.getLogger()
log_handler = logging.StreamHandler(sys.stdout)
if not 'LOGLEVEL' in os.environ:
    log.setLevel(logging.INFO)
    log_handler.setLevel(logging.INFO)
else:
  if os.environ['LOGLEVEL'].lower() == 'debug':
      log.setLevel(logging.DEBUG)
      log_handler.setLevel(logging.DEBUG)
  elif os.environ['LOGLEVEL'].lower() == 'info':
      log.setLevel(logging.INFO)
      log_handler.setLevel(logging.INFO)
  elif os.environ['LOGLEVEL'].lower() == 'warning':
      log.setLevel(logging.WARN)
      log_handler.setLevel(logging.WARN)
  elif os.environ['LOGLEVEL'].lower() == 'error':
      log.setLevel(logging.ERROR)
      log_handler.setLevel(logging.ERROR)
  else:
      log.setLevel(logging.INFO)
      log_handler.setLevel(logging.INFO)
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_formatter)
log.addHandler(log_handler)

log.info('OITC Webpage Monitoring System version ' + VERSION + ' started')

# Read environment variables
log.debug('Validate environment variables')
if not 'PUSHOVER_USER_KEY' in os.environ:
    log.error('Environment variable PUSHOVER_USER_KEY not defined')
    raise Exception('Environment variable PUSHOVER_USER_KEY not defined')
if not 'PUSHOVER_API_KEY' in os.environ:
    log.error('Environment variable PUSHOVER_API_KEY not defined')
    raise Exception('Environment variable PUSHOVER_API_KEY not defined')
if not 'MONITORING_CONFIGURATION_URL' in os.environ:
    log.error('Environment variable MONITORING_CONFIGURATION_URL not defined')
    raise Exception('Environment variable MONITORING_CONFIGURATION_URL not defined')
repeat_on_error=False
if 'REPEAT_ON_ERROR' in os.environ:
    repeat_on_error=False
    if os.environ['REPEAT_ON_ERROR'].lower() == 'true' or os.environ['REPEAT_ON_ERROR'].lower() == 'yes':
        repeat_on_error=True
if repeat_on_error:
    # set default values
    max_repeat_counter=1
    repeat_wait_time=2
    if 'REPEAT_ON_ERROR_COUNTER' in os.environ:
        max_repeat_counter=int(os.environ['REPEAT_ON_ERROR_COUNTER'])
    if 'REPEAT_ON_ERROR_WAIT_TIME_SEC' in os.environ:
        repeat_wait_time=int(os.environ['REPEAT_ON_ERROR_WAIT_TIME_SEC'])
else:
    # set default values
    max_repeat_counter=0
    repeat_wait_time=0


CONFIG = get_monitoring_configuration(os.environ['MONITORING_CONFIGURATION_URL'])

if 'webpages' in CONFIG:
    for webpage in CONFIG['webpages']:
        log.debug('Process monitoring entry: ' + json.dumps(webpage))
        if not 'monitoring_url' in webpage or len(webpage['monitoring_url']) < 7:
            log.warning('Entry has no attribute "monitoring_url": ' + json.dumps(webpage))
            continue

        response_ok_data = None
        if 'response_ok_data' in webpage and webpage['response_ok_data'] != None and len(webpage['response_ok_data']):
            response_ok_data = webpage['response_ok_data']
        response_warn_data = None
        if 'response_warn_data' in webpage and webpage['response_warn_data'] != None and len(webpage['response_warn_data']):
            response_warn_data = webpage['response_warn_data']

        if 'return_code' in webpage and isinstance(webpage['return_code'], int):
            return_code = int(webpage['return_code'])
        else:
            return_code = 200

        repeat_counter=0
        while max_repeat_counter <= repeat_counter:
            repeat_counter+=1
            status, details = check_status(url=webpage['monitoring_url'], return_code=200, ok_string=response_ok_data, warn_string=response_warn_data)
            if status == 2 and repeat_on_error:
                log.warning('WARNING ' + webpage['monitoring_url'] + ' (' + details + ') - repeat in ' + str(repeat_wait_time) + ' seconds.')
                time.sleep(repeat_wait_time)


        if status == 2:
            log.info('OK ' + webpage['monitoring_url'])
        elif status == 1:
            log.warning('WARNING ' + webpage['monitoring_url'] + ' (' + details + ')')
            send_pushover_message(userkey=os.environ['PUSHOVER_USER_KEY'],
                                  apikey=os.environ['PUSHOVER_API_KEY'],
                                  title='Website warning',
                                  message="Website monitoring warning for ({})\nDetails: {}".format(webpage['monitoring_url'], details),
                                  priority=0
                                  )
        else:
            log.error('ERROR ' + webpage['monitoring_url'] + ' (' + details + ')')
            send_pushover_message(userkey=os.environ['PUSHOVER_USER_KEY'],
                                  apikey=os.environ['PUSHOVER_API_KEY'],
                                  title='Website down',
                                  message="Website monitoring error for ({})\nDetails: {}".format(webpage['monitoring_url'], details),
                                  priority=1
                                  )


log.info('OITC Webpage Monitoring System version ' + VERSION + ' ended')
sys.exit()
