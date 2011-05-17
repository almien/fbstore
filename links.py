#!/usr/bin/env python
# -*- coding: utf-8 -*-
import libView;
from libView import toHtml;
import cgi
import libData;
import re

# option to enable error-reports to remote browser
import cgitb
cgitb.enable()


form = cgi.FieldStorage()

libView.doHeader("Bookmarks")

bookmarks = libData.load("bookmarks")

accounts = bookmarks.get("accounts", {})

action = form.getvalue("action", "")

if(action == "add"):
  print "<h2>Import from another website</h2>"
  print "<form action=\"links.py\" method=\"post\">Import bookmarks from "
  print "<input type=\"hidden\" name=\"action\" value=\"import_webservice\" />"
  print "<select>"
  print "<option selected name=delicious>del.icio.us</option>"
  print "</select> "
  print "username <input type=text name=site_ac>"
  print "password <input type=password name=site_pw>"
  print "<input type=submit value=\"OK\">"
  print "</form>"
  libView.infoBox("Note", "This only works with original-style delicious accounts, not the &quot;oauth&quot; ones that yahoo users have")

  print "<h2>Upload your browser&apos;s bookmarks</h2>"
  print "<form action=\"links.py\" enctype=\"multipart/form-data\" method=\"post\">Upload "
  print "<input type=\"hidden\" name=\"action\" value=\"upload\" />"
  print "<input type=\"hidden\" name=\"MAX_FILE_SIZE\" value=\"%d\" />" % (20 * 1024 * 1024,)
  print "<select>"
  print "<option selected name=firefox>Firefox's bookmarks.html</option>"
  print "</select> "
  print "<input type=file name=bookmarks_file>"
  print "<input type=submit value=\"OK\">"
  print "</form>"
  
  print "<h2>Create new blank area for bookmarks storage</h2>"
  print "<form action=\"links.py\" method=\"post\">"
  print "<input type=\"hidden\" name=\"action\" value=\"new_blank\" />"
  print "Name for this set: <input type=text name=ac_name>"
  print "<input type=submit value=\"OK\">"
  print "</form>"
  libView.infoBox("Note", "plain text only, no special-characters")  
  
  print "<p><a href=\"links.py\">Back to bookmarks index</a></p>"
  
elif(action == "new_blank"):
  name = form.getvalue("ac_name", "")
  name_max_chars = 80
  if(name == ""):
    libView.error("Need to specify a name for the new set of bookmarks")
  elif(len(name) > name_max_chars):
    libView.error("Name too long (max %d chars)" % (name_max_chars,))
  elif(re.search("^[A-Z0-9a-z_]+$", name) == None):
    libView.error("Sorry that name isn't currently allowed, due to security concerns handling the characters")
  elif(name in accounts.keys()):
    libView.error("Name already exists")
  else:
    accounts[name] = {"public":False, "bookmarks_type":"Local", "bookmarks":[]}
    bookmarks["accounts"] = accounts
    libData.store("bookmarks", bookmarks)
    print "<p>Created OK. <a href=\"links.py\">Back to bookmarks index</a></p>"

elif(action == "import_webservice"):
  import urllib
  site_ac = form.getvalue("site_ac", "")
  site_pw = form.getvalue("site_pw", "")  
  if(site_ac == "" or site_pw == ""):
    libView.error("Need to specify account name and password for the site")
  else:
    url = "https://%s:%s@api.del.icio.us/v1/posts/all" % (urllib.quote(site_ac), urllib.quote(site_pw),)
    f = urllib.urlopen(url)
    if(f):
      import xml.sax
      class DeliciousReader (xml.sax.ContentHandler):
        def __init__(self):
          self.posts = []
        def startElement(self, name, attrs):
          if(name == "post"):
            self.posts.append({
              "url": attrs.get("href", "#"),
              "name": attrs.get("description", "untitled"), 
              "tags": attrs.get("tag", "").split(" ")})
      reader = DeliciousReader()
      parser = xml.sax.make_parser()
      parser.setContentHandler(reader)
      parser.parse(f)
      
      name = "delicious"
      accounts[name] = {"public":False, "bookmarks_type":"Delicious", "bookmarks":reader.posts}
      bookmarks["accounts"] = accounts
      libData.store("bookmarks", bookmarks)
      print "<p>Created OK. <a href=\"links.py\">Back to bookmarks index</a></p>"

elif(action == "upload"):
  libView.error("unsupported")
else:
  # Viewing, not editing:

  account_name = form.getvalue("ac", "")
  tag_filter = form.getvalue("tag", "")
  if(account_name != ""):
    if(not account_name in accounts.keys()):
      libView.error("No such account")
    else:
      bookmarks = accounts[account_name].get("bookmarks", [])
      if(len(bookmarks) == 0):
        print "<p>No bookmarks in this account yet</p>"
      else:
        count = 0
        print "<ul>"
        for bookmark in bookmarks:
          tags = bookmark.get("tags", [])
          if(tag_filter == "" or tag_filter in tags):
            count += 1
            tags_text = ""
            if(len(tags) != 0):
              for tag in tags:
                tags_text += " <a href=\"links.py?ac=%s&amp;tag=%s\">%s</a>" %( toHtml(account_name), toHtml(tag), toHtml(tag),)
              tags_text = " [in" + tags_text + "]";
            libView.printf("<li><a href=\"%s\">%s</a>%s</li>", (
              toHtml(bookmark.get("url","")), 
              toHtml(bookmark.get("name","untitled")), 
              tags_text, ))
        if(count == 0):
          print "<li>No bookmarks matching filter</li>"
        print "</ul>"
    
  else:
    if(len(accounts.keys()) == 0):
      print "<p>No bookmark accounts have been setup</p>"
    else:
      for name, ac in accounts.items():
        print "<p><a href=\"links.py?ac=%s\">%s</a></p>" % (name,name,)
    print "<p><a href=\"links.py?action=add\">Add a new bookmarks account</a></p>"

libView.doFooter();

