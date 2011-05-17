#!/usr/bin/env python
# -*- coding: utf-8 -*-

import libUser
import libMain
import cgi
import urllib;

def defconColour():
  return("#CCFFCC")

def toHtml(text):
  s1 = cgi.escape(text, True)
  s2 = s1.encode('utf-8', 'xmlcharrefreplace')
  return(s2)

def toUrl(text):
  return(urllib.quote(text))

def printf(format, data):
  print format % data

def userBox():
  owner = libMain.get("owner")
  product = libMain.get("product")
  print "<div class='user' style='background-color:"+defconColour()+"'>"
  print "<div><i>"+toHtml(owner)+"</i>'s "+toHtml(product)+"</div>"
  print "<div>User [unknown] <a href='#'>Logout</a></div>"
  print "<div>Defcon <a href='admin.py'>5</a></div>"
  print "<div><a href='#'>Activity</a></div>"
  print "</div>"

def infoBox(noteType, text):
  print "<div class=infobox>" + toHtml(noteType) + ": " + toHtml(text) + "</div>" 

def error(text):
  print "<div class=error>" + toHtml(text) + "</div>" 
  
def doHeader(title):
  user = libUser.getUser()
  owner = libMain.get("owner")
  product = libMain.get("product")
  urlLogout = libUser.getUrlLogout()
  print "Content-type: text/html; charset=UTF-8\n\n"
  print "<html><head><title>" + toHtml(title) + " - "+ toHtml(owner) + "'s "+toHtml(product)+"</title>"
  print 
  print "<link rel=\"stylesheet\" href=\"/media/styles.css\" type=\"text/css\" />"
  print "</head><body>";
  userBox();
  print "<h1>"+title+"</h1>"

def doFooter():
  print "<div class=\"footer\">"
  print toHtml(libMain.get("product")) + " &bull; "
  print "<a href=\"/cgi-bin/index.py\">Home</a> &bull;";
  print "<a href=\"/help/\">Help</a> &bull;";
  print "<a href=\"%s\">About</a> &bull;" % (libMain.get("productURL"),)
  print "</div>";
  print "</body></html>\n"

