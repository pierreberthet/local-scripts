import numpy as np
import simulation_parameters
import nest
import nest.raster_plot
import matplotlib
import pylab as pl
import json
import pprint as pp

if (not 'bcpnn_dopamine_synapse' in nest.Models('synapses')):
    nest.Install('ml_module')

GP = simulation_parameters.global_parameters()
#GP.write_parameters_to_file() # write_parameters_to_file MUST be called before every simulation
params = GP.params


nest.ResetKernel()

#f = file('Test/Parameters/simulation_parameters.json', 'r')
#params = json.load(f)

pp.pprint( params)

resolution = 5.

dk = np.array([])
dkf = np.array([])
dm = np.array([])
dn = np.array([])
dk2 = np.array([])
dm2 = np.array([])
dn2 = np.array([])

pi = np.array([])
pj = np.array([])
pij = np.array([])
w = np.array([])
# = np.array([])
pi2 = np.array([])
pj2 = np.array([])
pij2 = np.array([])
w2 = np.array([])
# = np.array([])


def simulate(time):
        global dk, dkf
        global dm
        global dn    
        global dk2 
        global dm2 
        global dn2   
        global pi, pj, pij, w
        global pi2, pj2, pij2, w2
        sim_time = time / resolution
        connB = nest.GetConnections(pre, post)
        #connC = nest.GetConnections(pop, popC)
        #print 'CONN B', connB
        #print 'CONN C', connC
        for i in xrange(int(sim_time)):
            nest.Simulate(resolution)
            dk=np.r_[dk, nest.GetStatus(connB, ['k'])[0]]
            dkf=np.r_[dkf, nest.GetStatus(connB, ['k_filtered'])[0]]
            dm=np.r_[dm, nest.GetStatus(connB, ['m'])[0]]
            dn=np.r_[dn, nest.GetStatus(connB, ['n'])[0]]
           # dk2=np.r_[dk2, nest.GetStatus(connC, ['k'])[0]]
           # dm2=np.r_[dm2, nest.GetStatus(connC, ['m'])[0]]
           # dn2=np.r_[dn2, nest.GetStatus(connC, ['n'])[0]]
            pi = np.r_[pi, np.mean([a['p_i'] for a in nest.GetStatus(connB)])]
            pj = np.r_[pj, np.mean([a['p_j'] for a in nest.GetStatus(connB)])]
            pij = np.r_[pij, np.mean([a['p_ij'] for a in nest.GetStatus(connB)])]
            w = np.r_[w, np.mean([(np.log(a['p_ij']/(a['p_i']*a['p_j']))) for a in nest.GetStatus(connB)])]
           # pi2 = np.r_[pi2, np.mean([a['p_i'] for a in nest.GetStatus(connC)])]
           # pj2 = np.r_[pj2, np.mean([a['p_j'] for a in nest.GetStatus(connC)])]
           # pij2 = np.r_[pij2, np.mean([a['p_ij'] for a in nest.GetStatus(connC)])]
           # w2 = np.r_[w2, np.mean([(np.log(a['p_ij']/(a['p_i']*a['p_j']))) for a in nest.GetStatus(connC)])]
        return



params['neuron'] = {'V_th':-50. , 'C_m':250. , 'kappa': 1. ,'fmax':20. ,'V_reset':-75. }

### TEST script for silent neurons within homegeneous population with bcpnn dopa synapses

num_in = 10
num_pop = 10
num_dopa = 50

pre = nest.Create('iaf_cond_alpha_bias', num_in, params=params['neuron'])
post = nest.Create('iaf_cond_alpha_bias', num_pop, params=params['neuron'])
dopa = nest.Create('iaf_cond_alpha_bias', num_dopa, params=params['neuron'])


vt = nest.Create('volume_transmitter')

rew = nest.Create('poisson_generator',1)
stim = nest.Create('poisson_generator',1)
efference = nest.Create('poisson_generator',1)

volt = nest.Create('multimeter', params={'record_from': ['V_m'], 'interval' :0.1})
recorder_rew = nest.Create("spike_detector", params= {"withgid":True, "withtime":True})
recorder_post= nest.Create("spike_detector", params= {"withgid":True, "withtime":True})
recorder_pre= nest.Create("spike_detector", params= {"withgid":True, "withtime":True})


nest.ConvergentConnect(dopa, vt, weight = 4., delay = 1.)
nest.DivergentConnect(stim, pre, weight = 4., delay = 1.)
nest.DivergentConnect(efference, post, weight = 4., delay = 1.)
nest.DivergentConnect(rew, dopa, weight = 4., delay = 1.)

nest.ConvergentConnect(pre, recorder_pre)
nest.ConvergentConnect(post, recorder_post)
nest.ConvergentConnect(dopa, recorder_rew)
nest.ConvergentConnect(volt, post)

nest.SetDefaults('bcpnn_dopamine_synapse', { 'vt': vt[0] })
#nest.SetDefaults('bcpnn_dopamine_synapse', params=params['params_dopa_bcpnn'])
print 'sim start'


nest.DivergentConnect(pre, post, model='bcpnn_dopamine_synapse')

nest.SetStatus(rew, {'rate':2500.})
simulate(100.)
nest.SetStatus(stim, {'rate':3000.})

total_time = 300.
simulate(100.)

#nest.SetStatus(efference, {'rate':3000.})
simulate(100.)

#nest.raster_plot.from_device(recorder_rew, hist=True)
#pl.title('DOPA')
#nest.raster_plot.from_device(recorder_pre, hist=True)
#pl.title('PRE')
#nest.raster_plot.from_device(recorder_post, hist=True)
#pl.title('POST')

pl.figure(66)
data = nest.GetStatus(volt)[0]['events']
gids = np.unique(data['senders'])
for gid in gids:
    d = data['V_m'][ data['senders']==gid]
    pl.plot( d, label=str(int(gid)), lw=2)
pl.title('POST')

pl.figure(11)
pl.plot(dk, label='k')
pl.plot(dkf, label='k_filtered')
pl.plot(dm, label='m')
pl.plot(dn, label='n')
pl.legend()


pl.figure(13)
pl.plot(pi, label='pi')
pl.plot(pj, label='pj')
pl.plot(pij, label='pij')
pl.plot(w, label='w')
pl.title('PRE --> POST')
pl.legend()


exc_sptimes = nest.GetStatus(recorder_rew)[0]['events']['times']
exc_spids = nest.GetStatus(recorder_rew)[0]['events']['senders']
pl.figure(34)
pl.subplot(211)
pl.title('POP DOPA')
pl.scatter(exc_sptimes, exc_spids,s=1.)
pl.xlim([0,total_time])
binsize = 10
bins=np.arange(0, total_time+1, binsize)
c_exc,b = np.histogram(exc_sptimes,bins=bins)
rate_dopa = c_exc*(1000./binsize)*(1./num_dopa)
pl.subplot(212)
pl.plot(b[0:-1],rate_dopa)

exc_sptimes = nest.GetStatus(recorder_pre)[0]['events']['times']
exc_spids = nest.GetStatus(recorder_pre)[0]['events']['senders']
pl.figure(35)
pl.subplot(211)
pl.title('PRE')
pl.scatter(exc_sptimes, exc_spids,s=1.)
pl.xlim([0,total_time])
binsize = 10
bins=np.arange(0, total_time +1, binsize)
c_exc,b = np.histogram(exc_sptimes,bins=bins)
rate_A = c_exc*(1000./binsize)*(1./num_in)
pl.subplot(212)
pl.plot(b[0:-1],rate_A)

exc_sptimes = nest.GetStatus(recorder_post)[0]['events']['times']
exc_spids = nest.GetStatus(recorder_post)[0]['events']['senders']
pl.figure(36)
pl.subplot(211)
pl.title('POST')
pl.scatter(exc_sptimes, exc_spids,s=1.)
pl.xlim([0,total_time])
binsize = 10
bins=np.arange(0, total_time+1, binsize)
c_exc,b = np.histogram(exc_sptimes,bins=bins)
rate_B = c_exc*(1000./binsize)*(1./num_pop)
pl.subplot(212)
pl.plot(b[0:-1],rate_B)


nest.raster_plot.show()
