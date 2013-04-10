import urllib2, urllib, cookielib
from xml.dom.minidom import parseString
import hashlib

from fritzerror import FritzError
import fritzglobals as fg

def createResponse(challenge, password):
  text = "%s-%s" % (challenge, password)
  text = text.encode("utf-16le")
  res = "%s-%s" % (challenge, hashlib.md5(text).hexdigest())
  #print "md5: [%s]" % res
  return res

def login(username = None, password = None):
  url = fg.url
  if username: fg.username = username
  if password: fg.password = password
  sid = getSessionID(url,fg.username, fg.password)
  fg.SID = sid
  return sid

def getSessionID(baseuri, username, password):
  uri = baseuri + "/login_sid.lua"
  req = urllib2.urlopen(uri)
  data = req.read()
  if fg.DEBUG: print "data from checking sid:"
  if fg.DEBUG: print data
  xml = parseString(data)
  sid = xml.getElementsByTagName("SID").item(0).firstChild.data
  if fg.DEBUG: print "sid",sid
  if sid != "0000000000000000": return sid
  challenge = xml.getElementsByTagName("Challenge").item(0).firstChild.data
  if fg.DEBUG: print "challenge",challenge
  uri = baseuri + "/login_sid.lua"
  post_data = urllib.urlencode({'username' : username, 'response' : createResponse(challenge,password), 'page' : ''})
  if fg.DEBUG: print "req uri:",uri, post_data
  req = urllib2.urlopen(uri, post_data)
  data = req.read()
  if fg.DEBUG: print "data from login:"
  if fg.DEBUG: print req.info()
  if fg.DEBUG: print data
  xml = parseString(data)
  sid = xml.getElementsByTagName("SID").item(0).firstChild.data
  if fg.DEBUG: print "sid",sid
  if sid == "0000000000000000": raise FritzError("login to fritzbox failed")
  return sid

if __name__ == "__main__":
  print getSessionID("hallo","test")
  
