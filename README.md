# Reference-liftover

//  Created by Walfred MA in 2019, wangfei.ma@ucsf.edu. <br>
//  Copyright © 2019 UCSF-Kwoklab. All rights reserved.


-------Introduction-------



This tool is written in python2.7 and it has two functions: 1. it edits reference sequences based on a user's input and 2. it converts coordinates between two reference versions. We expect most users to be using only function 2. 

-------First_function (Not applicable to most users)-------

This function accepts up to three input files: 
1. Reference fasta file to be edited
2. Patch fasta file containing sequences to be incorporated into item #1
3. (Optional) Previous editing history file that records all past changes made to item #1

Specific features:

1.	It edits the reference sequences based on users' desired sequences, as provided in them #2
2.	It updates the sequence coordinates after each edit. After editing, the final coordinates are output to a record file
3.	It automatically checks for any overlap between patches (including the input patches and prior patches stored in previous records). It will choose the largest one among all overlapping patches.

-------Second_function-------

This function accepts two input files: 
1. Query coordinates to be converted (can either be a direct input in the command or an input file)
2. Previous editing records that includes all past changes to the reference. For conversion between Hg38 and the Human Diversity Reference, the record file is provided in this repository (./records/record_all_chr.tsv.gz). Please unzip before use.

By default, the tool assumes that the query coordinate is based on the pre-edited reference (Hg38) and it converts the coordinate to the post-edited reference (HDR). If **-R** is used, the query coordinate is assumed to be HDR.

The algorithm has been optimized to work with large dataset.

-------Formats & Requirements-------

Function 1:

1.	Both reference and patch files need to be fasta files. 
2.	The desired placement of each patch is the title of each contig.
e.g: 

>Chr1:100-103
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

Python2.7 reference_liftover.py –f patch.fa –r hg38.fa [-l records.tsv] [-s edited_hg38.fa] [-n newrecords.tsv]

Example of Function 2:

Python2.7 reference_liftover.py –l [record.tsv]  -c query_coordinates [-n output_coordinates.txt]

Or 

Python2.7 reference_liftover.py –l [record.tsv]  -c chr1:10000,chr1:1000000,chr2:200000   [-n output_coordinates.txt]





-------Options-------





**Function 1 (This is the default function and will be disabled with –c):**

Arguments required:

-f			input patch file to edit the reference

-r			reference genome that will be edited. Can be either a fasta file or a folder containing all contigs files (format must be *.fa)

Arguments optional:

-l			(optional) input records tsv file which contains all information of previous corrections, default will be ./fixed_records.tsv

-s			saved path, default will be ./step2_fixed. If input is folder then save will be folder; if input is a fasta file, saves will be a fasta file

-n			new records file save path after corrections


**Function 2 (this function will be enabled with –c) :**

Arguments required:

-c			query coordinates, can be either a file or a direct input (if using a direct input, please make sure this is no file with the same name)

-l			tsv record file that records all previous corrections

Arguments optional:

-n			output coordinates file save path. default file is ./newcoordinates.txt

-R      query coordinates are based on the post-edited reference file


