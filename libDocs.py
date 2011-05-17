#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import libView;
from libView import toHtml, toUrl;
import os
import json

def validPath(path):
  return(re.match("^[A-Za-z0-9/]+$", path) != None and path[0] == "/")

def basePath():
  return("/var/fb/docs")
  
def getMeta(path):
  data = {}
  if(validPath(path)):
    filename = basePath() + "/" + "meta.json"
    if os.path.exists(filename):
      with open(filename, "r") as f:
        try:
          data = json.load(f)
        except ValueError:
          data = {}
  return(data)

def storeMeta(path, data):
  if(validPath(path)):
    filename = basePath() + "/" + "meta.json"
    f = open(filename, "w")
    if(f):
      json.dump(data, f)
      f.close()
      return(True)
  return(False)



def folderHeader():
  print "<p><a href='addmodule.py></a></p>"

def showFile(filename):
  print "Is a file"

def showFolder(path, fullPath):
  libView.doHeader("Documents: " + path)
  
  folderHeader()

  if(not os.path.exists(fullPath)):
    print "<p>Invalid path</p>"
  else:
    files = os.listdir(fullPath)
    for f in files:
      ff = os.path.join(fullPath, f)
      if(os.path.isdir(ff)):      
        libView.printf( "<p>Subdir: <a href=\"docs.py?path=%s%s/\">%s</a></p>", (toUrl(path), toUrl(f),toHtml(f),))

    for f in files:
      if(f != "meta.json"):
        ff = os.path.join(fullPath, f)
        if(not os.path.isdir(ff)):      
          libView.printf( "<p>File: <a href=\"docs.py?path=%s%s\">%s</a></p>", (toUrl(path), toUrl(f),toHtml(f),))

  meta = getMeta(path)
  meta["count"] = meta.get("count",0) + 1
  storeMeta(path, meta)
  
  libView.printf("<p>Folder has %d views</p>", meta["count"])
  if(1):
    print "<h2>Upload</h2>"
    print "<form action=\"docs.py\" enctype=\"multipart/form-data\" method=\"post\">"
    libView.printf("<input type=\"file\" name=\"uploaded_file\" max_size=\"%s\">", (80 * 1024*1024,))
    print "<input type=\"hidden\" name=\"action\" value=\"upload\">"
    libView.printf("<input type=\"hidden\" name=\"path\" value=\"%s\">", (toHtml(path),))
    if(0): # option to require mime-type declaration on upload (otherwise just ask user-agent)
      filetypes = ("text/plain", "image/jpeg", "image/png", "application/pdf")
      print "<select>"
      for filetype in filetypes:
        libView.printf("<option name=\"%s\">%s</option>", (toHtml(filetype), toHtml(filetype),))
      print "</select> "
    print "<input type=\"submit\" value=\"Upload\">"
    print "</form>"
  
  libView.doFooter();

