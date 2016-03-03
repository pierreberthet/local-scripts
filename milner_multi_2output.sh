#! /bin/bash

rm Test/Multi/*
rm Test/Parameters/*
rm Test/Data/*

rm simulation_parameters.*

#if [ $1 == 'pdf' ]:

#    then
rm *.pdf
scp berthet@milner.pdc.kth.se:/cfs/milner/scratch/b/berthet/code/temp/*.pdf .
qpdfview *.pdf &
#fi

#test $1 == 'pdf' && (rm *.pdf ; scp berthet@milner.pdc.kth.se:/cfs/milner/scratch/b/berthet/code/temp/*.pdf . ; qpdfview *.pdf )


scp berthet@milner.pdc.kth.se:/cfs/milner/scratch/b/berthet/code/temp/Test/Multi/* Test/Multi/.
scp berthet@milner.pdc.kth.se:/cfs/milner/scratch/b/berthet/code/temp/Test/Data/* Test/Data/.
scp berthet@milner.pdc.kth.se:/cfs/milner/scratch/b/berthet/code/dopabg/simulation_parameters.py .

scp berthet@milner.pdc.kth.se:/cfs/milner/scratch/b/berthet/code/temp/Test/Parameters/* Test/Parameters/.

python multi_stats_auto.py &


