#!/bin/bash      

echo "Running fastuniq"
for dir in $(ls);
do cd $dir;
ls > /tmp/forFastUniq.txt;
/local/home/sarahgw/FastUniq/fastuniq -i /tmp/forFastUniq.txt -t q -o $(pwd)/"$dir"_FU1.fastq -p $(pwd)/"$dir"_FU2.fastq;
cd ..;
done

echo "Trimming"
for dir in $(ls); 
do cd $dir; 
java -jar /local/home/sarahgw/Trimmomatic-0.36/trimmomatic-0.36.jar PE -phred33 $(pwd)/"$dir"_FU1.fastq $(pwd)/"$dir"_FU2.fastq $(pwd)/"$dir"_FU1_trim_p.fastq $(pwd)/"$dir"_FU1_trim_up.fastq $(pwd)/"$dir"_FU2_trim_p.fastq $(pwd)/"$dir"_FU2_trim_up.fastq ILLUMINACLIP:/local/home/sarahgw/Trimmomatic-0.36/adapters/NexteraPE-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:30; 
cd ..; 
done

echo "Counting paired"
for dir in $(ls); 
do cd $dir;
grep -c '@' $(pwd)/"$dir"_FU1_trim_p.fastq>> /local/home/sarahgw/WGS/Sequences/Metrics/Pool8_reads;
cd ..; done 

echo "Counting unpaired1"
for dir in $(ls); 
do cd $dir; 
grep -c '@' $(pwd)/"$dir"_FU1_trim_up.fastq>> /local/home/sarahgw/WGS/Sequences/Metrics/Pool8_readsFU1up; 
cd ..; 
done 

echo "Counting unpaired2"
for dir in $(ls); 
do cd $dir; 
grep -c '@' $(pwd)/"$dir"_FU2_trim_up.fastq>> /local/home/sarahgw/WGS/Sequences/Metrics/Pool8_readsFU2up; 
cd ..; 
done 

echo "Running FastqScreen on paired"
for dir in $(ls); 
do cd $dir; 
/local/home/sarahgw/fastq_screen_v0.9.5/fastq_screen --subset 0 --tag --aligner Bowtie2 $(pwd)/"$dir"_FU1_trim_p.fastq $(pwd)/"$dir"_FU2_trim_p.fastq; 
cd ..; 
done

echo "Running FastqScreen on unpaired"
for dir in $(ls); 
do cd $dir; 
/local/home/sarahgw/fastq_screen_v0.9.5/fastq_screen --subset 0 --tag --force --aligner Bowtie2 $(pwd)/"$dir"_FU1_trim_up.fastq $(pwd)/"$dir"_FU1_trim_up.fastq; 
cd ..; 
done

echo "Filtering unpaired1"
for dir in $(ls); 
do cd $dir; 
/local/home/sarahgw/fastq_screen_v0.9.5/fastq_screen --subset 0 --tag --filter 00000 --force --aligner Bowtie2 $(pwd)/"$dir"_FU1_trim_up.fastq; cd ..; 
done

echo "Filtering unpaired2"
for dir in $(ls); 
do cd $dir; 
/local/home/sarahgw/fastq_screen_v0.9.5/fastq_screen --subset 0 --tag --filter 00000 --force --aligner Bowtie2 $(pwd)/"$dir"_FU2_trim_up.fastq; 
cd ..; 
done

echo "Filtering paired"
python ~/Notebooks/WNS_WGS/pfilter.py 


