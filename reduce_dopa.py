import nest
import nest.raster_plot
import numpy as np
import pylab as pl


nest.ResetKernel()
nest.SetKernelStatus({"overwrite_files": True})



if (not 'bcpnn_dopamine_synapse' in nest.Models()):
    nest.Install('ml_module')


popa = nest.Create('iaf_neuron', 200)
vt_dopa = nest.Create('volume_transmitter', 1)

nest.ConvergentConnect(popa, vt_dopa, weight= 5., delay = 1.)

sample_size = 20
neuron = nest.Create('iaf_cond_alpha_bias', sample_size)
poisson = nest.Create('poisson_generator',1)

recorder = nest.Create('spike_detector',1)
voltmeter = nest.Create('multimeter', 1, params={'record_from': ['V_m'], 'interval' :0.1} )
nest.SetStatus(voltmeter, [{"to_file": True, "withtime": True, 'label' : 'volt'}])




time = 300.

key = 'C_m'
spread = .2





default = nest.GetStatus([neuron[0]], key)[0]
print 'Default value for ', key, 'is ', default
start = (1-spread)*default
end= (1+spread)*default
value = np.arange(start, end, (end-start)/sample_size)

for i in xrange(sample_size):
    nest.SetStatus([neuron[i]], {key:value[i]})
    
    
nest.DivergentConnect(poisson, neuron, weight=4., delay=1.)
nest.ConvergentConnect(neuron, recorder)
nest.ConvergentConnect(voltmeter, neuron)
nest.SetStatus(poisson, {'rate': 0.})

nest.Simulate(time)

nest.SetStatus(poisson, {'rate': 2500.})

nest.Simulate(time)

nest.SetStatus(poisson, {'rate': 500.})
nest.Simulate(time)

events = nest.GetStatus(voltmeter)[0]['events']
t = events['times']

pl.subplot(211)
pl.plot(t, events['V_m'])
pl.ylabel('Membrane potential [mV]')

pl.subplot(212)
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

