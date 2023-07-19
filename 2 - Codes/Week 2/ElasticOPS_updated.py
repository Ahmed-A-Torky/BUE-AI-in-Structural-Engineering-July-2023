# -*- coding: utf-8 -*-
"""
Created on Wed May 31 12:49:59 2023
@author: Ahmed.Torky
"""

import openseespy.opensees as ops

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

list_areas = [0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 10.0, 100.0]

df = pd.DataFrame(columns=['Idx','Area','F1','F2','F3','F4','F5','ux4'])

# ------------------------------
# Start of loop
# -----------------------------
idx = 0
for a in list_areas:
    print("###############################")
    print("   Run with Area:",str(a))
    print("###############################")
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
    
    E1 = 200000.0
    E2 = 300000.0
    
    # define materials
    ops.uniaxialMaterial("Elastic", 1, E1)
    ops.uniaxialMaterial("Elastic", 2, E2)
    
    Area1 = 0.5
    Area2 = a
    
    # define elements
    ops.element("Truss",1,1,4,Area2,1)
    ops.element("Truss",2,2,4,Area1,1)
    ops.element("Truss",3,3,4,Area2,1)
    ops.element("Truss",4,1,2,Area2,1)
    ops.element("Truss",5,2,3,Area2,1)
    
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
    ops.load(4, 10.0, -2.8)
    
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
    F2 = ops.eleResponse( 2, 'globalForce')
    F3 = ops.eleResponse( 3, 'globalForce')
    F4 = ops.eleResponse( 4, 'globalForce')
    F5 = ops.eleResponse( 5, 'globalForce')
    Finternal1 = ops.basicForce( 1)
    K1 = ops.basicStiffness( 1)
    Disp1 = ops.eleResponse( 1, 'deformations')
    
    # Get results and add to dataframe
    list = [idx,a,F1[1],F2[1],F3[1],F4[1],F5[1], ux]
    df.loc[len(df)] = list
    
    print("ux:",ux)
    # print("uy:",uy)
    print("F1:",F1[0])
    # print("F3:",F3)
    print("DELTA:",F3[0]-F1[0])
    # print("Finternal1:",Finternal1)
    # print("Disp1:",Disp1)
    idx = idx + 1


# Plot my results
# fig, ax = plt.subplot()
df.plot(x="Area", y=["F1","F2","F3"])
# df.plot(x="Idx", y="F2")
# df.plot(x="Idx", y="F3")
plt.show()