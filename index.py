#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgitb
cgitb.enable()

import libMain
import libView;
libView.doHeader(libMain.get("product"))

print "<p><a href=\"docs.py?path=/\">Documents</a></p>"
print "<p><a href=\"links.py\">Bookmarks</a></p>"

libView.doFooter();
