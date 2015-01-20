#! /bin/bash

rm fig*.pdf
rm Test/Spikes/*
rm Test/Parameters/*
rm simulation_parameters.*

scp berthet@milner.pdc.kth.se:/cfs/milner/scratch/b/berthet/code/temp/fig* .

scp berthet@milner.pdc.kth.se:/cfs/milner/scratch/b/berthet/code/dopabg/simulation_parameters.py .
scp berthet@milner.pdc.kth.se:/cfs/milner/scratch/b/berthet/code/temp/Test/Spikes/*merged*spikes* Test/Spikes/.
scp berthet@milner.pdc.kth.se:/cfs/milner/scratch/b/berthet/code/temp/Test/Parameters/* Test/Parameters/.

qpdfview fig*.pdf &
#python MergeSpikefiles.py

python fullplot.py


