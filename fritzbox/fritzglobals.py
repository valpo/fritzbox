import sys
import ConfigParser

SID = None
url = "http://fritz.box"
username = ''
password = None
DEBUG = 0

def readConfig(fname):
  cfg = ConfigParser.ConfigParser()
  cfg.read(fname)
  for key, val in cfg.items("global"):
    setattr(sys.modules['fritzbox.fritzglobals'], key,val)

