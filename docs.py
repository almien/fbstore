#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgitb
cgitb.enable()

import libView
from libView import toHtml
import libDocs
import cgi
import os

form = cgi.FieldStorage()
path = form.getvalue("path", "/")
fullPath = libDocs.basePath() + path

if(not libDocs.validPath(path)):
  #---------------------------------------------------------
  # Invalid location
  #---------------------------------------------------------
  libView.doHeader("Documents")
  print "<p>Invalid path</p>"
  libView.doFooter();
elif(not path.endswith("/")):
  #---------------------------------------------------------
  # Displaying a file
  #---------------------------------------------------------
  libDocs.showFile(fullPath)
else:
  #---------------------------------------------------------
  # Displaying a folder
  #---------------------------------------------------------
  if(form.has_key("uploaded_file")):
    #---------------------------------------------------------
    # Upload
    #---------------------------------------------------------
    fileitem = form["uploaded_file"]
    libView.doHeader("Uploaded file")
    #print str(fileitem)
    #print toHtml(str(dir(fileitem)))
    if fileitem.file:
      filename = fileitem.filename
      contentType = fileitem.headers.get("Content-Type", "") 
      # according to wikipedia, is best to leave content-type unspecified if not known 
      # rather than guessing "application/octet-stream", since then we allow the recipient to guess the type
      libView.printf("<p>Uploaded %s of type %s</p>", (toHtml(filename), toHtml(contentType),))

      import hashlib
      h = hashlib.new("sha256")
      h.update(fileitem.filename)
      fileTitle = h.hexdigest()
      
      meta = libDocs.getMeta(path)
      file_list = meta.get("files", {})
      fileVersion = 1
      originalTitle = fileTitle
      while(fileTitle in file_list):
        fileVersion += 1
        fileTitle = originalTitle + "_%03d" % fileVersion
      
      file_list[fileTitle] = {"name":filename, "type":contentType}
      meta["files"] = file_list
      libDocs.storeMeta(path, meta)
      
      fileFullPath = libDocs.basePath() + os.path.join(path, fileTitle)
      print "<p>Storing in %s</p>" % toHtml(fileFullPath)
      if(1):
        fp = open(fileFullPath, "wb")
        if(fp):
          for line in fileitem.file.read():
            fp.write(line)
          fp.close()
      

    libView.doFooter()
  else:
    #---------------------------------------------------------
    # View folder
    #---------------------------------------------------------
    libDocs.showFolder(path, fullPath)

