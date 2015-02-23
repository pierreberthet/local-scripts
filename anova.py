import numpy as np
import json
import matplotlib
#matplotlib.use('Agg')
import pylab as pl
import sys
import pprint as pp
import difflib
#from difflib_data import *
# Plot the different figures for the merged spikes and voltages recordings.
# This file, as the MergeSpikefiles.py should be one level up than Test/..., the output of a simulation.

import scipy.stats as stats

def get_weights(folder):
    fparam = folder+'Test/Parameters/simulation_parameters.json'
    f = open(fparam, 'r')
    params = json.load(f)
    
    params['multi_n']+=1
    
    source_rew= folder+params['rewards_multi_fn']+'_'
    rewards = np.zeros((params['multi_n'], params['n_iterations']))
    
    for i in xrange(params['multi_n']):
        rewards[i] = np.loadtxt(source_rew+str(i))
    
    
    #for i in xrange(lend1):
    #    for j in xrange(params['n_actions']):
    #        wd1_m[i,j] = np.mean(wd1[:,i,j])
    #        wd1_std[i,j] = np.std(wd1[:,i,j])
    #        wd2_m[i,j] = np.mean(wd2[:,i,j])
    #        wd2_std[i,j] = np.std(wd2[:,i,j])
    #for i in xrange(lenrp):
    #    for j in xrange(params['n_actions']*params['n_states']):
    #        wrp_m[i,j] = np.mean(wrp[:,i,j])
    #        wrp_std[i,j] = np.std(wrp[:,i,j])

    return rewards
######################################
######################################


if len(sys.argv)<2: 
    print "Need 2 folders for comparison"
    pass

fname ={}

for i in xrange(1,len(sys.argv)):
    fname[i-1] = sys.argv[i]+'/'

params={}

for i in xrange(len(fname)):
    params[i]=json.load(open(fname[i]+'Test/Parameters/simulation_parameters.json'))


#print 'Do the simulations match? ',  params[:]['n_recordings']==params[:]['n_recordings']

#diff = difflib.ndiff(open(fparam1,'r').readlines(), open(fparam2,'r').readlines())
#print ''.join(diff)

rew = {}

for i in xrange(len(fname)):
    rew[i] = get_weights(fname[i])

start = 4
shift = start*params[1]['block_len']*params[1]['t_iteration']/params[1]['resolution']
shift_rew = start*params[1]['block_len']

perf = {}
for i in xrange(len(fname)):
    perf[i] = np.zeros(params[1]['multi_n'], dtype=float)
j=0
#for i in xrange(shift_rew, params1['n_iterations']):
#    r1[j]=sum(rewa[:,i])
#    r2[j]=sum(rewb[:,i])
#    j+=1

#for i in xrange(start, params1['n_blocks']):
for f in xrange(len(fname)):
    j=0
    for i in xrange(params[f]['multi_n']):
        for q in xrange(start, params[f]['n_blocks']):
            perf[f][j]+=sum(rew[f][i,q*params[f]['block_len']-6:q*params[f]['block_len']-1])
        j+=1

for f in xrange(len(fname)):
    perf[f] = perf[f]/((params[f]['n_blocks']-start)*5.)



print 'PERF'
for i in xrange(len(fname)):
    print  fname[i], 'mean= ',  np.mean(perf[i]), 'SD=', np.std(perf[i])
    for j in xrange(len(fname)):
        print fname[j], 'mean ',  np.mean(perf[j]), 'SD=', np.std(perf[j])
        print 'T-TEST: ', stats.ttest_ind(perf[i],perf[j])
        print 'F-TEST: ', stats.f_oneway(perf[i], perf[j])
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print '\n'
    print '+++++++++++++++++++++++++++++++'
print '\n'
print '\n'

