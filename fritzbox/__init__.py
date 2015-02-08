'''
  A package to access several FritzBox functions from the command line. 
  Tested with a 7390 and Fritz!OS 05.50
'''

from fritzglobals import readConfig
from fritzlogin import login, checkSession
from fritzautohome import getDevices, getConsumption, getTemperature, getLastConsumption, getPowerState, powerOn, powerOff
