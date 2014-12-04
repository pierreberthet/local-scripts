import numpy as np
import json
import matplotlib
#matplotlib.use('Agg')
import pylab as pl
import pprint as pp
# Plot the different figures for the merged spikes and voltages recordings.
# This file, as the MergeSpikefiles.py should be one level up than Test/..., the output of a simulation.

fparam = 'Test/Parameters/simulation_parameters.json'
f = open(fparam, 'r')
params = json.load(f)

pp.pprint(params)


params['figures_folder'] = "%sFigures" % params['folder_name']
color = ['b','g', 'r', 'c', 'm', 'y', 'k']
z = 6
cl = color[z%len(color)]

xa = -(params['t_sim']/10)
size = 5.

print 'SPIKES'
ymax = 0. 
pl.figure(666)
recorder_type = 'spikes'
mean = 0

#cell = ['states', 'rp', 'rew', 'd1', 'd2', 'efference', 'actions', 'brainstem' ]

#cell = 'states'
#
#
#for nstate in range(params['n_states']):
#    #    print nstate
#    data = np.loadtxt(params['spiketimes_folder']+'/'+str(nstate)+cell+'_merged_'+recorder_type+'.dat' )
#    mean += (np.min(data[:,0])+np.max(data[:,0]))/2
#    if np.max(data[:,0]) > ymax:
#        ymax = np.max(data[:,0])
#    pl.scatter(data[:,1], data[:,0], c=cl, s=size, marker="|")
#mean = mean/params['n_states']
#pl.text(xa, mean, cell, color=cl)
#
#z += 1
#cl = color[z%len(color)]
#cell = 'rp'
#for ni in range(params['n_states']*params['n_actions']):
#    #    print nstate
#    data = np.loadtxt(params['spiketimes_folder']+str(ni)+cell+'_merged_'+recorder_type+'.dat' )
#    if len(data)<=2:
#       print 'no data in ', cell, ni 
#    else:
#        mean += (np.min(data[:,0])+np.max(data[:,0]))/2
#        if np.max(data[:,0]) > ymax:
#            ymax = np.max(data[:,0])
#        pl.scatter(data[:,1], data[:,0], c=cl, s=size, marker="|")
#
#mean = mean/(params['n_states']*params['n_actions'])
#pl.text(xa, mean, cell, color=cl)
#mean = 0
#z += 1
#cl = color[z%len(color)]


cell = 'rew'
data = np.loadtxt(params['spiketimes_folder']+cell+'_merged_'+recorder_type+'.dat' )
if len(data)<2:
    print 'no data in ', cell
else:
    pl.scatter(data[:,1], data[:,0], c=cl, s=size,label=cell, marker="|")
    mean += (np.min(data[:,0])+np.max(data[:,0]))/2
    if np.max(data[:,0]) > ymax:
        ymax = np.max(data[:,0])
    #pl.text(xa, mean, cell, color=cl)
    mean = 0
   # z += 1
   # cl = color[z%len(color)]



#cell_types = ['d1', 'd2', 'actions','efference', 'brainstem']
#
## SPIKES
#for cell in cell_types:
#    for naction in range(params['n_actions']):
#        data = np.loadtxt(params['spiketimes_folder']+str(naction)+cell+'_merged_'+recorder_type+'.dat' )
#        if len(data)<2:
#            print 'no data in', cell, naction
#        else:
#            if naction ==0:
#                pl.scatter(data[:,1], data[:,0], c=cl, s=size, label=cell, marker="|")
#            else:
#                pl.scatter(data[:,1], data[:,0], c=cl, s=size, marker="|")
#            mean += (np.min(data[:,0])+np.max(data[:,0]))/2
#            if np.max(data[:,0]) > ymax:
#                ymax = np.max(data[:,0])
#    mean = mean/params['n_actions']
#    pl.text(xa,mean, cell, color=cl)
#    z += 1
#    cl = color[z%len(color)]
#    mean = 0
#pl.ylim(0, ymax)
#lines= np.arange(params['t_init'],params['t_sim'], params['t_iteration'])
#pl.vlines(lines, [0], ymax,  color='0.55', linestyles='dashed')
#pl.title(str(params['n_states'])+' states '+str(params['n_actions'])+' actions '+str(params['n_blocks']*params['block_len'])+ ' trials' )
pl.ylabel('dopaminergic neurons')
pl.xlabel("time")
#pl.legend()
pl.tight_layout()
#pl.subplots_adjust(left = .04, bottom=.04, right=.97, top=.97)




spread = 5
x = params['n_recordings'] * spread 
tempd =np.sort(data[:,1])

distrib = np.histogram(tempd, x)[0]
#distrib = np.hist(tempd, x)[0]
#distrib = np.histogram(data[:,1], x)[0]

#distrib = distrib[0] / float(np.sum(distrib[0]))
#distrib = distrib - np.mean(distrib)


adapt = np.max(distrib)

pl.figure(321)
#routcome = np.zeros(x)
#for i in xrange(len(outcome)):
#    routcome[spread*i:spread*i+spread] = outcome[i] * adapt

y=np.mean(distrib)
#pl.title('dopamine dynamic')
#pl.plot(routcome)
#pl.plot(distrib, c='k')
pl.hist(tempd, x, color=[cl])
pl.tight_layout()
#pl.fill_between(np.arange(x), distrib, y, where=distrib>=y, facecolor='green', interpolate=True)
#pl.fill_between(np.arange(x), distrib, y, where=distrib<=y, facecolor='red', interpolate=True)
pl.show()

