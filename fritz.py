import fritzbox as fb
from time import sleep
import os

def updateRrrd(powerconsumption):
  try: 
    import rrdtool
    if not os.path.exists("fritz.rrd"):
      rrdtool.create("fritz.rrd", "--step", "300", "DS:power:GAUGE:900:0:150", 'RRA:AVERAGE:0.5:12:3600', 'RRA:AVERAGE:0.5:288:3600', 'RRA:AVERAGE:0.5:1:3600')
    rrdtool.update("fritz.rrd", "N:%f" % powerconsumption)
  except: raise

def main():
  fb.readConfig("/home/mathias/.fritzboxpyrc")
  fb.fritzglobals.DEBUG = 0 # set this to 1 to see verbose output (may include passwords!)
  fb.login() # initialize session
  fb.fritzglobals.DEBUG = 1
  devices = fb.getDevices() # get a list of all devices known by the box
  for devid in devices:
    print "checking device",devid
    powerconsumption = fb.getConsumption(devid)
    print "current consumption:",powerconsumption
    temp = fb.getTemperature(devid)
    print "current temperatur:",temp
    state = fb.getPowerState(devid)
    print "current state:",state
    print "sleeping a bit..."
    sleep(21*60)
    state = fb.getPowerState(devid)
    print "current state:",state
    powerconsumption = fb.getConsumption(devid)
    print "current consumption:",powerconsumption
    continue
    # be carefull here....
    fb.powerOff(devid)
    state = fb.getPowerState(devid)
    print "current state:",state
    fb.powerOn(devid)
    state = fb.getPowerState(devid)
    print "current state:",state

  #updateRrrd(powerconsumption)
  

if __name__ == "__main__":
  main()
