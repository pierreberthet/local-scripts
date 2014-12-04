import numpy as np
import json
import matplotlib
#matplotlib.use('Agg')
import pylab as pl

# Plot the different figures for the merged spikes and voltages recordings.
# This file, as the MergeSpikefiles.py should be one level up than Test/..., the output of a simulation.

fparam = 'Test/Parameters/simulation_parameters.json'
f = open(fparam, 'r')
params = json.load(f)


def extract_trace(d, gid):
    """ 
    d : voltage trace from a saved with compatible_output=False
    gid : cell_gid
    """
    mask = gid * np.ones(d[:, 0].size)
    indices = mask == d[:, 0]
    time_axis, volt = d[indices, 1], d[indices, 2]
    return time_axis, volt



#cells = ['d1', 'd2']
#recorder_type = 'volt'
#for cell in cells:
#    for naction in xrange(params['n_actions']):
#        data = np.loadtxt(params['spiketimes_folder']+str(naction)+cell+'_merged_'+recorder_type+'.dat')
#        gids = np.unique(data[:,0])
#        for gid in ngids:
#            time_axis, volt = extract_trace(data, gid)
#            pl.plot(time_axis, volt, label=gid, lw=2)

cells= ['d1','d2']
recorder_type = 'volt'
nfig =0

for cell in cells:
    sub=100*params['n_actions']+11
    fig = pl.figure(nfig)
    for naction in xrange(params['n_actions']):
        fig.add_subplot(sub+naction)
        data = np.loadtxt(params['spiketimes_folder']+str(naction)+cell+'_merged_'+recorder_type+'.dat')
        gids = np.unique(data[:,0])
        for gid in gids:
            d = data[data[:,0]==gid, 1:]
            pl.plot( d[d[:,0].argsort(),1], label=str(int(gid)), lw=2)

    nfig+=1
    pl.title(cell)
pl.show()





#params['figures_folder'] = "%sFigures/" % params['folder_name']
#color = ['b','g', 'r', 'c', 'm', 'y', 'k']
#z = 0
#cl = color[z%len(color)]
#
#xa = -(params['t_sim']/10)
#size = 5.
#
#print 'SPIKES'
#ymax = params['n_actions']*params['num_brainstem_neurons'] + np.max(np.loadtxt(params['spiketimes_folder']+str(params['n_states']-1)+'states_merged_spikes.dat' )[:,0])
#pl.figure(666)
#lines= np.arange(0,params['t_sim'], params['t_iteration'])
#pl.vlines(lines, [0], ymax,  color='0.55', linestyles='dashed')
#pl.title(str(params['n_states'])+' states '+str(params['n_actions'])+' actions '+str(params['n_blocks']*params['block_len'])+ ' trials' )
#pl.ylabel("cell GID")
#pl.xlabel("time "+ r"$ms$")
#pl.ylim(0, ymax)
#
#cell = 'states'
#recorder_type = 'spikes'
#
#mean = 0
#
#for nstate in range(params['n_states']):
#    #    print nstate
#    data = np.loadtxt(params['spiketimes_folder']+'/'+str(nstate)+cell+'_merged_'+recorder_type+'.dat' )
#    mean += (np.min(data[:,0])+np.max(data[:,0]))/2
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
#    if len(data)<2:
#       print 'no data in ', cell, ni 
#    else:
#        mean += (np.min(data[:,0])+np.max(data[:,0]))/2
#        pl.scatter(data[:,1], data[:,0], c=cl, s=size, marker="|")
#
#mean = mean/(params['n_states']*params['n_actions'])
#pl.text(xa, mean, cell, color=cl)
#mean = 0
#z += 1
#cl = color[z%len(color)]
#
#
#cell = 'rew'
#data = np.loadtxt(params['spiketimes_folder']+cell+'_merged_'+recorder_type+'.dat' )
#if len(data)<2:
#    print 'no data in ', cell
#else:
#    pl.scatter(data[:,1], data[:,0], c=cl, s=size, marker="|")
#    mean += (np.min(data[:,0])+np.max(data[:,0]))/2
#    pl.text(xa, mean, cell, color=cl)
#    mean = 0
#    z += 1
#    cl = color[z%len(color)]
#
#
#
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
#    mean = mean/params['n_actions']
#    pl.text(xa,mean, cell, color=cl)
#    z += 1
#    cl = color[z%len(color)]
#    mean = 0
#pl.legend()
#pl.show()
