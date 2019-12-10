# Reference-liftover

//  Created by Walfred MA in 2019, wangfei.ma@ucsf.edu.
//  Copyright © 2019 UCSF-Kwoklab. All rights reserved.


-------Introduction-------



This is a python2.7 script. It has two main functions 1. replace specified regions of the reference sequence and 2. Liftover coordinates between original and new references:

For function 2, we are also providing a records to transfer the coordinates between our new human diversity reference and the old reference (hg38).




-------First_function-------




replace specified regions of the reference sequence:

This takes up to three files: 
1. Reference file;
2. patch file (the sequence to be incorporated into new reference with designated coordinates);
3. (optional) Previous records that includes all past changes of the reference;

It has following features:

1.	It will load all patch files, replace/insert the designated regions on the referebce with the patches. 
2.	It will update the coordinates after each correction. After finishing all correction, it saves final coordinates to a new record file.
3.	It will automatically check for any overlap of fix patches (including the input patches and prior patches in previous records). It will choose the largest one among all overlapped patches.





-------Second_function-------

coordinate transferring:

This takes two files: 
1. designated query coordinated in old reference;  
2. Previous records that includes all past changes of the reference. 

By default, it takes old coordinates (coordinates before changes in previous records) as the query, and output new coordinates (coordinates after changes in previous records), based on previous records.

If -R presents, it reversely takes new coordinate as the query, as output old coordinates based on previous records.

The algorithm has been optimized to work will large dataset.



-------Formats & Requirements-------



Function 1:

1.	Both reference and patch files need to be fasta files. 
2.	The coordinates of each patch should be stated in title of each contig.
e.g: 

>Chr1:100-1000
AAATCAACCGCGC


Notes:
-Coordinate is zero-based and left cap and right open
-if start position is after stop position, the script will treat this as tandem expansion, and thus will duplicate the region between start and stop sites.






Function 2:

1.	All coordinates must follow chromosome:coordinate. E.g: chr1:2000, Chr:20000(chr1 or Chr1 will be treat as the same chromosome, but CHR1 will not).

2.	The patch file’s coordinates should be separated into each line. <br>
E.g: <br>
Chr1:20000 <br>
Chr1:232020

3.	If direct input, please use “,” as the delimiter. 
4.	For output coordinates file, query coordinates are the first column and output coordinates are the second column. 


It accepts a tsv record file (option -l) that includes all past correction.

Titles should be:

'#name': name of each patch.
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

Python2.7 fix_step2.py –l record.tsv  -c query_coordinates [-n output_coordinates.txt]

Or 

Python2.7 fix_step2.py –l record.tsv  -c chr1:10000,chr1:1000000,chr2:200000   [-n output_coordinates.txt]





-------Options-------





Function 1 (This is the default function and will be disabled with –c):

Arguments required:

-f			input patch files to update the reference

-r			reference genome that will be updated. Can be either a fasta file or folder contains all contigs files (format needs to be *.fa)

Arguments optional:

-l			(optional) input records tsv file which contains all information of prior corrections, default will be ./fixed_records.tsv.

-s			saved path, default will be ./step2_fixed. If input is folder then save will be folder; if input is a fasta file, saves will be a fasta file.

-n			new records file save path after corrections. 






Function 2 (this function will be enable with –c) :

Arguments required:

-c			query coordinates, can be either a file or direct input (when directly input coordinates, please make sure this is no file with the same name).

-l			tsv record file that records all previous corrections. 

Arguments optional:

-n			output coordinates file save path. default file is ./newcoordinates.txt.


