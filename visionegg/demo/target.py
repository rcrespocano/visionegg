#!/usr/bin/env python

from VisionEgg.Core import *
from VisionEgg.AppHelper import *
from VisionEgg.MoreStimuli import *

velocity = 10.0

def x_as_function_of_time(t):
    return velocity*sin(0.1*2.0*math.pi*t)

def y_as_function_of_time(t):
    return velocity*sin(0.1*2.0*math.pi*t)

def orientation(dummy):
    return 135.0

def on_during_experiment(t):
    if t < 0.0:
        return 0
    else:
        return 1
    
screen = get_default_screen()
projection = SimplePerspectiveProjection(fov_x=45.0)
viewport = Viewport(screen,(0,0),screen.size,projection)
target = Target2D()
target.init_gl()
viewport.add_overlay(target)
p = Presentation(duration_sec=10.0,viewports=[viewport])
p.add_realtime_controller(target.parameters,'x', x_as_function_of_time)
p.add_realtime_controller(target.parameters,'y', y_as_function_of_time)
p.add_transitional_controller(target.parameters,'orientation', orientation)
p.add_transitional_controller(target.parameters,'on', on_during_experiment)
p.go()


