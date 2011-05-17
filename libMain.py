#!/usr/bin/env python

def get(name):
  basicSettings = {
    "owner":"deviceOwner",
    "product":"freedomBoxStore",
    "productURL":"http://somefblink.example.com"}
  if(name in basicSettings.keys()):
    return(basicSettings[name])
  return("")

