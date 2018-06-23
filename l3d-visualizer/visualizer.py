
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) Vispy Development Team. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------

"""
This example demonstrates how to create a sphere.
"""

import sys

from vispy import scene
from vispy.visuals.transforms import STTransform

canvas = scene.SceneCanvas(keys='interactive', bgcolor='white',
                           size=(800, 600), show=True)

view = canvas.central_widget.add_view()
view.camera = 'arcball'

spheres = scene.Node(parent=view.scene)
for x in range(100):
    scene.visuals.Cube(size=1,parent=spheres,edge_color='#ff00ff', color = '#ff0000')
'''
index = 0
for x in range(10):
    for y in range(10):
        for z in range(10):
            if(y%2==0):
                if x%2==0:
                    spheres[index]=  STTransform(translate=[x, z, y])
                    #newlist[index,0] = ((x*10)+z+(y*100));
                else:
                    spheres[index]=  STTransform(translate=[x, 9-z, y])
                    #newlist[index,0] = ((x*10)+9-z+(y*100));
            else:

                if x%2==0:
                    spheres[index]=  STTransform(translate=[9-x, 9-z, y])
                    #newlist[index,0] = ((90-(x*10))+9-z+(y*100));
                else:
                    spheres[index]=  STTransform(translate=[9-x, z, y])
                    #newlist[index,0] = ((90-(x*10))+z+(y*100));#sphere1.transform = STTransform(translate=[-2.5, 0, 0])
            index = index+1
#sphere3.transform = STTransform(translate=[2.5, 0, 0])
'''

'''
def update(ev):
    global pos, color, line
    pos[:, 1] = np.random.normal(size=N)
    color = np.roll(color, 1, axis=0)
    line.set_data(pos=pos, color=color)

timer = app.Timer()
timer.connect(update)
timer.start(0)
'''
if __name__ == '__main__' and sys.flags.interactive == 0:
    canvas.app.run()
