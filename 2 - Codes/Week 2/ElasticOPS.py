# -*- coding: utf-8 -*-
"""
Created on Wed May 31 12:49:59 2023

@author: Ahmed.Torky
"""

import openseespy.opensees as ops

import numpy as np
import matplotlib.pyplot as plt

# ------------------------------
# Start of model generation
# -----------------------------

# remove existing model
ops.wipe()

# set modelbuilder
ops.model('basic', '-ndm', 2, '-ndf', 2)

# create nodes
ops.node(1, 0.0, 0.0)
ops.node(2, 100.0,  0.0)
ops.node(3, 200.0,  0.0)
ops.node(4, 100.0, 100.0)

# set boundary condition
ops.fix(1, 1, 1)
ops.fix(2, 1, 1)
ops.fix(3, 1, 1)

# define materials
ops.uniaxialMaterial("Elastic", 1, 200000.0)

# define elements
ops.element("Truss",1,1,4,0.5,1)
ops.element("Truss",2,2,4,0.5,1)
ops.element("Truss",3,3,4,0.5,1)

ops.recorder('Node', '-file', 'DispNode1.out','-time', '-node', 1, '-dof', 1,2, 'disp')
ops.recorder('Node', '-file', 'RNode1.out','-time', '-node', 1, '-dof', 1,2, 'reaction')
ops.recorder('Element', '-file', 'GFBar1.out','-time', '-ele', 1, 'globalForce')
ops.recorder('Element', '-file', 'ForceBarSec1.out','-time', '-ele', 1, 'section', 1, 'force')
ops.recorder('Element', '-file', 'DispBar1.out','-time', '-ele', 1, 'deformations')

# create TimeSeries
ops.timeSeries("Linear", 1)

# create a plain load pattern
ops.pattern("Plain", 1, 1)

# Create the nodal load - command: load nodeID xForce yForce
ops.load(4, 0.0, -2.8)

# ------------------------------
# Start of analysis generation
# ------------------------------

# create SOE
ops.system("BandSPD")

# create DOF number
ops.numberer("RCM")

# create constraint handler
ops.constraints("Plain")

# create integrator
ops.integrator("LoadControl", 1.0)

# create algorithm
ops.algorithm("Linear")

# create analysis object
ops.analysis("Static")

# perform the analysis
ops.analyze(1)

# A = ops.printA()

ux = ops.nodeDisp(4,1)
uy = ops.nodeDisp(4,2)

F1 = ops.eleResponse( 1, 'globalForce')
Finternal1 = ops.basicForce( 1)
K1 = ops.basicStiffness( 1)
Disp1 = ops.eleResponse( 1, 'deformations')


print("ux:",ux)
print("uy:",uy)
print("F1:",F1)
print("Finternal1:",Finternal1)
print("Disp1:",Disp1)

# if abs(ux-0.53009277713228375450)<1e-12 and abs(uy+0.17789363846931768864)<1e-12:
#     print("Passed!")
# else:
#     print("Failed!")