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
  ''' get the power consumption of this device for the given time range. range may be 10 or '''
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

if __name__ == "__main__":
  sid = fritzlogin.getSessionID('http://fritz.box','','')
  uri = "http://fritz.box/net/home_auto_query.lua"
  post_data = urllib.urlencode({'sid' : sid, 'command' : 'AllOutletStates', 'xhr' : 0 })
  print "req uri:",uri, post_data
  req = urllib2.urlopen(uri + '?' + post_data)
  data = req.read()
  print "data from autohome:"
  print req.info()
  print data
  #xml = parseString(data)
  #sid = xml.getElementsByTagName("SID").item(0).firstChild.data

  post_data = urllib.urlencode({'sid' : sid, 'command' : 'EnergyStats_10', 'id' : 16, 'xhr' : 0 })
  req = urllib2.urlopen(uri + '?' + post_data)
  data = req.read()
  print "data from autohome:"
  print req.info()
  print data
  data = json.loads(data)
  average = float(data["EnStats_average_value"])/100.0
  print "average:", average

  if not os.path.exists("fritz.rrd"):
    rrdtool.create("fritz.rrd", "--step", "600", "DS:power:GAUGE:900:0:150", 'RRA:AVERAGE:0.5:1:24',
                 'RRA:AVERAGE:0.5:6:10')
  rrdtool.update("fritz.rrd", "N:%f" % average)
