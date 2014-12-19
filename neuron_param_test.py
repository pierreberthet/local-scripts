import nest
import nest.raster_plot
import numpy as np
import pylab as pl


nest.ResetKernel()
nest.SetKernelStatus({"overwrite_files": True})



if (not 'bcpnn_dopamine_synapse' in nest.Models()):
    nest.Install('ml_module')
# #####
# DOPA
# #####
#popa = nest.Create('iaf_neuron', 200)
#vt_dopa = nest.Create('volume_transmitter', 1)

#nest.ConvergentConnect(popa, vt_dopa, weight= 5., delay = 1.)

sample_size = 20
neuron_a = nest.Create('iaf_cond_alpha_bias', sample_size)
neuron_b = nest.Create('iaf_cond_alpha_bias', sample_size)
poisson = nest.Create('poisson_generator',1)

recorder = nest.Create('spike_detector',1)
voltmeter_a = nest.Create('multimeter', 1, params={'record_from': ['V_m'], 'interval' :0.1} )
voltmeter_b = nest.Create('multimeter', 1, params={'record_from': ['V_m'], 'interval' :0.1} )
nest.SetStatus(voltmeter_a, [{"to_file": True, "withtime": True, 'label' : 'volt'}])
nest.SetStatus(voltmeter_b, [{"to_file": True, "withtime": True, 'label' : 'volt'}])




time = 300.

key_a = 'C_m'
key_b = 'V_m'
spread = .2





default_a = nest.GetStatus([neuron_a[0]], key_a)[0]
default_b = nest.GetStatus([neuron_b[0]], key_b)[0]
print 'Default value for ', key_a, 'is ', default_a
print 'Default value for ', key_b, 'is ', default_b
start_a = (1-spread)*default_a
end_a = (1+spread)*default_a
value_a = np.arange(start_a, end_a, (end_a-start_a)/sample_size)
start_b = (1-spread)*default_b
end_b = (1+spread)*default_b
value_b = np.arange(start_b, end_b, (end_b-start_b)/sample_size)

for i in xrange(sample_size):
    nest.SetStatus([neuron_a[i]], {key_a:value_a[i]})
    nest.SetStatus([neuron_b[i]], {key_b:value_b[i]})
    
    
nest.DivergentConnect(poisson, neuron_a, weight=4., delay=1.)
nest.DivergentConnect(poisson, neuron_b, weight=4., delay=1.)
nest.ConvergentConnect(neuron_a, recorder)
nest.ConvergentConnect(neuron_b, recorder)
nest.ConvergentConnect(voltmeter_a, neuron_a)
nest.ConvergentConnect(voltmeter_b, neuron_b)
nest.SetStatus(poisson, {'rate': 0.})

nest.Simulate(time)

nest.SetStatus(poisson, {'rate': 2500.})

nest.Simulate(time)

nest.SetStatus(poisson, {'rate': 500.})
nest.Simulate(time)

events = nest.GetStatus(voltmeter_a)[0]['events']
t = events['times']

xmin = 0.
xmax = 30*time
ymin = -85.
ymax = -50.

ax = [ xmin, xmax, ymin, ymax]

pl.subplot(211)
gids = np.unique(events['senders'])
i = 0
for gid in gids:
    pl.plot(events['V_m'][events['senders']==gid], label=str(value_a[i]))
    i+=1
#pl.plot(t, events['V_m'])
pl.ylabel('Membrane potential [mV]')
pl.xlabel('time [ms]')
pl.axis(ax)
pl.subplot(212)
events = nest.GetStatus(voltmeter_b)[0]['events']
t = events['times']
gids = np.unique(events['senders'])
i = 0
for gid in gids:
    pl.plot(events['V_m'][events['senders']==gid], label=str(value_b[i]))
    i+=1
#pl.plot(t, events['V_m'])
pl.ylabel('Membrane potential [mV]')
pl.xlabel('time [ms]')
pl.axis(ax)
pl.suptitle(str(100*spread)+' % variation of '+key_a +' default value = '+str(default_a) +'and '+ key_b + ' default value = '+str(default_b))
pl.legend()
pl.show()

nest.raster_plot.from_device(recorder, hist=True)
nest.raster_plot.show()


param = [{'C_m': 250.0,
'E_L': -70.0,
'E_ex': 0.0,
'E_in': -85.0,
'I_e': 0.0,
'V_m': -70.0,
'V_reset': -60.0,
'V_th': -55.0,
'archiver_length': 0,
'bias': 0.0,
'epsilon': 0.001,
'fmax': 20.0,
'frozen': False,
'g_L': 16.6667,
'gain': 1.0,
'global_id': 204,
'kappa': 1.0,
'local': True,
'local_id': 204,
'model': 'iaf_cond_alpha_bias',
'parent': 0,
'recordables': ['V_m',
't_ref_remaining',
'g_ex',
'g_in',
'z_j',
'e_j',
'p_j',
'bias',
'epsilon',
'kappa'],
'state': 0,
't_ref': 2.0,
't_spike': -1.0,
'tau_e': 100.0,
'tau_j': 10.0,
'tau_minus': 20.0,
'tau_minus_triplet': 110.0,
'tau_p': 1000.0,
'tau_syn_ex': 0.2,
'tau_syn_in': 2.0,
'thread': 0,
'type': 'neuron',
'vp': 0}]

