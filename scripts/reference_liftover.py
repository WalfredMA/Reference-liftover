#!/usr/bin/python1.7

import os
import pandas as pd
import re
import collections as cl
import time
import Queue
import sys
import getopt
import numpy as np

def usage():
	
	print 
	
	'''
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
	'''


def inputallchroms(chromefolder):
		
	seqs={}
	titles={}
	
	if inputisfile==1:
		
		with open(chromefolder,mode='r') as f:
		
			reads=f.read().split('>')[1:]
	
		f.close()

		for read0 in reads:
			
			titles[read0.split('\n')[0].split('\s')[0].strip().replace('Chr','chr')]=read0.split('\n')[0]
			seqs[read0.split('\n')[0].split('\s')[0].strip().replace('Chr','chr')]=''.join(read0.split('\n')[1:]).strip()
		
		
	else:
		
		for x in os.listdir(chromefolder):

			with open(chromefolder+x,mode='r') as f:

				read=f.read().splitlines()
				titles[x.split('.')[0].replace('Chr','chr')]=read[0]				
				seqs[x.split('.')[0].replace('Chr','chr')]=''.join(read[1:])

			f.close()

	return titles,seqs


def readlog(logfile):
	
	records=cl.defaultdict(list)

	try:
		t0=pd.read_csv(logfile,sep='\t',header=None,comment='#')
	
	except:
		
		return records
	
	readrecords=t0.values.tolist()

	for record in readrecords:
		
		if len(record[1])<3:
			record[1]='chr'+record[1]

		records[record[1]].append(record)
	
	return records
	

def findcordi(cordi, record,length=0 ,checkoverlap=1):
		

	if len(record)==0:

		return cordi,[]


	

	if ifreverse==-1:

		record=[x[:2]+x[4:6]+x[2:4]+x[6:] for x in record]
		

	allstarts=[x[2] for x in record]

	allstops=[x[3] for x in record]


	fixpatchsizes=[x[6] for x in record]


	##caluclate replaced sizes. if it is tendem expansion, then the size is minus.

	if ifreverse==-1:
		replacedsizes=[x[5]-x[4] for x in record]
	else:
		replacedsizes=[x[3]-x[2] for x in record]

	##calculate the size change (coordinate shift) of the reference, = inserted size - replaced size
		
	##check for if there is any overlaps when the option is designated in arguements
	if checkoverlap==1:
		
		overlaps=[i for i,x in enumerate(zip(allstarts,allstops)) if min(x)<max(cordi) and max(x)>min(cordi)]

	else:

		overlaps=[]


	if len(overlaps)>0:
		
		print 'overlap notice!!!!\n',[record[i] for i in overlaps]

		if length<=max([record[i][6] for i in overlaps]):

			return [-1,-1],[]

		else:

			record=[x for i,x in enumerate(record) if i not in overlaps]

			if len(record)==0:

				return cordi, overlaps

	##re-calculate everything after filtering overlaps


	allstarts=[x[2] for x in record]

	allstops=[x[3] for x in record]


	fixpatchsizes=[x[6] for x in record]

	if ifreverse==-1:
		replacedsizes=[x[5]-x[4] for x in record]
	else:
		replacedsizes=[x[3]-x[2] for x in record]

	cordishifts=[ifreverse*(x-y) for x,y in zip(fixpatchsizes, replacedsizes)]


	l0=len(allstarts)
	l1=len(allstarts)+len(allstops)
	

	##those are all coordinates will be corrected, and we sort them first
	allcordis=allstarts+allstops+cordi

	sort_keys=sorted(range(len(allcordis)), key=lambda x: allcordis[x])
	
	
	newcordi=[x for x in cordi]
	

	##a loop to edit and correct coordinates based on coordiate thift (difference between original coordinate and post-fixation coordinate

	cordi_fix=0
	for i,key in enumerate(sort_keys):
		
		#if this is the coordinates of input query, then correct base on coordinate shift
		if key>=l1:

			newcordi[key-l1]=cordi[key-l1]+cordi_fix
		

		##if this is a start position from record, then first correct the coordinate and store in record, then update the coordiate shift.
		elif key<l0:

			record[key][4]=record[key][2]+cordi_fix
			
			#we only update the coordinate shift when the start site is after the stop site
			if record[key][3]<record[key][2]:

				cordi_fix=cordi_fix+cordishifts[key]	
		
		##if this is a stop position from record, then first correct the coordinate and store in record, then update the coordiate shift.
		else:

			##only update coordiate when stop site is after start site
			if record[key-l0][3]>=record[key-l0][2]:

				cordi_fix=cordi_fix+cordishifts[key-l0]

				record[key-l0][5]=record[key-l0][3]+cordi_fix
	
			else:
				
				record[key-l0][5]=record[key-l0][2]+cordi_fix+cordishifts[key-l0]


	

	return newcordi,overlaps



def cleanoverlap(seq0, record, overlaps):



	already_fixed=[]
	newrecord=[]


	#loop to clean overlap patches
	for i in sorted(overlaps):

		#locate each patches from records, and find coordinates on reference
		
		eachoverlap=record[i-len(already_fixed)]

		cordi_onseq=eachoverlap[4:6]

		#clean the patches

		seq=seq[:cordi_onseq[0]]+seq[cordi_onseq[1]:]

		already_fixed.append(i)

		#clean the record		

		record=[x for i0,x in enumerate(record) if i0 != i-len(already_fixed)]

			
		#update the coordinates after each clean

		findcordi([0,0],record, 0,0)

	return seq, record




def eachpatch(name0,file0,records,seqs):

	#find information from the title
	title=file0.splitlines()[0]
	
	fix_seq=''.join(file0.splitlines()[1:])
	
	chrome=title.split(':')[0].replace('Chr','chr')
	
	cordi=[int(x) for x in title.split(':')[1].split('-')]


	#update all coordinaets in record and find coordinates for fixation (this coordinate may change if addtional patches come
	newcordi,overlaps=findcordi(cordi,records[chrome], len(fix_seq))

	#if there is overlap and this patch is too small to be use, then abort
	if newcordi[0]==-1:

		return 0

	#if there is overlap and this patch is the largest, then clean prior patches
	elif len(overlaps)>0:

		seq0, newrecord=cleanoverlap(seqs[chrome], records[chrome], overlaps)

		seqs[chrome]=seq0

		records[chrome]=newrecord

	#add patches to the reference 
	seqs[chrome]=seqs[chrome][:newcordi[0]]+fix_seq+seqs[chrome][newcordi[1]:]

	#add information to the record
	records[chrome].append([name0, chrome]+cordi+newcordi+[len(fix_seq)])
	
	print [name0, chrome]+cordi+newcordi+[len(fix_seq)]


	return 0


def updaterecords(records):

	allrecords=[x for chrom,records in records.items() for x in records  ]

	table=pd.DataFrame.from_records(allrecords)

	table.sort_values([1,4],ascending=[True,True])

	table.to_csv(newrecord,mode='w',index=False, header=['#name', 'chr', 'start_hg38', 'stop_hg38', 'start_fixed', 'stop_fixed', 'fixsize'],sep='\t')


def save(titles,seqs):
	
	if inputisfile ==1 :


		with open(svfolder, mode='a') as f:
			
			for name  in sorted(seqs.keys()):

				f.write('>'+titles[name]+'\n'+seqs[name]+'\n')

		f.close()


	else:
		for name,seq  in seqs.items():

			with open(svfolder+name+'.fa', mode='w') as f:

				f.write(titles[name]+'\n'+seq)

			f.close()



def fixall():
	
	#input all references 
	titles, seqs=inputallchroms(reference_folder)


	#input all records
	records=readlog(logfile)
	
	#input all patches
	with open(inputfile, mode='r') as f:
		
		reads=f.read().split('>')[1:]
	
	f.close()

	#sorted patches based on sizes to fix larger patches first
	reads=sorted(reads, key=lambda x: len(x.strip()), reverse=True)

	#loop to fix
	for i,eachfile in enumerate(reads):

		eachpatch('fix_'+str(i),eachfile.strip(),records,seqs)

	#final update coordinates
	for record in records.values():

		findcordi([0,0], record ,0 ,0 )

	#output records

	updaterecords(records)

	#save reference
	save(titles,seqs)


	return records


def outputcoordi():

	#read records
	records=readlog(logfile)


	#organize and sort all coordinates and combine coordinates on the same chromosome
	coordis_eachchrom=cl.defaultdict(list)

	index_eachchrom=[]

	for coordi in allcoordis:

		coordis_eachchrom[coordi[0]].append(coordi[1])

		index_eachchrom.append(len(coordis_eachchrom[coordi[0]])-1)


	#calculate new coordinates
	newcoordis_eachchrom={}

	for chr0, cordi in coordis_eachchrom.items():
		newcoordis_eachchrom[chr0]=findcordi(cordi, records[chr0],0,0)[0]


	#organize new coordinates to the same order with the old coordinates
	newcoordis=[]
	for (index,coordi) in zip(index_eachchrom,allcoordis):

		newcoordis.append(coordi[0]+':'+str(newcoordis_eachchrom[coordi[0]][index]))		

	print newcoordis

	global num_coordi_perline

	if num_coordi_perline==[]:
		num_coordi_perline=[1 for x in newcoordis]

	if outputbed==1:

		with open(outputbedfile, mode='w') as f:

			current_index=0
			for num in num_coordi_perline:
				out=str(newcoordis[current_index]).split(':')[0]+'\t'+'\t'.join([str(x).split(':')[1] for x in newcoordis[current_index:(num+current_index)]])+'\n'

				current_index=current_index+num

				f.write(out)

		f.close()


	#output 
	if outnewrecord==1:

		with open(newrecord, mode='w') as f:

			f.write('\n'.join([x[0]+":"+str(x[1])+'\t'+str(y) for x,y in zip(allcoordis,newcoordis)]))

		f.close()

if __name__=="__main__":
	
	reference_folder='./fixed/'

	logfile='./fixed_records.tsv'

	svfolder='./step2_fixed/'

	newrecord='./fixed_records_step2.tsv'

	outnewrecord=0

	mode=0

	outputbed=0

	outputbedfile=''

	num_coordi_perline=[]

	ifreverse=1
	
	try:
		opts,args=getopt.getopt(sys.argv[1:],"f:r:l:s:n:c:b:o:R")
	except getopt.GetoptError:
		usage()
		sys.exit(2)

	if not len(sys.argv[1:]):
		
		usage()
		sys.exit(2)

	for op, value in opts:
		if op=='-f':
			inputfile=value
		if op=='-r':
			reference_folder=value
		elif op=='-l':
			logfile=value
		elif op=='-s':
			svfolder=value
		elif op=='-c':
			mode=1
			inputcordi=value
			newrecord='./newcoordinates.txt'
		elif op=='-n':
			outnewrecord=1
			newrecord=value
		elif op=='-b':
			outputbed=1
			outputbedfile=value
		elif op=='-R':
			ifreverse=-1
		elif op in ('-h', '--help'):
			usage()
			sys.exit(2)
		else:
			usage()
			sys.exit(2)		

	#preparation for the input arguements


	if mode==1:

		allcoordis={}

		if os.path.isfile(inputcordi):


			with open(inputcordi, mode='r') as f:

				allcoordis=[[[x.strip().split('\t')[0].replace('Chr','chr'),int(a)] for a in x.strip().split('\t')[1:]] if ":" not in x  else  [[x.strip().split(':')[0].replace('Chr','chr'),int(x.strip().split(':')[1])]] for x in f.read().splitlines() if len(x)>0 and x[0]!="#"] 

				num_coordi_perline=[len(x) for x in allcoordis]
					
				allcoordis=[a for x in allcoordis for a in x]

				
			f.close()		

		else:
			allcoordis=[[x.split(':')[0].replace('Chr','chr'), int(x.split(':')[1])] for x in inputcordi.split(',')] 


	else:
		
		if os.path.isfile(reference_folder):
			
			inputisfile=1

		else:
				
			inputisfile=0

			try:
				os.mkdir(svfolder)
			except:
				pass

	if mode==0:

		records=fixall()

	elif mode==1:

		outputcoordi()		
