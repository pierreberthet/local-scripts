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


cells= ['actions']
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
