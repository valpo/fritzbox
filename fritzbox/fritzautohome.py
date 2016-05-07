import urllib2, urllib, cookielib
from xml.dom.minidom import parseString
import json
import os.path

from fritzerror import FritzError
import fritzglobals as fg
import fritzlogin

def getDevices():
  ''' returns a list of tuples (deviceid, connectstate, switchstate) '''
  baseurl = fg.url
  url = baseurl + "/webservices/homeautoswitch.lua"
  post_data = urllib.urlencode({'sid' : fg.SID, 'switchcmd' : 'getswitchlist' })
  req = urllib2.urlopen(url + '?' + post_data)
  data = req.read()
  if fg.DEBUG:
    print "data from autohome:"
    print req.info()
    print data
  data = data.strip().split(",")
  return data

def getTemperature(deviceid):
  ''' get the temperature of this device in celsius '''
  baseurl = fg.url + "/webservices/homeautoswitch.lua"
  post_data = urllib.urlencode({'sid' : fg.SID, 'switchcmd' : 'gettemperature', 'ain' : deviceid })
  req = urllib2.urlopen(baseurl + '?' + post_data)
  data = req.read()
  if fg.DEBUG:
    print "data from temperature:"
    print req.info()
    print data
  data = float(data.strip())/10.0
  if fg.DEBUG:
    print data
  return data

def getConsumption(deviceid):
  ''' get the current power consumption of this device '''
  baseurl = fg.url + "/webservices/homeautoswitch.lua"
  post_data = urllib.urlencode({'sid' : fg.SID, 'switchcmd' : 'getswitchpower', 'ain' : deviceid })
  req = urllib2.urlopen(baseurl + '?' + post_data)
  data = req.read()
  if fg.DEBUG:
    print "data from power consumption:"
    print req.info()
    print data
  data = float(data.strip())/1000.0
  if fg.DEBUG: print "average:", data
  return data

def getLastConsumption(deviceid):
  ''' get the last known (latest) power consumption of this device '''
  return getConsumption(deviceid)

def getPowerState(deviceid):
  ''' returns either 0 (power off) or 1 (power on) '''
  baseurl = fg.url + "/net/home_auto_query.lua"
  post_data = urllib.urlencode({'sid' : fg.SID, 'command' : 'OutletStates', 'id' : deviceid, 'xhr' : 1 })
  req = urllib2.urlopen(baseurl + '?' + post_data)
  data = req.read()
  if fg.DEBUG:
    print "data from powerstates:"
    print req.info()
    print data
  data = json.loads(data)
  switchState = int(data["DeviceSwitchState"])
  if fg.DEBUG: print "state:", switchState
  return switchState

def setPowerState(deviceid, value):
  baseurl = fg.url + "/net/home_auto_query.lua"
  post_data = urllib.urlencode({'sid' : fg.SID, 'command' : 'SwitchOnOff', 'id' : deviceid, 'value_to_set' : value, 'xhr' : 1 })
  req = urllib2.urlopen(baseurl, post_data)
  data = req.read()
  if fg.DEBUG:
    print "data from powerstates:"
    print req.info()
    print data
  data = json.loads(data)
  res = int(data["RequestResult"])
  if fg.DEBUG: print "result:", res
  return res

def powerOn(deviceid):
  ''' power on the device '''
  setPowerState(deviceid, 1)
  
def powerOff(deviceid):
  ''' power off the device '''
  setPowerState(deviceid, 0)
  

if __name__ == "__main__":
  pass
