from os import listdir, path
from multiprocessing.pool import ThreadPool
import subprocess
import sys

site = sys.argv[1]

def run_angsd(filename):
    
    # Runs angsd for each snp and 100 bootstrapped files
    for i in range(100):
        snp_idx = filename.split('_')[-1]
        bs_file = '/local/home/sarahgw/WGS/SNPS/All_mylu/mafs/FiltFiles/{}_Bootstrapped_Filelists/{}_{}'.format(site, filename, i+1)
        chrom_file = '/local/home/sarahgw/WGS/SNPS/All_mylu/snps/{}_chrom_files/{}_chrom.txt'.format(site, snp_idx)
        site_ref_file = '/local/home/sarahgw/WGS/SNPS/All_mylu/snps/{}_sites_files/{}_sites.txt'.format(site, snp_idx)
        output_file = '/local/home/sarahgw/WGS/SNPS/All_mylu/mafs/{}_Bootstrapped_mafs/tmp/{}_{}'.format(site, filename, i+1)
        cmd = "/local/home/sarahgw/angsd/angsd/angsd -b {} -GL 1 -doMajorMinor 3 -doMaf 11 -doCounts 1 -P 20 -rf {} -sites {} -out {}".format(bs_file, chrom_file, site_ref_file, output_file)
        subprocess.call(cmd.split())
        
        #Delete this
        #raise Exception('done')
        
files = listdir('/local/home/sarahgw/WGS/SNPS/All_mylu/mafs/FiltFiles/{}_Site_SNPS_Data/'.format(site))

for f in list(files):
    if path.isfile('/local/home/sarahgw/WGS/SNPS/All_mylu/mafs/{}_Bootstrapped_mafs/tmp/{}_100.arg'.format(site, f)):
        # print "done {}".format(f)
        files.remove(f)
pool = ThreadPool(10)
print files[:2]
pool.map(run_angsd, files)

#for i in range(len(files)):
#    f = files[i]
#    print "{}: Running angsd for {}".format(i, f)
#    run_angsd((site, f))  
