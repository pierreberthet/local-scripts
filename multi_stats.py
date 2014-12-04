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

params['multi_n']+=1

source_d1 = params['weights_d1_multi_fn']+'_'
source_d2 = params['weights_d2_multi_fn']+'_'
source_rew = params['rewards_multi_fn']+'_'
source_rp = params['weights_rp_multi_fn']+'_'
print 'init phase'
color = ['b','g', 'r', 'c', 'm', 'y', 'k']
z = 0
cl = color[z%len(color)]

lend1= len(np.loadtxt(source_d1+'0'))
lend2= len(np.loadtxt(source_d2+'0'))
lenrp= len(np.loadtxt(source_rp+'0'))
if not lend1 == lend2:
    print 'INCONSISTENCY D1 and D2 length (number of recordings)'
#params['multi_n'] = params['multi_n'] -1
wd1 = np.zeros((params['multi_n'], lend1, params['n_actions']))
wd1_m = np.zeros((lend1, params['n_actions']))
wd1_std = np.zeros((lend1, params['n_actions']))
wd2 = np.zeros((params['multi_n'], lend2,params['n_actions']))
wd2_m = np.zeros((lend2, params['n_actions']))
wd2_std = np.zeros((lend2, params['n_actions']))
wrp = np.zeros((params['multi_n'], lenrp,params['n_actions'] * params['n_states']))
wrp_m = np.zeros((lenrp, params['n_actions'] * params['n_states']))
wrp_std = np.zeros((lenrp, params['n_actions'] * params['n_states']))
rewards = np.zeros((params['multi_n'], params['n_iterations']))
rewards_m = np.zeros(params['n_iterations'])
rewards_std = np.zeros(params['n_iterations'])

for i in xrange(params['multi_n']):
    wd1[i] = np.loadtxt(source_d1+str(i))
    wd2[i] = np.loadtxt(source_d2+str(i))
    wrp[i] = np.loadtxt(source_rp+str(i))
    rewards[i] = np.loadtxt(source_rew+str(i))


for i in xrange(lend1):
    for j in xrange(params['n_actions']):
        wd1_m[i,j] = np.mean(wd1[:,i,j])
        wd1_std[i,j] = np.std(wd1[:,i,j])
        wd2_m[i,j] = np.mean(wd2[:,i,j])
        wd2_std[i,j] = np.std(wd2[:,i,j])
for i in xrange(lenrp):
    for j in xrange(params['n_actions']*params['n_states']):
        wrp_m[i,j] = np.mean(wrp[:,i,j])
        wrp_std[i,j] = np.std(wrp[:,i,j])

#wd1 = wd1 / params['multi_n']
#wd2 = wd2 / params['multi_n']
#rewards = rewards / params['multi_n']

mini = np.minimum(np.min(wd1_m - wd1_std), np.min(wd2_m - wd2_std)) - .2
maxi = np.maximum(np.max(wd1_m + wd1_std), np.max(wd2_m + wd2_std)) + .2
print 'd1 data' 

pl.figure(600)
pl.subplot(211)
pl.title('D1')
for i in xrange(params['n_actions']):
    pl.plot(wd1_m[:,i], c=cl)
    pl.fill_between(np.arange(lend1), wd1_m[:,i] + wd1_std[:,i], wd1_m[:,i] - wd1_std[:,i], facecolor=cl,alpha =.5 )
    z+=1
    cl = color[z%len(color)]
    
mean = np.zeros(lend1)
for j in xrange(lend1):
    mean[j] = np.mean(wd1_m[j,:])
pl.plot(mean, 'k.')
pl.ylim([mini, maxi])
pl.ylabel(r'$W_{ij}$')
#pl.vlines( np.arange(0,params['t_sim']/params['resolution'], params['t_sim']/(params['n_blocks']*params['resolution'])), [0], [1.01], color='0.55', linestyles='dashed' )
if params['n_blocks']>1:
    pl.vlines( np.arange(lend1/params['n_blocks'], lend1-1., lend1/params['n_blocks'] ), [mini], [maxi], color='0.55', linestyles='dashed' )

z=0
cl = color[z%len(color)]
print 'd2 data' 
pl.subplot(212)
mean = np.zeros(lend2)
pl.title('D2')
for i in xrange(params['n_actions']):
    pl.plot(wd2_m[:,i], c=cl)
    pl.fill_between(np.arange(lend2), wd2_m[:,i] + wd2_std[:,i], wd2_m[:,i] - wd2_std[:,i], alpha =.5, facecolor=cl )
    z+=1
    cl = color[z%len(color)]
for j in xrange(lend2):
    mean[j] = np.mean(wd2_m[j,:])
pl.plot(mean, 'k.')
pl.ylim([mini, maxi])
pl.ylabel(r'$W_{ij}$')
pl.xlabel(r'$time$ in '+str(params['resolution'])+' ms')
#pl.vlines( np.arange(0,params['t_sim']/params['resolution'], params['t_sim']/(params['n_blocks']*params['resolution'])), [0], [1.01], color='0.55', linestyles='dashed' )
if params['n_blocks']>1:
    pl.vlines( np.arange(lend2/params['n_blocks'], lend2-1., lend2/params['n_blocks'] ), [mini], [maxi], color='0.55', linestyles='dashed' )

print 'rp data' 
pl.figure(601)
z=0
mean = np.zeros(lenrp)
cl = color[z%len(color)]
pl.xlabel(r'$time$ in '+str(params['resolution'])+' ms')
pl.ylabel('average RP weights')
for i in xrange(params['n_actions']*params['n_states']):
    pl.plot(wrp_m[:,i], c=cl)
    pl.fill_between(np.arange(lenrp), wrp_m[:,i] + wrp_std[:,i], wrp_m[:,i] - wrp_std[:,i], alpha =.5, facecolor=cl )
    z+=1
    cl = color[z%len(color)]
if params['n_blocks']>1:
    pl.vlines( np.arange(lenrp/params['n_blocks'], lenrp-1., lenrp/params['n_blocks'] ), -.2, .2, color='0.55', linestyles='dashed' )
for j in xrange(lenrp):
    mean[j] = np.mean(wrp_m[j,:])
pl.plot(mean, 'k.')


perf= np.zeros((params['multi_n'], params['n_iterations']))
for j in xrange(0, params['multi_n']):
    for i in xrange(1, params['n_iterations']):
        perf[j,i]= perf[j,i-1] + (rewards[j,i] - perf[j,i-1])*0.25
for m in xrange(params['n_iterations']):
    rewards_m[m] = np.mean(perf[:,m])
    rewards_std[m] = np.std(perf[:,m])
print 'average perf'
pl.figure(602)
#pl.title('performance')
pl.xlabel('trials')
pl.ylabel('average success ratio')
if params['n_blocks']>1:
    pl.vlines( np.arange(params['block_len'],params['n_blocks']*params['block_len']-1., params['block_len']), [0], [1.05], color='0.55', linestyles='dashed' )
pl.plot(rewards_m)
pl.fill_between(np.arange(params['n_iterations']), rewards_m +rewards_std, rewards_m - rewards_std, alpha=.2)
pl.ylim([0, 1.05])


#for i in xrange(params['multi_n']):
#    pl.figure(333+i)
#    pl.subplot(211)
#    pl.title('D1 run '+str(i))
#    pl.plot(wd1[i])
#    pl.subplot(212)
#    pl.title('D2 run '+str(i))
#    pl.plot(wd2[i])

pl.figure(330)
for i in xrange(params['multi_n']):
    pl.plot(perf[i], label=i)
pl.show()



