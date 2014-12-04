# times
if RANK==0:
    exc_sptimes = nest.GetStatus(exc_spike_recorder)[0]['events']['times']
    for i_proc in xrange(1, SIZE):
       exc_sptimes = np.r_[exc_sptimes, COMM.recv(source=i_proc)]
else:
    COMM.send(nest.GetStatus(exc_spike_recorder)[0]['events']['times'],dest=0)

#ids
if RANK==0:
    exc_spids = nest.GetStatus(exc_spike_recorder)[0]['events']['senders']
    for i_proc in xrange(1, SIZE):
        exc_spids = np.r_[exc_spids, COMM.recv(source=i_proc)]
else:
    COMM.send(nest.GetStatus(exc_spike_recorder)[0]['events']['senders'],dest=0)

#plot
if RANK==0:
    pl.scatter(exc_sptimes, exc_spids,s=1.)
