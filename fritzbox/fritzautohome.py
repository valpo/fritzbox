import urllib2, urllib, cookielib
from xml.dom.minidom import parseString
import json
import rrdtool
import os.path

from fritzerror import FritzError
import fritzglobals as fg
import fritzlogin

def getDevices():
  ''' returns a list of tuples (deviceid, connectstate, switchstate) '''
  baseurl = fg.url
  url = baseurl + "/net/home_auto_query.lua"
  post_data = urllib.urlencode({'sid' : fg.SID, 'command' : 'AllOutletStates', 'xhr' : 0 })
  req = urllib2.urlopen(url + '?' + post_data)
  data = req.read()
  if fg.DEBUG:
    print "data from autohome:"
    print req.info()
    print data
  data = json.loads(data)
  count = int(data["Outlet_count"])
  res = []
  for i in range(1,count+1):
    device = (int(data["DeviceID_%d" % i]), int(data["DeviceConnectState_%d" % i]), int(data["DeviceSwitchState_%d" % i]))
    res.append(device)
  return res

def getConsumption(deviceid, timerange = "10"):
  ''' get the average power consumption of this device for the given time range. range may be 10, 24h, month or year'''
  tranges = ("10","24h","month","year")
  if timerange not in tranges: raise FritzError("unknown timerange, possible values are: %s" % str(tranges))
  baseurl = fg.url + "/net/home_auto_query.lua"
  post_data = urllib.urlencode({'sid' : fg.SID, 'command' : 'EnergyStats_%s' % timerange, 'id' : deviceid, 'xhr' : 0 })
  req = urllib2.urlopen(baseurl + '?' + post_data)
  data = req.read()
  if fg.DEBUG:
    print "data from power consumption:"
    print req.info()
    print data
  data = json.loads(data)
  average = float(data["EnStats_average_value"])/100.0
  if fg.DEBUG: print "average:", average
  return average

def getLastConsumption(deviceid):
  ''' get the last known (latest) power consumption of this device '''
  baseurl = fg.url + "/net/home_auto_query.lua"
  post_data = urllib.urlencode({'sid' : fg.SID, 'command' : 'EnergyStats_10', 'id' : deviceid, 'xhr' : 0 })
  req = urllib2.urlopen(baseurl + '?' + post_data)
  data = req.read()
  if fg.DEBUG:
    print "data from power consumption:"
    print req.info()
    print data
  data = json.loads(data)
  latest = float(data["EnStats_watt_value_1"])/100.0
  if fg.DEBUG: print "latest:", latest
  return latest

def getPowerState(deviceid):
  ''' returns either 0 (power off) or 1 (power on) '''
  baseurl = fg.url + "/net/home_auto_query.lua"
  post_data = urllib.urlencode({'sid' : fg.SID, 'command' : 'AllOutletStates', 'id' : deviceid, 'xhr' : 1 })
  req = urllib2.urlopen(baseurl + '?' + post_data)
  data = req.read()
  if fg.DEBUG:
    print "data from powerstates:"
    print req.info()
    print data
  data = json.loads(data)
  switchState = int(data["DeviceSwitchState_1"])
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
