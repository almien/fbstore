#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os

def baseDir():
  return("/var/fb/data")
  
def load(name):
  filename = baseDir() + "/" + name + ".json"
  data = {}
  if os.path.exists(filename):
    with open(filename, "r") as f:
      try:
        data = json.load(f)
      except ValueError:
        data = {}
  return(data)

def store(name, data):
  filename = baseDir() + "/" + name + ".json"
  f = open(filename, "w")
  if(f):
    json.dump(data, f)
    f.close()
    return(True)
  return(False)

