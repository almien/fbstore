#!/usr/bin/env python
import libView;
libView.doHeader();

services = [
  "twitter/identica",
  "email account",
  "email domain",
  "mobile phone camera uploader",
  "RSS/ATOM"
  ""]

print "<p>Add a service...</p>"

print "<p><form><select>"
for service in services:
  print "<option>%s</option>\n" % service
print "</select>"
print "<input type='submit' value='Add' />";
print "</form></p>"

print "<p>Services let you download data, such as your email, twitter messages, or RSS feeds from the regular internet to your FreedomBox</p>"

libView.doFooter();
