#!/usr/bin/env python
# -*- coding: utf-8 -*-

import libView;
from libView import toHtml;
import cgi

# option to enable error-reports to remote browser
import cgitb
cgitb.enable()

libView.doHeader("Encoding test")

form = cgi.FieldStorage()
text = form.getvalue("text", "sample text")


print "<h2>Type some text to display</h2>"
print "<form action='test_encoding.py' method='post'>"
libView.printf("<input type=text name=text value=\"%s\">", (toHtml(text),))
print "<input type=submit value='OK'>"
print "</form>"

print "<p>You typed <span style='border:1px solid green; margin:2px; padding:2px;background-color:#CFC'>%s</span></p>" % (toHtml(text),)

URL = "test_encoding.py?text=" + libView.toUrl(text)
print "<p>URL would be %s <a href='%s'>Test</a></p>" % (URL, URL,)


libView.doFooter();

