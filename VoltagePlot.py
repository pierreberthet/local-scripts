import numpy as np
import json
import matplotlib
#matplotlib.use('Agg')
import pylab as pl

# Plot the different figures for the merged voltages recordings.
# This file, as the MergeSpikefiles.py should be one level up than Test/..., the output of a simulation.

fparam = 'Test/Parameters/simulation_parameters.json'
f = open(fparam, 'r')
params = json.load(f)

params['figures_folder'] = "%sFigures/" % params['folder_name']
color = ['b','g', 'r', 'c', 'm', 'y', 'k']
z = 0
cl = color[z%len(color)]


cell_types_volt = ['d1', 'd2', 'actions']


# VOLTAGES
print 'VOLTAGES'
recorder_type = 'volt'
pl.figure(667)

fig = 0 

for cell in cell_types_volt:
    cl = 0
    pl.subplot(311+fig)
    for naction in xrange(params['n_actions']):
        data = np.loadtxt(params['spiketimes_folder']+str(naction)+cell+'_merged_'+recorder_type+'.dat' )
            
        pl.plot(data[:,1], data[:,2], c=cl)
        cl +=1
    print cell, fig
    fig += 1

pl.show()
