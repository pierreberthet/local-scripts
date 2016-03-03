import numpy as np
import json
import matplotlib
#matplotlib.use('Agg')
import pylab as pl
import pprint as pp
import sys
# Plot the different figures for the merged spikes and voltages recordings.
# This file, as the MergeSpikefiles.py should be one level up than Test/..., the output of a simulation.

path = sys.argv[1]+'/'

fparam = path+'Test/Parameters/simulation_parameters.json'
#print fparam
f = open(fparam, 'r')
params = json.load(f)


si = 15 
parms = {
    'axes.labelsize': si,
    'text.fontsize': si,
    'legend.fontsize': si,
    'xtick.labelsize': si,
    'ytick.labelsize': si,
    'text.usetex': False
    #'figure.figsize': [6., 7.]
}
pl.rcParams.update(parms)

params['multi_n']+=1

source_gpi =   path+ params['actions_taken_fn']+'_'
source_bs =    path+ params['actions_bs_fn']+'_'

#source_rew = np.loadtxt(  path+ params['rewards_multi_fn']+'_' )

print 'init phase'
color = ['b','g', 'r', 'c', 'm', 'y', 'k']
z = 0
cl = color[z%len(color)]

len_gpi= len(np.loadtxt(source_gpi+'0'))
len_habit= len(np.loadtxt(source_bs+'0'))



gpi = np.zeros((params['multi_n'], len_gpi))
gpi_m = np.zeros(len_gpi)
gpi_std = np.zeros(len_gpi)
habit = np.zeros((params['multi_n'], len_habit))
habit_m = np.zeros(len_habit)
habit_std = np.zeros(len_habit)

for i in xrange(params['multi_n']):
    gpi[i] = np.loadtxt(source_gpi+str(i))
    habit[i] = np.loadtxt(source_bs+str(i))


for i in xrange(len_gpi):
    gpi_m[i] =    np.mean(gpi[:,i])
    gpi_std[i] =   np.std(gpi[:,i])
    habit_m[i] =  np.mean(habit[:,i])
    habit_std[i]=  np.std(habit[:,i])

mini = np.minimum(np.min(gpi_m - gpi_std), np.min(habit_m - habit_std)) - .1
maxi = np.maximum(np.max(gpi_m + gpi_std), np.max(habit_m + habit_std)) + .1



pl.figure(600)
ax = pl.subplot(211)
pl.title('BG')
for i in xrange(params['n_actions']):
    pl.plot(gpi_m[i:-1:params['n_actions']], c=cl)
    pl.fill_between(np.arange(len_gpi/3), gpi_m[i:-1:params['n_actions']] + gpi_std[i:-1:params['n_actions']], gpi_m[i:-1:params['n_actions']] - gpi_std[i:-1:params['n_actions']], facecolor=cl,alpha =.5 )
    z+=1
    cl = color[z%len(color)]
    
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
ax.tick_params(axis='x', direction='out')
ax.get_xaxis().set_visible(False)
ax.tick_params(axis='y', length=0)
ax.grid(axis='y', color="0.9", linestyle='-', linewidth=1)
ax.set_axisbelow(True)

pl.ylim([mini, maxi])
pl.xticks(pl.xticks()[0],[str(int(a*.25)) for a in pl.xticks()[0]])
pl.ylabel('Action selected')
#pl.ylabel(r'$W_{ij}$')
#pl.vlines( np.arange(0,params['t_sim']/params['resolution'], params['t_sim']/(params['n_blocks']*params['resolution'])), [0], [1.01], color='0.55', linestyles='dashed' )
if params['n_blocks']>1:
    #pl.vlines( np.arange(len_gpi/(3*params['n_blocks']), len_gpi/3-1., len_gpi/(3*params['n_blocks']) ), [mini], [maxi], color='0.55', linestyles='dashed' )
    pl.vlines( np.arange(params['block_len']/3, len_gpi/3-4, params['block_len']/3+1 ), [mini], [maxi], color='0.55', linestyles='dashed' )
pl.tight_layout()

z=0
cl = color[z%len(color)]
ax =pl.subplot(212)
pl.title('Habit')
for i in xrange(params['n_actions']):
    pl.plot(habit_m[i:-1:params['n_actions']], c=cl)
    pl.fill_between(np.arange(len_habit/3), habit_m[i:-1:params['n_actions']] + habit_std[i:-1:params['n_actions']], habit_m[i:-1:params['n_actions']] - habit_std[i:-1:params['n_actions']], facecolor=cl,alpha =.5 )
    z+=1
    cl = color[z%len(color)]
    
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
ax.tick_params(axis='x', direction='out')
ax.get_xaxis().set_visible(False)
ax.tick_params(axis='y', length=0)
ax.grid(axis='y', color="0.9", linestyle='-', linewidth=1)
ax.set_axisbelow(True)
#pl.xticks([0,1,2,3,4,5,6],['0','65','130', '185', '250','325','390'])
pl.ylabel('Action selected for state 1')

pl.ylim([mini, maxi])
#pl.xticks(pl.xticks()[0],[str(int(a*12.5)) for a in pl.xticks()[0]])
pl.ylabel('Action selected')
#pl.ylabel(r'$W_{ij}$')
#pl.vlines( np.arange(0,params['t_sim']/params['resolution'], params['t_sim']/(params['n_blocks']*params['resolution'])), [0], [1.01], color='0.55', linestyles='dashed' )
if params['n_blocks']>1:
    pl.vlines( np.arange(params['block_len']/3, len_gpi/3-4, params['block_len']/3+1 ), [mini], [maxi], color='0.55', linestyles='dashed' )
pl.tight_layout()


z=0
cl = color[z%len(color)]
pl.figure(200)
ax =pl.subplot(111)
#pl.title('Habit vs BG')
i=0
gpi_m[params['block_trigger1']*params['block_len']+1:params['block_trigger2']*params['block_len']+1] = None
gpi_std[params['block_trigger1']*params['block_len']+1:params['block_trigger2']*params['block_len']+1] = None
pl.plot(gpi_m[i:-1:params['n_actions']], c=cl, label='BG')
#pl.fill_between(np.arange(len_gpi/3), gpi_m[i:-1:params['n_actions']] + gpi_std[i:-1:params['n_actions']], gpi_m[i:-1:params['n_actions']] - gpi_std[i:-1:params['n_actions']], facecolor=cl,alpha =.5 )
pl.fill_between(np.arange((params['block_trigger1']*params['block_len'])/3), gpi_m[i:params['block_trigger1']*params['block_len']-2:params['n_actions']] + gpi_std[i:params['block_trigger1']*params['block_len']-2:params['n_actions']], gpi_m[i:params['block_trigger1']*params['block_len']-2:params['n_actions']] - gpi_std[i:params['block_trigger1']*params['block_len']-2:params['n_actions']], facecolor=cl,alpha =.5 )
pl.fill_between(np.arange(params['block_trigger2']*params['block_len']/3, params['n_iterations']/3), gpi_m[params['block_trigger2']*params['block_len']-1+i:-1:params['n_actions']] + gpi_std[params['block_trigger2']*params['block_len']-1+i:-1:params['n_actions']], gpi_m[params['block_trigger2']*params['block_len']-1+i:-1:params['n_actions']] - gpi_std[params['block_trigger2']*params['block_len']-1+i:-1:params['n_actions']], facecolor=cl,alpha =.5 )
z+=2
cl = color[z%len(color)]

pl.plot(habit_m[i:-1:params['n_actions']], c=cl, label='Habit')
pl.fill_between(np.arange(len_habit/3), habit_m[i:-1:params['n_actions']] + habit_std[i:-1:params['n_actions']], habit_m[i:-1:params['n_actions']] - habit_std[i:-1:params['n_actions']], facecolor=cl,alpha =.5 )

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
ax.tick_params(axis='x', direction='out')
#ax.get_xaxis().set_visible(False)
ax.tick_params(axis='y', length=0)
ax.grid(axis='y', color="0.9", linestyle='-', linewidth=1)
ax.set_axisbelow(True)

pl.ylim([mini, maxi])
#pl.xticks(pl.xticks()[0],[str(int(a*.25)) for a in pl.xticks()[0]])
pl.yticks([0,1,2],['1','2','3'])
pl.ylabel('Average action selected in state '+str(i+1))
pl.xlabel('block #')
#pl.ylabel(r'$W_{ij}$')
#pl.vlines( np.arange(0,params['t_sim']/params['resolution'], params['t_sim']/(params['n_blocks']*params['resolution'])), [0], [1.01], color='0.55', linestyles='dashed' )
if params['n_blocks']>1:
    #pl.vlines( np.arange(len_gpi/(3*params['n_blocks']), len_gpi/3-1., len_habit/(3*params['n_blocks']) ), [mini], [maxi], color='0.55', linestyles='dashed' )
    pl.vlines( np.arange(params['block_len']/3, len_gpi/3-4, params['block_len']/3+1 ), [mini], [maxi], color='0.55', linestyles='dashed' )
pl.xticks(np.arange(params['block_len']/6, len_gpi/3, params['block_len']/3+1) , ['1','2','3','4','5','6','7','8'])
pl.xlim([0.,params['block_len']*params['n_blocks']/3-1])
pl.legend()
pl.tight_layout()
#pl.figure(200)
#pl.plot(source_gpi[0::params['n_actions']])
#pl.plot(source_bs[0::params['n_actions']])



z=0
cl = color[z%len(color)]
pl.figure(202)
ax =pl.subplot(111)
pl.title('Habit vs BG')
i=0

gpi[0][params['block_trigger1']*params['block_len']:params['block_trigger2']*params['block_len']] = None
xval = np.arange(len_gpi/3)
#pl.plot(gpi[0][i:-1:params['n_actions']], c=cl, label='BG')
gpi[0] -= .04
pl.scatter(xval,gpi[0][i:-1:params['n_actions']], c=cl, label='BG')
z+=2
cl = color[z%len(color)]
#pl.plot(habit[0][i:-1:params['n_actions']], c=cl, label='Habit')
habit[0]+=.04
pl.scatter(xval,habit[0][i:-1:params['n_actions']], c=cl, label='Habit')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
ax.tick_params(axis='x', direction='out')
#ax.get_xaxis().set_visible(False)
ax.tick_params(axis='y', length=0)
ax.grid(axis='y', color="0.9", linestyle='-', linewidth=1)
ax.set_axisbelow(True)

pl.ylim([mini, maxi])
pl.xticks(pl.xticks()[0],[str(int(a*.25)) for a in pl.xticks()[0]])
pl.yticks([0,1,2],['1','2','3'])
pl.ylabel('action selected for state 1')
pl.xlabel('trials')
#pl.ylabel(r'$W_{ij}$')
#pl.vlines( np.arange(0,params['t_sim']/params['resolution'], params['t_sim']/(params['n_blocks']*params['resolution'])), [0], [1.01], color='0.55', linestyles='dashed' )
if params['n_blocks']>1:
    pl.vlines( np.arange(len_gpi/(3*params['n_blocks']), len_gpi/3-1., len_habit/(3*params['n_blocks']) ), [mini], [maxi], color='0.55', linestyles='dashed' )
pl.legend()
pl.tight_layout()


pl.show()


