#!/usr/bin/env python
import libView;
libView.doHeader();

tactics = {"pw":"Require password every 5 minutes",
           "newpw": "Require special password",
           "isolate": "Disconnect from internet",
           "encrypt": "Delete encryption keys",
           "delete": "Delete all data"
           }

triggers = {"timeout":"No activity for 10 minutes during time of heightened alert",
            "vote":"2 trusted friends send the code []",
            "mobile":"Activated by mobile-phone client"}

defcon = {
  '1':{'triggers':[],'tactics':[]},
  '2':{'triggers':[],'tactics':[]},
  '3':{'triggers':[],'tactics':[]},
  '4':{'triggers':[],'tactics':[]},
  '5':{'triggers':[],'tactics':[]}
}

print "<p>Current level is defcon 1</p>"

for level in defcon.keys():
  print "<h2>Level %s</h2>" % level
  print "<p>On trigger <select>"
  for tactic in tactics.keys():
    print "<option>%s</option>\n" % tactic
  print "</select></p>" 
  print "<p>Do action <select>"
  for trigger in triggers.keys():
    print "<option>%s</option>\n" % trigger
  print "</select></p>"      
      
print "<p>Note: each folder may have its own defcon-specific action, e.g. deleting a particular folder at certain defcon</p>"

libView.doFooter();
