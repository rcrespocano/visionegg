#!/usr/bin/env python
"""quit_server.py -- Use this to quit cal_server."""

from VisionEgg.PyroHelpers import *
from VisionEgg.Core import *

# Get the controllers

client = PyroClient()

quit_controller = client.get('quit_controller')
quit_controller.set_during_go_value(1)
quit_controller.set_between_go_value(1)
quit_controller.evaluate_now()