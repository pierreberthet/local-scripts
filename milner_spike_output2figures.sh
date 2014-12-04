#! /bin/bash

rm fig*.pdf
rm Test/Spikes/*
rm Test/Parameters/*

scp berthet@milner.pdc.kth.se:/cfs/milner/scratch/b/berthet/code/temp/fig* .

scp berthet@milner.pdc.kth.se:/cfs/milner/scratch/b/berthet/code/temp/Test/Spikes/*merged*spikes* Test/Spikes/.
scp berthet@milner.pdc.kth.se:/cfs/milner/scratch/b/berthet/code/temp/Test/Parameters/* Test/Parameters/.

qpdfview fig*.pdf &
#python MergeSpikefiles.py

python fullplot.py


