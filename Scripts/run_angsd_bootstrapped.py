import subprocess
from os import listdir, path
from multiprocessing.pool import ThreadPool

def run_angsd(filename):
    # Runs angsd for each snp and 100 bootstrapped files
    for i in range(100):
        snp_idx = filename.split('_')[-1]
        bs_file = '/local/home/sarahgw/WGS/SNPS/All_mylu/mafs/FiltFiles/Bootstrapped_Filelists/{}_{}'.format(filename, i+1)
        chrom_file = '/local/home/sarahgw/WGS/SNPS/All_mylu/snps/chrom_files/{}_chrom.txt'.format(snp_idx)
        site_ref_file = '/local/home/sarahgw/WGS/SNPS/All_mylu/snps/sites_files/{}_sites.txt'.format(snp_idx)
        output_file = '/local/home/sarahgw/WGS/SNPS/All_mylu/mafs/Bootstrapped_mafs/tmp/{}_{}'.format(filename, i+1)
        cmd = "/local/home/sarahgw/angsd/angsd/angsd -b {} -GL 1 -doMajorMinor 3 -doMaf 11 -doCounts 1 -P 20 -rf {} -sites {} -out {}".format(bs_file, chrom_file, site_ref_file, output_file)
        subprocess.call(cmd.split())
        
        # Delete this
        # raise Exception('done')

files = listdir('/local/home/sarahgw/WGS/SNPS/All_mylu/mafs/FiltFiles/Site_SNPS_Data/')

for f in list(files):
    if path.isfile('/local/home/sarahgw/WGS/SNPS/All_mylu/mafs/Bootstrapped_mafs/{}_100.arg'.format(f)):
        # print "done {}".format(f)
        files.remove(f)

pool = ThreadPool(10)
print files[:2]
pool.map(run_angsd, files)
# for i in range(len(files)):
#    f = files[i]
#    print "{}: Running angsd for {}".format(i, f)
#    run_angsd(f)  
    
