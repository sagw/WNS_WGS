from Bio import SeqIO
from os import listdir

import threading
import Queue
import gc
import traceback

def pfilter(in1, in2, out1, out2, name):
    """
    Takes string file handles
    """
    
    print 'combined filtering ' + name + ' ... '
    print in1
    print in2
    print out1
    print out2

    f1 = SeqIO.parse(in1, 'fastq')
    f2 = SeqIO.parse(in2, 'fastq')
    
    seqs1 = []
    seqs2 = []
    count= 0
    seq1 = ''
    seq2 = ''
    check = '00000'

    while True:
        try:
            seq1 = f1.next()
            seq2 = f2.next()
        except:
            break
            
        tag1 = seq1.description[-5:]
        tag2 = seq2.description[-5:]
        
        if tag1 == check and tag2 == check:
            seqs1.append(seq1)
            seqs2.append(seq2)
            count += 1

        if count == 100000:
            o1 = open(out1, 'a')
            o2 = open(out2, 'a')
            SeqIO.write(seqs1, o1, 'fastq')
            SeqIO.write(seqs2, o2, 'fastq')
            o1.close()
            o2.close()
            seqs1 = []
            seqs2 = []
            count = 0
            
    
    o1 = open(out1, 'a')
    o2 = open(out2, 'a')
    SeqIO.write(seqs1, o1, 'fastq')
    SeqIO.write(seqs2, o2, 'fastq')
    o1.close()
    o2.close()

    print 'finished ' + name



class worker(threading.Thread):

    def __init__(self, queue):
        super(worker, self).__init__()
        self._queue = queue

        self.setDaemon(False) #  Threads should finish
        self.alive = threading.Event()
        self.alive.set()

    def run(self):
        while self.alive.isSet():
            try:
                msg = self._queue.get(True, 0.1)
                print "{} folders remaining".format(self._queue.qsize())
                pfilter(msg[0], msg[1], msg[2], msg[3], msg[4])
            except Queue.Empty as e:
                break
            except Exception as e:
                traceback.print_exc()
                continue


#
#
# EDIT THIS STUFF
#
#            

# File directory
roo = '/local/home/sarahgw/WGS/Sequences/Pool10/'
#roo = '/local/home/sarahgw/Downloads/'

# Infile suffix
in_s1 = '_FU1_trim_p.tagged.fastq'
in_s2 = '_FU2_trim_p.tagged.fastq'

# Outfile suffix
out_s1 = '_FU1_trim_p.tagged_pfilter.fastq'
out_s2 = '_FU2_trim_p.tagged_pfilter.fastq'

# Number of thread workers
num_threads = 5

#
#
# Don't edit this stuff
#
#

# Get all names
dirs = listdir(roo)

# Temporary overrides
#dirs = ['NY_U_23']
print(dirs)
jobs = Queue.Queue()
for name in dirs:
    in1 = roo + name + '/' + name + in_s1
    in2 = roo + name + '/' + name + in_s2
    out1 = roo + name + '/' + name + out_s1
    out2 = roo + name + '/' + name + out_s2
    
    job = [in1, in2, out1, out2, name]
    jobs.put(job)


threads = []
for i in range(num_threads):
    w = worker(jobs)
    threads.append(w)
    w.start()


while True:
    if jobs.empty():
        break
