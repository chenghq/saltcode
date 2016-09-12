# -*- coding: utf-8 -*-
import salt.utils.event

events = salt.utils.event.MasterEvent('/var/run/salt/master')

for event in events.iter_events(full=True):
    print event
    print ("===========================================")
