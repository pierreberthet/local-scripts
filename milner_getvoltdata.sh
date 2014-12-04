#! /bin/bash

rm Test/Spikes/*volt*
rm Test/Parameters/*


scp berthet@milner.pdc.kth.se:/cfs/milner/scratch/b/berthet/code/temp/Test/Spikes/*merged*volt* Test/Spikes/.
scp berthet@milner.pdc.kth.se:/cfs/milner/scratch/b/berthet/code/temp/Test/Parameters/* Test/Parameters/.

#python MergeVoltfiles.py

#python 


