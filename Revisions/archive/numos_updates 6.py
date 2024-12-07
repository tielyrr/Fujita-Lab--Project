import os
import subprocess
import csv
import pymysql
import numpy as np
from Bio.SeqIO import parse
import itertools 


conn = pymysql.connect(  #connection to sql
        host='localhost',
        user='root',
        password='Abc12345',
        db='ncbi',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
        local_infile = True)



class numos(): 
    def __init__(self):
        self.self = self
        self.sp_path = ''#'/Users/biollab-120475/Desktop/ncbi_dataset/data/GCA_020142125.1/ncbi_dataset/data' #path to accession folder with gff and fna
        self.sp_id = ''#'GCA_020142125.1'
        self.c_id = '' #chromosome id, will reset with each iteration of the loop
        self.chrom_end = ''
        self.gene_ss = {} #start/stop lists
        self.exon_ss = []

    def files(self): #write all files to be used for bulk inserts so functions can access and append to them as needed
        #change directory to sql uploads
        os.chdir('/Users/biollab-120475/mysqlUploads')
        with open('gene_records.tsv', 'w', newline='') as tsvfile:
            writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
            fieldnames = ['accession_id','chrom_id', 'gene_id', 'g_strand', 'g_seq_start', 'g_seq_end']
            writer = csv.DictWriter(tsvfile, fieldnames=fieldnames)
            writer.writeheader()
        with open('exon_records.tsv', 'w', newline='') as tsvfile:
            writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
            fieldnames = ['accession_id','chrom_id', 'gene_id', 'exon_id','exon_strand', 'exon_seq_start', 'exon_seq_end']
            writer = csv.DictWriter(tsvfile, fieldnames=fieldnames)
            writer.writeheader()
        with open('cds_records.tsv', 'w', newline='') as tsvfile:
            writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
            fieldnames = ['accession_id','chrom_id', 'gene_id', 'cds_id', 'cds_strand', 'cds_seq_start', 'cds_seq_end']
            writer = csv.DictWriter(tsvfile, fieldnames=fieldnames)
            writer.writeheader()
        with open('window_records.tsv', 'w', newline='') as tsvfile:
            writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
            fieldnames = ['accession_id','chrom_id', 'wind_id', 'wind_seq_start', 'wind_seq_end', 'gene_count']
            writer = csv.DictWriter(tsvfile, fieldnames=fieldnames)
            writer.writeheader()
        with open('intron_records.tsv', 'w', newline='') as tsvfile:
            writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
            fieldnames = ['accession_id','chrom_id', 'gene_id', 'intron_id', 'intron_strand', 'intron_seq_start', 'intron_seq_end']
            writer = csv.DictWriter(tsvfile, fieldnames=fieldnames)
            writer.writeheader()
        with open('igs_records.tsv', 'w', newline='') as tsvfile:
            writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
            fieldnames = ['accession_id','chrom_id', 'igs_id', 'igs_seq_start', 'igs_seq_end'] #not including a strand column rn
            writer = csv.DictWriter(tsvfile, fieldnames=fieldnames)
            writer.writeheader()
        with open('flank_records.tsv', 'w', newline='') as tsvfile:
            writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
            fieldnames = ['accession_id','chrom_id', 'gene_id','flank_id', 'flank_strand','up_start', 'up_stop', 'down_start', 'down_stop'] #not including a strand column rn
            writer = csv.DictWriter(tsvfile, fieldnames=fieldnames)
            writer.writeheader()
            
    def upload(self, filepath, fields, table): #bulk insert to sql -- ***adjust database name if changed
        with conn.cursor() as cursor:
            cursor.execute(f"LOAD DATA LOCAL INFILE '{filepath}' INTO TABLE ncbi.{table} FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n' IGNORE 1 LINES ({fields});")
            conn.commit()
        #will need to do data transformations probably here as well
        return None #a successful or unsuccessful value?

    def species(self, sp_id, sp_folder_path): #will set the class property values and insert the info for the species table. gets info from csv. 
        print('on species function')
        self.sp_path = sp_folder_path
        self.sp_id = sp_id
        with conn.cursor() as cursor:
            sql = f"INSERT INTO Species (accession_id) VALUES (%s)"
            cursor.execute(sql, (sp_id)) 
            conn.commit()
        return self.chromosomes()


    def chromosomes(self):
        print('on chrom function')
        os.chdir(self.sp_path)
        chroms = subprocess.run(["cut -f 9 genomic.gff | cut -d ';' -f 4 | grep -i -n 'chromosome='| less"], shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip().split('\n') #get output for all chromosomes with line numbers
        c_starts = [] #list of lines where all chromosomes start in the gff
        for i in chroms: #does the loop for the whole genome, each chrom
            if len(i) > 0:
                i = i.split(':')
                c_starts.append(i[0])
                os.chdir(self.sp_path) #gets lost here if this isnt here
                romo = subprocess.run([f"sed -n '{i[0]}'p genomic.gff"], shell = True, stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip().split('\t') #use the line numbers to grab the line of the chromosome you want
                rom = romo[-1].split(';')[2].split('=')[1]
                l, seq = self.get_seq(romo[0])
                with conn.cursor() as cursor:
                    sql = f"INSERT INTO Chromosomes (accession_id, chrom_id, chrom_name, chrom_seq_start, chrom_seq_end, chrom_seq) VALUES (%s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (self.sp_id, romo[0], rom, romo[3], romo[4], seq,)) #calling self.get_seq calls igs and windows and resets gene_ss
                    conn.commit()
            
                self.c_id = romo[0] #reassign with each one-- after windows and igs have been done with the above self.get_seq call
                self.chrom_end = l
                self.genes(l) #dont return or else it wont do the loop, l for windows later


    def get_seq(self, cid): #takes a minute. called when chromosome is resetting- doing function calls here
        print('on seq function')
        fnap = []
        for i in os.listdir(self.sp_path): #change to an if statement? get rid of unecessary loops?
            if i != 'genomic.gff':
                fnap = i
        for seq_record in parse(fnap, "fasta"):
            if cid in seq_record.id:
                return len(seq_record.seq), seq_record.seq #will this convert to string for input in sql?

            
    def genes(self, l): #find +- strands so we can do the complement in sql for our g-c calculations
        print('on genes function')
        results = []
        g = subprocess.run([f'grep "^{self.c_id}.*ID=gene.*" genomic.gff | less'], shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip().split('\n') #get all genes for current chromosome
        self.gene_ss = {} #reset for each chrom
        for i in g: #for each gene in the chromosome
            if len(i) >1: #theres an empty space at the end for some reason
                i = i.split('\t') #split the info
                ene = {}
                ene['accession_id'] = self.sp_id
                ene['chrom_id'] = self.c_id
                ene['gene_id'] = i[-1].split(';')[0][3::] 
                ene['strand'] = i[6]
                ene['start'] = i[3] 
                ene['end'] = i[4]

                results.append(ene)

                
                self.gene_ss[ene['gene_id']] = [int(ene['start']), int(ene['end'])] #testing for introns
                self.flanking(ene['gene_id'], ene['strand'], [int(ene['start']), int(ene['end'])])  #call the flanking function for each gene, uses self.gene_id as it updates each time

        os.chdir('/Users/biollab-120475/mysqlUploads')
        with open('gene_records.tsv', 'a') as tsvfile:
            writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
            for rec in results:
                writer.writerow(rec.values())
        print('uploading gene and flank info')
        self.upload('/Users/biollab-120475/mysqlUploads/gene_records.tsv', 'accession_id, chrom_id, gene_id, gene_strand, gene_seq_start, gene_seq_end', 'Genes') #upload the genes once they have all been recorded for the chromosome
        self.upload('/Users/biollab-120475/mysqlUploads/flank_records.tsv', 'accession_id, chrom_id, gene_id, flank_id, flank_strand, up_start, up_stop, down_start, down_stop', 'Flanking_seq') #upload the flanking sequences once all of the genes have been added to the database


        self.windows(l)
        self.exons()
        return None

    def flanking(self, gid, strand, ss): 
        j = 0 #counter to keep ids unique within genes
        upstart = int(ss[0])-50 # ***51???***   the start of the upstream flanking seq
        upend = int(ss[0]) #end of upstream
        downstart = int(ss[1]) 
        downend = int(ss[1])+50
        if upstart < 1 or downend > self.chrom_end: #we cant let the sequences be negative or go past the end of the chromosome
            None
        else:
            j += 1
            flank_id = f'f_{gid}_{j}' #adding the gene_id makes it unique

            flank_rec = {'accession_id':self.sp_id, 'chrom_id':self.c_id,'gene_id': gid, 'flank_id':flank_id, 'flank_strand':strand,'up_start':upstart, 'up_stop':upend, 'down_start':downstart, 'down_end':downend}
            os.chdir('/Users/biollab-120475/mysqlUploads')
            with open('flank_records.tsv', 'a') as tsvfile:
                    writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
                    writer.writerow(flank_rec.values()) 
        #dont upload because the genes havent been inserted to the database yet
        return None


    def windows(self, l):
        print('on windows function')
        kbs = [500000,100000,50000,10000,3000]
        gene_intervals = [(z[0], z[1]) for z in self.gene_ss.values()]  # Pre-compute gene intervals
        results = []  # Collect results to write at once
        j = 0 #for the ID

        for b in kbs: #for each window size
            print(f'on size {b}')
            windows = []
            for i in range(0, l, b): #increment by window size, not l+1 right?
                window_start = i
                window_end = min(i + b, l)  # cap at l
                g = 0  # gene count

                for gene_start, gene_end in gene_intervals: #i think this works?
                    if gene_end < window_start or gene_start > window_end:  # Completely outside
                        continue
                    g += 1  # Overlapping or contained gene

                j += 1
                size = int(b/1000)
                wind_id = f'w{size}_{self.c_id[:10]}_{j}' #window size, chromosome, #
                    
                window_rec = {'accession_id':self.sp_id, 'chrom_id':self.c_id,'wind_id':wind_id, 'wind_seq_start':window_start, 'wind_seq_end':window_end, 'gene_count':g}
                results.append(window_rec)
        os.chdir('/Users/biollab-120475/mysqlUploads')
        with open('window_records.tsv', 'a') as tsvfile:
            writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
            for rec in results:
                writer.writerow(rec.values())
            
        self.upload('/Users/biollab-120475/mysqlUploads/window_records.tsv', 'accession_id, chrom_id, wind_id, wind_seq_start, wind_seq_end, gene_count', 'Windows')   
    
        return None

    

    def exons(self):
        print('on exon function')
        results = []
        self.exon_ss = [] #reset with each chrom
        grandparents = {} # dictionary for reference of all rnas and gene parents for exons who have rna parents and not gene parents
        os.chdir(self.sp_path) #get to the directory with ur file
        rnas = subprocess.run([f'grep "^{self.c_id}.*ID=rna.*" genomic.gff | less'], shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip().split('\n') #get all rna
        for i in rnas:
            p = i.split('\t')
            p2 = p[-1].split(';')
            rnaid = p2[0][3::]
            grandparent = p2[1]
            grandparents[rnaid] = grandparent

        os.chdir(self.sp_path) #get to the directory with ur file
        exs = subprocess.run([f'grep "^{self.c_id}.*ID=exon.*" genomic.gff | less'], shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip().split('\n') #gives me all exons for chromosome
        for i in exs: #for each exon, enumerating for troubleshooting
            e = i.split('\t') #break it
            e2 = e[-1].split(';') #break the last field
            if 'Parent=rna' in e2[1]:
                exon_rec = {'accession_id':self.sp_id, 'chrom_id':self.c_id, 'gene_id': grandparents[e2[1][7::]],'exon_id':e2[0][3::], 'exon_strand':e[6],'exon_seq_start':e[3], 'exon_seq_end':e[4]}
            elif 'Parent=gene' in e2[1]:
                exon_rec = {'accession_id':self.sp_id, 'chrom_id':self.c_id, 'gene_id': e2[1][7::],'exon_id':e2[0][3::], 'exon_strand':e[6],'exon_seq_start':e[3], 'exon_seq_end':e[4]} #cant use self.gene_id because this is called outside the gene loop
            else:
                print('new parent found, record not added to file:', i)

            results.append(exon_rec)
            self.exon_ss.append([int(e[3]), int(e[4])]) 

        os.chdir('/Users/biollab-120475/mysqlUploads')
        with open('exon_records.tsv', 'a') as tsvfile: #write all at once
            writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
            for rec in results:
                writer.writerow(rec.values())

        self.upload('/Users/biollab-120475/mysqlUploads/exon_records.tsv', 'accession_id, chrom_id, gene_id, exon_id, exon_strand, exon_seq_start, exon_seq_end', 'Exons')

        self.fix_overlap(self.exon_ss) #do the introns now that the exon_ss list is complete, before igs messes it up
        self.fix_overlap(self.gene_ss) #we can mess up the gene list now for igs,
        self.cds()
        return None


    def cds(self): #dont know the relationships for this yet-- need to make a table
        print('on cds function')
        results = []
        grandparents = {} # dictionary for reference of all rnas and gene parents for exons who have rna parents and not gene parents
        os.chdir(self.sp_path) #get to the directory with ur file
        rnas = subprocess.run([f'grep "^{self.c_id}.*ID=rna.*" genomic.gff | less'], shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip().split('\n') #get all rna
        for i in rnas:
            p = i.split('\t')
            p2 = p[-1].split(';')
            rnaid = p2[0][3::]
            grandparent = p2[1]
            grandparents[rnaid] = grandparent

        os.chdir(self.sp_path) #get to the directory with ur file
        cdss = subprocess.run([f'grep "^{self.c_id}.*ID=cds.*" genomic.gff | less'], shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip().split('\n') #gives me all exons for chromosome
        for i in cdss: #for each cds
            c = i.split('\t') #break it
            c2 = c[-1].split(';') #break the last field
            if 'Parent=rna' in c2[1]:
                cds_rec = {'accession_id':self.sp_id, 'chrom_id':self.c_id, 'gene_id': grandparents[c2[1][7::]],'cds_id':c2[0][3::], 'cds_strand':c[6],'cds_seq_start':c[3], 'cds_seq_end':c[4]}
            elif 'Parent=gene' in c2[1]:
                cds_rec = {'accession_id':self.sp_id, 'chrom_id':self.c_id, 'gene_id': c2[1][7::],'cds_id':c2[0][3::], 'cds_strand':c[6],'cds_seq_start':c[3], 'cds_seq_end':c[4]} #cant use self.gene_id because this is called outside the gene loop
            else:
                print('new parent found, record not added to file:', i)
            
            results.append(cds_rec)

            
        os.chdir('/Users/biollab-120475/mysqlUploads')
        with open('cds_records.tsv', 'a') as tsvfile: #write all at once
            writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
            for rec in results:
                writer.writerow(rec.values())
        self.upload('/Users/biollab-120475/mysqlUploads/cds_records.tsv', 'accession_id, chrom_id, gene_id, cds_id, cds_strand, cds_seq_start, cds_seq_end', 'CDS')
        

        return None



    def fix_overlap(self, ss_list): #fix overlap on either genes or exons before igs and intron calcs -- i edited this a lot but it should work
        print('fixing overlaps')
        v = 0
        if type(ss_list) == dict:
            ss_list = list(ss_list.values()) #testing dict, its important that this happens after introns cuz its replacing the property. 
            v = 1
        else:
            None

        ss_list.sort(key=lambda x: x[0]) #sort by the start coordinate!!! 
        for index, i in enumerate(ss_list):
            if index != len(ss_list)-1: #if it isnt the last gene/exon
                if i[1] > ss_list[index+1][0]: #if the second coordinate is bigger than the first of the next one, there is an overlapping gene
                    indices = [] #list to hold all indices involved in overlap
                    y = index+1  #the index of the next gene
                    indices.append(index) #include the gene with the minimnum in the list since we use the minimum and maximum later
                    next_start_coord = ss_list[y][0]  
                    r = [] #running list of ranges
                    r.append(list([i for i in range(ss_list[y-1][0], int(ss_list[y-1][1]+1))]))   
                    r = list(itertools.chain.from_iterable(r)) #makes it one big list 
                    while next_start_coord in r: #until the start coordinate of the next gene is not in any of the ranges of the genes starting at i                *do this recursively later?
                        indices.append(y) #add index of the overlapping gene
                        y = y + 1 #go to the next gene (if i is gene B, we just tested gene c, so test start coord of gene d now)
                        r.extend(list([i for i in range(ss_list[y-1][0], int(ss_list[y-1][1] +1))])) #add the numbers for the range of the gene we just tested (c) to the running list
                        if y <= len(ss_list) -1:
                            next_start_coord = ss_list[y][0]   #look ahead to the next one
                        else: #if looking ahead doesnt lead to finding a non overlapping gene before the list ends
                            break
                    coords = [i for index, i in enumerate(ss_list) if index in indices] #get the values if the indexes
                    coords = list(itertools.chain.from_iterable(coords)) #concatenates the list so we can easily get min and max
                    if max(coords) == i[1]:  #the min will always be i if it is sorted by i[0], so if the first gene encompasses the coordinates of all the ones overlapping
                        to_delete = [ss_list[j] for j in indices[1::]]
                        [ss_list.remove(k) for k in to_delete]  
                    else: #if the max is not the i[1]
                        i[1] = max(coords) #make the max of the list the end of the first gene, basically combining them all. 
                        to_delete = [ss_list[j] for j in indices[1::]]  #dont include the index with the minimum(start point), it should be the first one because it was added first
                        [ss_list.remove(k) for k in to_delete] 
                
                else:
                    continue 
        if v == 1: #should work
            return self.igs()
        else:
            return self.introns()


    def igs(self): #we are now working with the edited list, no strand info for igs yet
        print('on igs function')
        j = 0 
        if len(self.gene_ss) > 1: #if there is more than one gene, so at least one seq
            for index, i in enumerate(self.gene_ss):
                if index < len(self.gene_ss)-1: #if its not the last gene
                    print(i[1], type(i[1]))
                    start = int(i[1])+1 #running into errors converting to int, is this an empty string???
                    next_gene = self.gene_ss[index+1]
                    stop = int(next_gene[0]) - 1 
                    j += 1
                    igs_id = f'igs_{self.c_id}_{j}'
                    
                    igs_rec = {'accession_id':self.sp_id, 'chrom_id':self.c_id,'igs_id':igs_id, 'igs_seq_start':start, 'igs_seq_end':stop} #not including strands rn
                    os.chdir('/Users/biollab-120475/mysqlUploads')
                    with open('igs_records.tsv', 'a') as tsvfile:
                        writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
                        writer.writerow(igs_rec.values()) 
                else: #if it is the last gene, dont make the calculation or the entry
                    None
        else:
            None #dont make an entry
        return self.upload('/Users/biollab-120475/mysqlUploads/igs_records.tsv', 'accession_id, chrom_id, igs_id, igs_seq_start, igs_seq_end', 'Intergenic_seq')

    def introns(self): #we are now working with the edited list
        print('on intron function')
        results = []
        j = 0 
        if len(self.exon_ss) > 1: #if there is more than one exon, so at least one seq
            for index, i in enumerate(self.exon_ss):
                if index < len(self.exon_ss)-1: #if its not the last exon
                    start = int(i[1])+1
                    next_ex = self.exon_ss[index+1]
                    stop = int(next_ex[0]) - 1 
                    j += 1
                    
                    key = self.intron_gids([start,stop]) #find the corresponding geneid and strand
                    int_id = f'int_{key}_{j}'
                    intron_rec = {'accession_id':self.sp_id, 'chrom_id':self.c_id,'gene_id':None ,'inton_id':int_id, 'intron_strand':None,'int_seq_start':start, 'int_seq_end':stop}
                    results.append(intron_rec)
                     
                else: #if it is the last exon, dont make the calculation or the entry
                    None
        else:
            None #dont make an entry

        os.chdir('/Users/biollab-120475/mysqlUploads')
        with open('intron_records.tsv', 'a') as tsvfile: #write all at once
            writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
            for rec in results:
                writer.writerow(rec.values())

        return self.upload('/Users/biollab-120475/mysqlUploads/intron_records.tsv', 'accession_id, chrom_id, gene_id, intron_id, intron_strand, intron_seq_start, intron_seq_end', 'Introns')

    def intron_gids(self, coords):
        for key, value in self.gene_ss.items():
            if coords[0] in range(value[0], value[1]+1) and coords[1] in range(value[0], value[1]+1): #an intron should have both coords within a gene, and this is before the gene overlaps are fixed 
                #print(coords, key, value)
                return key
            else:
                continue #i may be skipping a lot idk yet. 






today = numos()
today.files()
today.species('GCA_020142125.1', '/Users/biollab-120475/Desktop/ncbi_dataset/data/GCA_020142125.1/ncbi_dataset/data/GCA_020142125.1')
#call this in a loop for each file folder?
#for i in os.listdir('/Users/biollab-120475/Desktop/ncbi_dataset/data'):
    #today.species(i, f'/Users/biollab-120475/Desktop/ncbi_dataset/data/{i}/ncbi_dataset/data') #should be the format for everything?


# CDS and exons not uploading. igs function saying theres an int base 10 error with the gene_ss coord, check that its not an empty string. 

#check out ensemble and add to database
"""
def windows(self, l):
        print('on windows function')
        kbs = [500000,100000,50000,10000,3000]
        j = 0 #for the ID
        for b in kbs: #for each window size
            print('on new size')
            windows = []
            for i in range(0, l, b): #increment by window size
                y = i +b
                if y <= l: #if it is not longer than the chromosome
                    windows.append([i, i+b])
                elif y > l: #if it is longer
                    windows.append([i, i + (l - i)]) #make a partial window

            for k in windows:
                g = 0 #gene count   
                for z in self.gene_ss.values():
                    if z[0] < k[0] and z[1] > k[1]: #if the gene is larger than the window and the start/end coords are outside of it
                        g += 1
                    if z[0] in range(k[0], k[1]+1) or z[1] in range(k[0], k[1]+1): #if the start or end cord is in the range of the window
                        g += 1
                    else:
                        None
                j += 1
                size = int(b/1000)
                wind_id = f'w{size}_{self.c_id[:10]}_{j}' #window size, chromosome, #
                    
                window_rec = {'accession_id':self.sp_id, 'chrom_id':self.c_id,'wind_id':wind_id, 'wind_seq_start':k[0], 'wind_seq_end':k[1], 'gene_count':g}
                os.chdir('/Users/biollab-120475/mysqlUploads')
                with open('window_records.tsv', 'a') as tsvfile:
                    writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
                    writer.writerow(window_rec.values()) 
            
        self.upload('/Users/biollab-120475/mysqlUploads/window_records.tsv', 'accession_id, chrom_id, wind_id, wind_seq_start, wind_seq_end, gene_count', 'Windows')   
    
        return None
"""
"""
import csv

def windows(self, l):
    print('on windows function')
    kbs = [500000, 100000, 50000, 10000, 3000]
    j = 0  # for the ID
    gene_intervals = [(z[0], z[1]) for z in self.gene_ss.values()]  # Pre-compute gene intervals
    results = []  # Collect results to write at once

    for b in kbs:  # for each window size
        print('on new size')
        for i in range(0, l, b):  # increment by window size
            window_start = i
            window_end = min(i + b, l)  # cap at l
            g = 0  # gene count

            for gene_start, gene_end in gene_intervals:
                if gene_end < window_start or gene_start > window_end:  # Completely outside
                    continue
                g += 1  # Overlapping or contained gene

            j += 1
            size = int(b / 1000)
            wind_id = f'w{size}_{self.c_id[:10]}_{j}'  # window size, chromosome, #

            window_rec = {
                'accession_id': self.sp_id,
                'chrom_id': self.c_id,
                'wind_id': wind_id,
                'wind_seq_start': window_start,
                'wind_seq_end': window_end,
                'gene_count': g
            }
            results.append(window_rec)  # Store result

    # Write all results to the file at once
    file_path = '/Users/biollab-120475/mysqlUploads/window_records.tsv'
    with open(file_path, 'a', newline='') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
        writer.writerow(window_rec.keys())  # Write header if needed
        for rec in results:
            writer.writerow(rec.values())

    self.upload(file_path, 'accession_id, chrom_id, wind_id, wind_seq_start, wind_seq_end, gene_count', 'Windows')

    return None
"""
