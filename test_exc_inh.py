import nest
import numpy as np
import matplotlib
import pylab as pl


nest.ResetKernel()
nest.SetKernelStatus({"overwrite_files": True})

exc = nest.Create('iaf_cond_alpha',1)
inh = nest.Create('iaf_cond_alpha',1)
tgt = nest.Create('iaf_cond_alpha',1)

poisson = nest.Create('poisson_generator',1)
noise   = nest.Create('poisson_generator',1)
spike_file = "fspike"
volt_file  = "fvolt"


volt = nest.Create('multimeter', params={'record_from': ['V_m'], 'interval':.1})
nest.SetStatus(volt, [{"to_file": True, "withtime":True, "label":volt_file}])


recorder = nest.Create('spike_detector')
nest.SetStatus(recorder, [{"to_file": True, "withtime":True, "label":spike_file}])
nest.Connect(exc, recorder)
nest.Connect(inh, recorder)
nest.Connect(tgt, recorder)
nest.Connect(volt, tgt)

w_exc = 20.
w_inh = -5.
w_noise = 5.
w_poisson = 5.

rate_poisson = 4000.
rate_noise = 2000.


nest.Connect(exc, tgt, 'one_to_one', {'weight':w_exc, 'delay':1.})
nest.Connect(inh, tgt, 'one_to_one', {'weight':w_inh, 'delay':1.})
nest.Connect(noise, tgt, 'one_to_one', {'weight':w_noise, 'delay':1.})
nest.Connect(poisson, exc, 'one_to_one', {'weight':w_poisson, 'delay':1.})
nest.Connect(poisson, inh, 'one_to_one', {'weight':w_poisson, 'delay':1.})

nest.SetStatus(noise, {'rate':rate_noise})


nest.Simulate(500.)
nest.SetStatus(poisson, {'rate':rate_poisson})
nest.Simulate(500.)


spike_data = np.loadtxt(spike_file+"-"+str(recorder[0])+"-0.gdf")
volt_data= np.loadtxt(volt_file+"-"+str(volt[0])+"-0.dat")


pl.figure(22)
pl.subplot(211)
pl.scatter(spike_data[:,1], spike_data[:,0], marker = "|")
pl.subplot(212)
gids = np.unique(volt_data[:,0])
for gid in gids:
    d = volt_data[volt_data[:,0]==gid, 1:]
    pl.plot(d[d[:,0].argsort(),1], lw=2, label="V_"+str(gid))
pl.hlines(nest.GetStatus(tgt)[0]['V_th'], 0, max(volt_data[:,1])*10., colors="k", linestyles="solid", label="V_th")
pl.legend()
#pl.subplot(312)
#pl.scatter(spike_data[:,1], spike_data[:,0], marker = "|")
#pl.subplot(313)
#pl.scatter(spike_data[:,1], spike_data[:,0], marker = "|")

#pl.figure(23)
pl.show()
