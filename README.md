# Reference-liftover


-------Introduction-------

This is a python2.7 script. It has two main functions 1.reference fixation and 2. Coordinate transferring between pre-fixation and after-fixation:

-First, reference fixation:

it adds fixations to designated reference. It has following features:

1.	It will replace the labeled regions with the fixed sequences. After it fixes all regions, it will output to designed folder (per file each contig). 
2.	It will update the coordinates after each fixation and output to designed record file after finish.
3.	It will automatically check for any overlap of fix patches (including the designated patches and prior patches in the record file). After find all overlap, it will choose the largest one.

-Second, coordinate transferring:

when input with coordinates, it can calculate new coordinates based on records of fixations. The algorithm has been optimized to work will large dataset.


-------Formats & Requirements-------


Function 1:
1.	Both reference and input files need to be fasta files. 
2.	The coordinates of each insertion should be stated in title of each contig.
e.g: 

>Chr1:100-1000
AAATCAACCGCGC


Notes:
-Coordinate is zero-based and left cap and right open
-if start position is after stop position, the script will treat this as tandem expansion, and thus will duplicate the region between start and stop sites.

Function 2:

1.	All coordinates must follow chromosome:coordinate. E.g: chr1:2000, Chr:20000(chr1 or Chr1 will be treat as the same chromosome, but CHR1 will not).

2.	The input file’s coordinates should be separated into each line. 
E.g: 
Chr1:20000
Chr1:232020

3.	If direct input, please use “,” as the delimiter. 
4.	Old coordinates are the first column of output file and the new coordinates are the second column. 


It also accepts a tsv record file (option -l) that includes all past fixations.

Titles should be:

'#name': name of each fixation.
'chr': fixed contig (chromosome)
'start_hg38':start base on reference
'stop_hg38':stop base on reference 
'start_fixed':start base on post-fix sequence
'stop_fixed':stop base on post-fix sequence
'fixsize':size of the patch sequence



-------Usage-------

Please run the script with python2.7 through commend line. 

Example of function 1:

Python2.7 fix_step2.py –f input_insertion.fa –r hg38.fa [-l records.tsv] [-s savefile.fa] [-n newrecords.tsv]

Example of Function 2:

Python2.7 fix_step2.py –l record.tsv  -c oldcoordinates.txt   [-n newcoordinates.txt]

Or 

Python2.7 fix_step2.py –l record.tsv  -c chr1:10000,chr1:1000000,chr2:200000   [-n newcoordinates.txt]





-------Options-------

Function 1 (This is the default function and will be disabled with –c):

Arguments required:

-f			input insertion file to fix the reference

-r			reference genome that will be fixed. Can be either a fasta file or folder contains all contigs files (format needs to be *.fa)

Arguments optional:

-l			input records tsv file which contains all information of prior fixations, default will be ./fixed_records.tsv. records file can be missed.

-s			saved file, default will be step2_fixed. If input is folder then save will be folder, also input is fasta file, save will be fasta file.

-n			saved new records after fixations. 


Function 2 (this function will be enable with –c) :

Arguments required:

-c			input coordinates, can be either a file or direct input (when directly input coordinates, please make sure this is no file with same name).

-l			Tsv record file that records all fixations

Arguments optional:

-n			save new calculated coordinates. If a path indicated, will output to the path otherwise it will output to default file newcoordinates.txt. 

