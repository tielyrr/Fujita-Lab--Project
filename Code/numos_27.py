import json
import os
import jsonlines
import datetime
from datetime import date
import shutil
import sys
import csv
import pymysql
import numpy as np
import pandas as pd
import subprocess
import pathlib
import re
import gzip
import itertools
import ast

# I'm going to use PyInstaller to turn this script into an executable that can be run on anyones computer 
# without them having to download packages and stuff.
# from there, I can set up the .exe to run in the windows or linux scheduler for whatever time interval


###########################################################################################################################################################################################################
#                                                                                                                                                                                                         #
#                  CHANGE THESE CLASS PROPERTIES BEFORE RUNNING THE PROGRAM:                                                                                                                              #
#   -local_genomes_folder_pathway  #the folder that contains your rehydrated genomes(fna files) and records_updates and jsonl and csv file                                                                 #
#   -local_genomes_jsonl_pathway   #JSON FOR SPECIFIC TAXON OR INFO YOU NEED IF THERE ARE MULTIPLE GENOME COLLECTIONS ON THE COMPUTER.                                                                     #
#   -taxon   #add to this list if you want more or different taxa checked and downloaded                                                                                                                   #
#   -ncbi_tags                                                                                                                                                                                             #
#   THIS IS WHAT YOUR NCBI_TAGS SHOULD LOOK LIKE OR THINGS WONT WORK:                                                                                                                                     #
#   ncbi_tags = f'./datasets summary genome taxon {self.taxon} --annotated --assembly-level chromosome --assembly-level complete --assembly-source refseq --as-json-lines > {self.taxon}_updates.jsonl' 
#   -conn properties for MySQL connection
#                                                                                                                                                                                                         #
###########################################################################################################################################################################################################



conn = pymysql.connect(  #connection to sql
        host='localhost',
        user='root',
        password='Abc12345',
        db='ncbi',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)




class NCBI_genome_auto_update():
    def __init__(self):
        self.local_genomes_folder_pathway = r'/Users/biollab-120475/Desktop/ncbi_dataset/data'
        self.local_genomes_jsonl_pathway = r'/Users/biollab-120475/Desktop/ncbi_dataset/squamata.jsonl'  
        self.local_folder = r'/Users/biollab-120475/Desktop/ncbi_dataset' 
        self.taxon = 'squamata'
        self.ncbi_tags = f'datasets summary genome taxon {self.taxon} --annotated --reference --assembly-level chromosome --assembly-level complete --as-json-lines > {self.taxon}_updates.jsonl'
        self.updates_file_path = []
        self.data = []
        self.successfully_downloaded_data = []
        
    def records_writing(self, r_data):  #writes what the update is doing in real time to a records text file in the specified directory
        os.chdir(self.local_folder)
        with open('genome_auto_updates_records.txt', 'a') as file: #appends to existing file
                file.write(r_data)
   
    def check_records(self): #makes a records file if there isnt one already
        os.chdir(self.local_folder)
        check_for_file = os.path.isfile(f'{self.local_folder}/genome_auto_updates_records.txt')
        if check_for_file == False:
            with open('genome_auto_updates_records.txt', 'w') as file:
                file.write('')
        else:
            None
    def do_mac_setup(self):
        #check for datasets cli
        test = os.system('datasets --help')
        if test != 0: #if this results in an error, you will need to download 'datasets' and add to your computers PATH
            r_data = f"\n\n\n{datetime.datetime.now()} ***ERROR*** PROGRAM TERMINATED. NCBI CLI 'datasets' not in $SHELL path.\n"
            self.records_writing(r_data)
            sys.exit() 
        else:
            r_data = f"\n\n\n{datetime.datetime.now()}" #make a timestamp for the record so you can see the days and times things ran
            self.records_writing(r_data)
            return None
          
        
    def check_for_new_data(self): 
        r_data = f'\n\nChecking the NCBI Database for new updates using these tags:\n{self.ncbi_tags}'
        self.records_writing(r_data)
        
        os.chdir(self.local_folder) #make sure download is where we want it
        exit_val = os.system(self.ncbi_tags) #downloading the summary from ncbi, saving exit result so we can know if it was successful or not
        #^ this will do the check without having to download the dehydrated zip file for checking for updates
        #^^gets the metadata to a jsonl that could be compared line by line to another   
        if exit_val != 0: #a value of 1 means there was an error
            r_data = f'\n***ERROR*** PROGRAM TERMINATED. FAILED TO RETRIEVE UPDATES FILE FROM NCBI DUE TO CLI ISSUE, EXIT VALUE: {exit_val}'
            self.records_writing(r_data)
            sys.exit()
        else:
            r_data = '\n--Successfully retrieved updated information from  NCBI--'
            self.records_writing(r_data)
            
        updates_file_path = rf'{self.local_folder}/{self.taxon}_updates.jsonl' #establish this so it can be added to the class property later, after it is converted
         
        # I have to rewrite the files because if I don't, even if they are the 'same' using jsondiff, it wont work.
        with jsonlines.open(updates_file_path, mode='r') as reader, jsonlines.open(rf'{self.local_folder}/{self.taxon}_updates2.jsonl', mode='w', compact = True) as writer:
            for line in reader:
                writer.write(line) # ** have to rewrite it or else it wont compare properly in the duplicates function **
        
        with jsonlines.open(self.local_genomes_jsonl_pathway, mode='r') as reader, jsonlines.open(rf'{self.local_folder}/{self.taxon}_fixer.jsonl', mode='w', compact = True) as writer:
            for line in reader:
                writer.write(line) #rewriting this too in case it is an ncbi copy and not one that ive rewritten
        
        os.remove(updates_file_path) #remove the one that wont compare properly
        os.remove(self.local_genomes_jsonl_pathway)
        os.rename(f'{self.taxon}_fixer.jsonl', f'{self.taxon}.jsonl')
        os.rename(f'{self.taxon}_updates2.jsonl', f'{self.taxon}_updates.jsonl') #rename the rewritten one to the original name
        self.updates_file_path.append(updates_file_path) #make the path official for later reference
        
        
        #os.system(f'./datasets download genome taxon squamata --annotated --assembly-level complete --assembly-level chromosome --assembly-source refseq --dehydrated')
        #^ this downloads the dehydrated data. the json file given is matching the lookup- they both currently have 16. 
        #changing the flags up will change the output
        #now i know the check without the download is accurate because the two match.
       
        #this relies on ncbi's accessions updating the number after the decimal for updates. under 'locus name' https://www.ncbi.nlm.nih.gov/genbank/samplerecord/ 
        with open(self.updates_file_path[0], 'r') as k, open(self.local_genomes_jsonl_pathway, 'r') as f:  
            a = f.read()
            for line in k: #for every line in the update file
                lk = json.loads(line) #load the line to a variable
                tf = lk['accession'] in a #if the line exists in the file anywhere
                if tf ==True:
                    continue  #it is already downloaded or a duplicate whos accession wasnt updated per the link above
                else:
                    self.data.append(lk) #it is a new bit of data
                        
        if len(self.data) != 0: #if there is new data to be handled
            r_data = f"\nNew Data Acquired: {[i['accession'] for i in self.data]}"
            self.records_writing(r_data)
            return self.find_duplicates()          #call next function
                
        else: #if there is not new data
            r_data = '\n--No new data or updates to be found. CHECK COMPLETE--\n' 
            self.records_writing(r_data)
            os.remove(self.updates_file_path[0])
            sys.exit()
 #add something to write a csv here, too?               
                           
 ###############################################################
 #   Everything past here is only if new data has been found   #
 ###############################################################     
  
  # if duplicates are found, we will delete all old files, replace them with updated ones in directory, then go to sql and delete cascade everything with that accession - make new data
  # only issue is sometimes updates change the accession to a .3 or .2, in that case 2 different accessions would reference the same genome, just one more updated
  # so i cant check if the accessions are equal anymore... just the data before the decimal and then after the decimal, then do a replacement for those. also a regular 
  # equality check, though, just in case they did not change the accession with the update. 
    def find_duplicates(self): 
        extant_updates = [] #list for any data that has been updated (a different number after decimal)
        #see if any of the new data has matching accession numbers to existing local data
        with jsonlines.open(self.local_genomes_jsonl_pathway) as reader:
            for obj in reader: #for every line in the local json
                for i in self.data:
                    tf2 = i['accession'][:-2] == obj['accession'][:-2] #if the accessions before the decimal are the same but not after the decimal
                    if tf2 == True:
                        extant_updates.append(i['accession'])
                    else:
                        None 
                                   
        #archive local json before we do anything else
        archive_path = rf'{self.local_folder}/update_archive' #where the file should be if it exists or where it will be once created
        check_for_file = os.path.isdir(archive_path) #see if it exists
        if check_for_file == False:
            os.makedirs(rf'{self.local_folder}/update_archive') #make archive folder
        else:
            None
            
        shutil.copy2(self.local_genomes_jsonl_pathway, archive_path) #copy it over
        os.chdir(archive_path)
        os.rename(f'{self.taxon}.jsonl', f"{date.today().strftime('%Y-%m-%d')}.jsonl") #So you know what day it was from
        r_data = '\nCopy of local JSONL archived.'    
        self.records_writing(r_data)

        if len(extant_updates) == 0: #if there are no duplicates
            r_data = '\nNo extant updates.'    
            self.records_writing(r_data)
            return self.download_new_data(extant_updates) #including the empty list as an if else to change how new json is written there
        else:
             r_data = '\nThere are extant updates...'    
             self.records_writing(r_data)
             return self.fix_dupes(extant_updates)


    
    def fix_dupes(self, update_lst): #currently only deletes duplicates from local files and not the database, also, the lab mac won't let me delete directories
        r_data = f'\nUpdates found for: {update_lst} --- Deleting these files(fna,lnk, gff) from {self.local_genomes_folder_pathway} and the MySQL Database.' 
        self.records_writing(r_data)
        # below is not tested, but what I would like to happen
        
        with conn.cursor() as cursor: #perform the delete cascade simultaneously
            for i in update_lst:
                with conn.cursor() as cursor:
                    sql = f"DELETE FROM species WHERE accession_id == '{i}'"
                    cursor.execute(sql, (i,))
                    conn.commit()
                    

             
        #deleting old files because if there is a duplicate we want the newest info. this takes a while because it is searching...
        for i in update_lst: 
            for (root, dirs, files) in os.walk(self.local_genomes_folder_pathway):
                for file in files:
                    if i in file: 
                        path = root + '/' + file
                        os.remove(path) #SCARY!
                for name in dirs: #the gff files are in the directory and not individually named
                        if i in name:
                            stuff = os.listdir(rf'{self.local_genomes_folder_pathway}/{name}')
                            for j in stuff:
                                if '.gff' in j:
                                    os.remove(f'{self.local_genomes_folder_pathway}/{name}/{j}')
        # This unfortunately leaves empty directories because the lab MAC won't let me delete directories from the script. 
        # If on a different computer, add code to delete matching directories
            
        return self.download_new_data(update_lst)
        
    def download_new_data(self, update_lst): #THIS TAKES TIME SINCE EACH ONE IS A HALF A GIG. Downloads one at a time since this is meant to be an updating script to an existing database. for uploads of bulk data, i may make a different script/function. 
        successfully_downloaded_data = []
        for i in self.data:
            os.chdir(self.local_genomes_folder_pathway)  #download all new data to the right directory
            exit_value = os.system(f"datasets download genome accession {i['accession']} --include genome,gff3 --filename {i['accession']}.zip") #this runs the command and stores the exit value
            if exit_value != 0: #if the download was unsuccessful or incomplete in any way
                r_data = f"\n****************EXIT VALUE ERROR: {exit_value} for {i['accession']} --DOWNLOAD UNSUCCESSFUL--\nACTION REQUIRED: FILE METADATA NOT WRITTEN ONTO LOCAL JSONL OR CSV-- CHECK WORKING DIRECTORY FOR INCOMPLETE DATA\n***************\n"
                self.records_writing(r_data)
            else:
                r_data = f"\nDownload successful for {i['accession']}"
                successfully_downloaded_data.append(i['accession']) #to make file for next class to read
                self.records_writing(r_data)
                
                os.chdir(self.local_genomes_folder_pathway)
                os.system(f"unzip {i['accession']}.zip -d {i['accession']}") #sometimes unzip doesnt work and you may need to use 'Expand-Archive -Path "C:\Path\To\Your\Archive.zip" -DestinationPath "C:\Path\To\Destination\Folder"'

                os.remove(f"{i['accession']}.zip") #we dont need it anymore
                
                if len(update_lst) == 0: #if there were no duplicates, you can just append to the end of the json.
                    with jsonlines.open(self.local_genomes_jsonl_pathway, mode='a', compact = True) as writer:    
                        writer.write(i)  #updates the local json
                
                else: #if there were updates
                    #remove deleted duplicate file's metadata from local json. doesnt work in dupe function, only here
                    with jsonlines.open(self.local_genomes_jsonl_pathway, mode='r') as reader, jsonlines.open(rf'{self.local_folder}/{self.taxon}2.jsonl', mode='w', compact = True) as writer: #you cant delete from a json, gotta rewrite
                        for line in reader:
                            for j in update_lst:
                                tf = line['accession'] in update_lst
                                if tf == True: #if the accession is the same, skip over it because it was just deleted
                                    None
                                else:
                                    writer.write(line)
                        writer.write(i) 
                    os.chdir(self.local_folder)
                    os.rename(f'{self.taxon}2.jsonl', f'{self.taxon}.jsonl') #make it normal to be used properly later
                        
        r_data = f'\nRewrote metadata to reflect updated local database.'
        self.records_writing(r_data)

        with open('data_to_upload.txt', 'w') as writer:
            writer.write(f'{successfully_downloaded_data}')
            writer.close()

        return self.make_csv()
    
    def make_csv(self): #this works on mac but not linux for some reason- it wont save all the lines, just the last row that was written
        check_for_file = os.path.isfile(f'{self.local_folder}/{self.taxon}_metadata.csv')
        if check_for_file == True:
            os.remove(f'{self.local_folder}/{self.taxon}_metadata.csv')
            #get rid of not updated information and rewrite the csv
        else:
            None # continue with next block of code
        os.chdir(self.local_folder)
        
        fields = ['accession', 'assembly_level', 'refseq_category', 'organism', 'assembly_status','bioproject_accession',  'path_to_fna', 'path_to_gff'] #what we want easily seen and accessed
        with open(f'{self.taxon}_metadata.csv', 'w', newline = '') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields)
            with jsonlines.open(self.local_genomes_jsonl_pathway, mode='r') as reader: #open the file and write info as you come across it
                for i in reader:
                    fna_path = ''
                    gff_path = ''
                    for (root, dirs, files) in os.walk(self.local_genomes_folder_pathway): #this takes a long time even for just a few files...
                        for file in files:
                            if i['accession'] in file and '.fna' in file:
                                fna_path = os.path.abspath(os.path.join(root,file))
                        for name in dirs: #the gff files are in the directory and not individually named ('genomic.gff' with no accession included in name), this will add these along with any files in unzipped folders with the matching name
                            if i['accession'] in name:
                                dn = os.path.abspath(os.path.join(root,name))
                                stuff = os.listdir(dn)
                                for j in stuff:
                                    if '.gff' in j:
                                        gff_path = os.path.abspath(os.path.join(root,name,j))
                    #so far two different naming conventions -- was also causing issues with comparisons to check for new data
                    if 'assembly_info' in i.keys():
                        spb = [i['accession'], i['assembly_info']['assembly_level'], i['assembly_info']['refseq_category'], i['organism']['organism_name'], i['assembly_info']['assembly_status'],i['assembly_info']['bioproject_accession'], fna_path, gff_path]
                        csvwriter.writerow(spb)
                    elif 'assemblyInfo' in i.keys():
                        spb = [i['accession'], i['assemblyInfo']['assemblyLevel'], i['assemblyInfo']['refseqCategory'], i['organism']['organismName'], i['assemblyInfo']['assemblyStatus'],i['assemblyInfo']['bioprojectAccession'], fna_path, gff_path]
                        csvwriter.writerow(spb)
                        
                        
    
                r_data = '\nCSV rewritten\n--UPDATE COMPLETE--'
                self.records_writing(r_data)
                os.remove(self.updates_file_path[0])
            
                return None
        

    

#comment these out if you want to only do an upload without a check- dont forget to change the properties          

           
todays_check = NCBI_genome_auto_update()
todays_check.check_records()
todays_check.do_mac_setup()
todays_check.check_for_new_data() 


##############################################################################################################################################################################################
# while the parent class is inactive, a list called 'self.ndata' will take its place for testing purposes or when you dont need to use the update class                                       #   
#                                                                                                                                                                                            #
# CHANGE THESE IN THE CLASS BEFORE RUNNING  TO YOUR OWN PATH AND DATA                                                                                                                        #
# self.data = ['GCA_009733165.1'] #change to be the parent class property successfully_downloaded_data when you need                                                                         #
# self.csv_path = r"C:\Users\tyler\Downloads\squamata_metadata.csv"                                                                                                                          #
#                                                                                                                                                                                            #
##############################################################################################################################################################################################



class adams_gff_gen(): #same functions Adam wrote, just in oop format
    def __init__(self):
        self.self = self    
        self.GTF_HEADER  = ['seqname', 'source', 'feature', 'start', 'end', 'score','strand', 'frame']
        self.R_SEMICOLON = re.compile(r'\s*;\s*')
        self.R_COMMA     = re.compile(r'\s*,\s*')
        self.R_KEYVALUE  = re.compile(r'(\s+|\s*=\s*)')

    def lines(self, filename):
        """Open an optionally gzipped GTF file and generate a dict for each line.
        """
        #fn_open = gzip.open if filename.endswith('.gz') else open
        with open(filename) as fh:
            for line in fh:
                if line.startswith('#'):
                    continue
                else:
                    yield self.parse(line)
                
    def _get_value(self,value):
        if not value:
            return None

        # Strip double and single quotes.
        value = value.strip('"\'')

        # Return a list if the value has a comma.
        if ',' in value:
            value = re.split(self.R_COMMA, value)
        # These values are equivalent to None.
        elif value in ['', '.', 'NA']:
            return None

        return value

    def parse(self,line):
        """Parse a single GTF line and return a dict.
        """
        result = {}

        fields = line.rstrip().split('\t')

        for i, col in enumerate(self.GTF_HEADER):
            result[col] = self._get_value(fields[i])

        # INFO field consists of "key1=value;key2=value;...".
        infos = [x for x in re.split(self.R_SEMICOLON, fields[8]) if x.strip()]

        for i, info in enumerate(infos, 1):
            # It should be key="value".
            try:
                key, _, value = re.split(self.R_KEYVALUE, info, 1)
            # But sometimes it is just "value".
            except ValueError:
                key = 'INFO{}'.format(i)
                value = info
            # Ignore the field if there is no value.
            if value:
                result[key] = self._get_value(value)

        return result
    





class parse_upload(): #will write our new data to sql!
    def __init__(self):
        self.ndata = []
        self.csv_path = r"/Users/biollab-120475/Desktop/ncbi_dataset/squamata_metadata.csv" #where the csv with the file paths is
        self.accession = '' #has to be above function calls. order of operations. caused me a bit of trouble when it wasn't
        self.fnap = '' #fna path
        self.chrom_id = '' #id of current chrom- constantly updating
        self.gene_id = ''  #id of current gene- constantly updating
        self.gene_start = 0 #start of current gene- constantly updating
        self.gene_end = 0 #end of current gene- constantly updating
        self.gene_ss = [] #start-stop list, used to calculate igs and window gene count
        self.exon_ss = [] #start-stop list to calculate introns
        self.chrom_end = '' #for flanking seq calculations
        
    def csv_data(self): #establishes paths for use. inserts species info into sql so everything else will work
        y = open('/Users/biollab-120475/Desktop/ncbi_dataset/data_to_upload.txt', 'r')
        self.ndata = [i for i in ast.literal_eval(y.read())] #reads the list back in
        df = pd.read_csv(self.csv_path)
        for i in self.ndata: #this is the loop that the whole update will ride on for each accession-- change to 'self.ndata' if not using solo. if empty, nothing will happen.
            index_of_accession = np.where(df["accession"] == i)
            gp = f'{df.loc[index_of_accession]["path_to_gff"].item()}' #establish the paths as class properties for the run we are on, will update with each iteration
            fnap = f"{df.loc[index_of_accession]['path_to_fna'].item()}" 
            self.fnap = fr'{fnap}'
            self.accession = i #this is the accession we are on. 

            #
            with conn.cursor() as cursor: #establishes connection
                sql = f"INSERT INTO Species (accession_id) VALUES (%s)"
                cursor.execute(sql, (self.accession,))
                conn.commit() #cant add anything else unless this is already saved

            gg = adams_gff_gen()
            gff_gen = gg.lines(gp) #i dont know why this wont let me run without self
            self.parse_write(gff_gen) #will call everything for the update -- crucial line
            
        os.remove('/Users/biollab-120475/Desktop/ncbi_dataset/data_to_upload') #delete once used
        
    def flanking(self, ss): 
       j = 0 #counter to keep ids unique within genes
       upstart = int(ss[0])-50 # ***51???***   the start of the upstream flanking seq
       upend = int(ss[0]) #end of upstream
       downstart = int(ss[1]) 
       downend = int(ss[1])+50
       if upstart < 1 or downend > int(self.chrom_end): #we cant let the sequences be negative or go past the end of the chromosome
           None
       else:
           j += 1
           flank_id = f'f_{self.gene_id}_{j}' #adding the gene_id makes it unique
           with conn.cursor() as cursor:                   
               sql = f"INSERT INTO flanking_seq (accession_id, chrom_id, gene_id, flank_id, up_start, up_end, down_start, down_stop) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
               cursor.execute(sql, (self.accession, self.chrom_id, self.gene_id, flank_id, upstart, upend, downstart, downend,))
               conn.commit()
       
       return None
   
    def intergenic_seq(self): #calculates intergenic sequences by combining any overlapping genes, then finding the spaces between them
        self.gene_ss.sort(key=lambda x: x[0]) #sort by the start coordinate!!!
        for index, i in enumerate(self.gene_ss):
            if index != len(self.gene_ss)-1: #if it isnt the last gene
                if i[1] > self.gene_ss[index+1][0]: #if the second coordinate is bigger than the first of the next one, there is an overlapping gene
                    indices = [] #list to hold all indices involved in overlap
                    y = index+1  #the index of the next gene
                    indices.append(index) #include the gene with the minimnum in the list since we use the minimum and maximum later
                    next_start_coord = self.gene_ss[y][0]  
                    r = [] #running list of ranges
                    r.append(list([i for i in range(self.gene_ss[y-1][0], int(self.gene_ss[y-1][1]+1))]))   
                    r = list(itertools.chain.from_iterable(r)) #makes it one big list 
                    while next_start_coord in r: #until the start coordinate of the next gene is not in any of the ranges of the genes starting at i                *do this recursively later?
                        indices.append(y) #add index of the overlapping gene
                        y = y + 1 #go to the next gene (if i is gene B, we just tested gene c, so test start coord of gene d now)
                        r.extend(list([i for i in range(self.gene_ss[y-1][0], int(self.gene_ss[y-1][1] +1))])) #add the numbers for the range of the gene we just tested (c) to the running list
                        if y <= len(self.gene_ss) -1:
                            next_start_coord = self.gene_ss[y][0]   #look ahead to the next one
                        else: #if looking ahead doesnt lead to finding a non overlapping gene before the list ends
                            break
                    coords = [i for index, i in enumerate(self.gene_ss) if index in indices] #get the values if the indexes
                    coords = list(itertools.chain.from_iterable(coords)) #concatenates the list so we can easily get min and max
                    if max(coords) == i[1]:  #the min will always be i if it is sorted by i[0], so if the first gene encompasses the coordinates of all the ones overlapping
                        to_delete = [self.gene_ss[j] for j in indices[1::]]
                        [self.gene_ss.remove(k) for k in to_delete]
                        
                    else: #if the max is not the i[1]
                        i[1] = max(coords) #make the max of the list the end of the first gene, basically combining them all. 
                        to_delete = [self.gene_ss[j] for j in indices[1::]]  #dont include the index with the minimum(start point), it should be the first one because it was added first
                        [self.gene_ss.remove(k) for k in to_delete] 
                        
                else:
                    continue 

        #complete above before making the igs, we are now working with the edited list
                
        j = 0 
        if len(self.gene_ss) > 1: #if there is more than one gene, so at least one seq
            for index, i in enumerate(self.gene_ss):
                if index < len(self.gene_ss)-1: #if its not the last gene
                    start = int(i[1])+1
                    next_gene = self.gene_ss[index+1]
                    stop = int(next_gene[0]) - 1 
                    j += 1
                    igs_id = f'igs_{self.chrom_id}_{j}'
                    with conn.cursor() as cursor:
                        sql = f"INSERT INTO Intergenic_seq (accession_id, chrom_id, igs_id, igs_seq_start, igs_seq_end) VALUES (%s, %s, %s, %s, %s)"
                        cursor.execute(sql, (self.accession, self.chrom_id, igs_id, start, stop,))
                        conn.commit()
                else: #if it is the last gene, dont make the calculation or the entry
                    None
        else:
            None #dont make an entry
            
  
    def introns(self): #overlapping exons have to be dealt with
        self.exon_ss.sort(key=lambda x: x[0]) #sort by the start coordinate!!!
        for index, i in enumerate(self.exon_ss):
            if index != len(self.exon_ss)-1: #if it isnt the last ex
                if i[1] > self.exon_ss[index+1][0]: #if the second coordinate is bigger than the first of the next one, there is an overlapping ex
                    indices = [] #list to hold all indices involved in overlap
                    y = index+1  #the index of the next ex
                    indices.append(index) #include the ex with the minimnum in the list since we use the minimum and maximum later
                    next_start_coord = self.exon_ss[y][0]  
                    r = [] #running list of ranges
                    r.append(list([i for i in range(self.exon_ss[y-1][0], int(self.exon_ss[y-1][1]+1))])) #include the current index
                    r = list(itertools.chain.from_iterable(r)) #makes it one big list 
                    while next_start_coord in r: #until the start coordinate of the next ex is not in any of the ranges of the exs starting at i                *do this recursively later?
                        indices.append(y) #add index of the overlapping ex
                        y = y + 1 #go to the next ex (if i is ex B, we just tested ex c, so test start coord of ex d now)
                        r.extend(list([i for i in range(self.exon_ss[y-1][0], int(self.exon_ss[y-1][1] +1))])) #add the numbers for the range of the ex we just tested (c) to the running list
                        if y <= len(self.exon_ss) -1:
                            next_start_coord = self.exon_ss[y][0]   #look ahead to the next one
                        else: #if looking ahead doesnt lead to finding a non overlapping exon before the list ends
                            break
                    coords = [i for index, i in enumerate(self.exon_ss) if index in indices] #get the values if the indexes
                    coords = list(itertools.chain.from_iterable(coords)) #concatenates the list so we can easily get min and max
                    if max(coords) == i[1]:  #the min will always be i if it is sorted by i[0], so if the ex encompasses the coordinates of all the ones overlapping
                        to_delete = [self.exon_ss[j] for j in indices[1::]]
                        [self.exon_ss.remove(k) for k in to_delete]
                        
                    else: #if the max is not the i[1]
                        i[1] = max(coords) #make the max of the list the end of the first ex, basically combining them all. 
                        to_delete = [self.exon_ss[j] for j in indices[1::]]  #dont include the index with the minimum(start point), it should be the first one because it was added first
                        [self.exon_ss.remove(k) for k in to_delete] 
                        
                else:
                    continue 
            else:
                None

        #complete above before making the igs, we are now working with the edited list
                
        j = 0 
        if len(self.exon_ss) > 1: #if there is more than one gene, so at least one seq
            for index, i in enumerate(self.exon_ss):
                if index < len(self.exon_ss)-1: #if its not the last gene
                    start = int(i[1])+1
                    next_ex = self.exon_ss[index+1]
                    stop = int(next_ex[0]) - 1 
                    j += 1
                    int_id = f'int_{self.gene_id}_{j}'
                    with conn.cursor() as cursor:
                        sql = f"INSERT INTO Introns (accession_id, chrom_id, gene_id, intron_id, intron_seq_start, intron_seq_end) VALUES (%s, %s, %s, %s, %s, %s)"
                        cursor.execute(sql, (self.accession, self.chrom_id, self.gene_id, int_id, start, stop,))
                        conn.commit()
                else: #if it is the last gene, dont make the calculation or the entry
                    None
        else:
            None #dont make an entry
                
            
    def fna_gen(self): #generator for each line in the fna 
        with open(fr"{self.fnap}", 'r') as fh: 
            for line in fh:
                yield line

    def get_seq(self): #make this faster? takes 7-10sec.  
        c_id = self.chrom_id[:10] 
        sequences = []
        fna_g = self.fna_gen() 
        for line in fna_g:
            if line.startswith(">"): #these are the 'titles' before the seq that tell you what is next
                if self.chrom_id.partition(':')[0] in line:  #covers all i think, some IDs will be identical til you hit 17, and the fnas only use the ID before the colon so far, not the whole thing - not tested. was using chrom[:10] or chrom[:17] etc
                    x = next(fna_g) #go to the first line of the seq- this should never reach the end, but the next one might if its the last chrom
                    while not x.startswith(">"):
                        l = x.rstrip()
                        sequences.append(l.upper())
                        try:                             
                            x = next(fna_g)
                        except StopIteration:
                            x = ">"
        seq = "".join(sequences)
        return seq #very large

    def w_kb500(self): #all of these make windows for respective kilobase sizes, but including them all results in 20min upload time for one chromosome. So for now we are only calling w_kb100. this will need to be optimized later, possibly with a bulk insert. 
        l = len(self.get_seq())
        j = 0 #for the ID
        kb500 = 500000
        windows = []
        for i in range(0, l, kb500): #increment by window size
            y = i +kb500
            if y <= l: #if it is not longer than the chromosome
                windows.append([i, i+kb500])
            elif y > l: #if it is longer
                windows.append([i, i + (l - i)]) #make a partial window
        
        for k in windows:
            g = 0 #gene count   
            for z in self.gene_ss:
                if z[0] < k[0] and z[1] > k[1]: #if the gene is larger than the window and the start/end coords are outside of it
                    g += 1
                if z[0] in range(k[0], k[1]+1) or z[1] in range(k[0], k[1]+1): #if the start or end cord is in the range of the window
                    g += 1
                else:
                    None
            j += 1
            wind_id = f'w500_{self.chrom_id[:10]}_{j}' #window size, chromosome, #
            
            with conn.cursor() as cursor:
                sql = f"INSERT INTO Windows (accession_id, chrom_id, wind_id, wind_seq_start, wind_seq_end, gene_count) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (self.accession, self.chrom_id, wind_id, k[0], k[1], g,))
                conn.commit()
                
        return self.w_kb100(l) #make all calculations, then call next window maker
                
    def w_kb100(self): #add 'l' when you do the kb500 again
        l = len(self.get_seq())
        j = 0
        kb100 = 100000
        windows = []
        for i in range(0, l, kb100):
            y = i +kb100
            if y <= l:
                windows.append([i, i+kb100])
            elif y > l:
                windows.append([i, i + (l - i)])
        for k in windows:
            g = 0 #gene count   
            for z in self.gene_ss:
                if z[0] < k[0] and z[1] > k[1]: #if the gene is larger than the window and the start/end coords are outside of it
                    g += 1
                if z[0] in range(k[0], k[1]+1) or z[1] in range(k[0], k[1]+1): #if the start or end cord is in the range of the window
                    g += 1
                else:
                    None
            
            j += 1
            wind_id = f'w100_{self.chrom_id[:17]}_{j}' #window size, chromosome, #17 for the one genome that has a long id
            
            with conn.cursor() as cursor:
                sql = f"INSERT INTO Windows (accession_id, chrom_id, wind_id, wind_seq_start, wind_seq_end, gene_count) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (self.accession, self.chrom_id, wind_id, k[0], k[1], g,))
                conn.commit()
                
        return None #self.w_kb50(l)
                
    def w_kb50(self, l):
        j = 0
        kb50 = 50000
        windows = []
        for i in range(0, l, kb50):
            y = i +kb50
            if y <= l:
                windows.append([i, i+kb50])
            elif y > l:
                windows.append([i, i + (l - i)])
        for k in windows:
            g = 0 #gene count   
            for z in self.gene_ss:
                if z[0] < k[0] and z[1] > k[1]: #if the gene is larger than the window and the start/end coords are outside of it
                    g += 1
                if z[0] in range(k[0], k[1]+1) or z[1] in range(k[0], k[1]+1): #if the start or end cord is in the range of the window
                    g += 1
                else:
                    None
            
            j += 1
            wind_id = f'w50_{self.chrom_id[:10]}_{j}' #window size, chromosome, #
            
            with conn.cursor() as cursor:
                sql = f"INSERT INTO Windows (accession_id, chrom_id, wind_id, wind_seq_start, wind_seq_end, gene_count) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (self.accession, self.chrom_id, wind_id, k[0], k[1], g,))
                conn.commit()
                
        return self.w_kb10(l)

    def w_kb10(self, l):
        j = 0
        kb10 = 10000
        windows = []
        for i in range(0, l, kb10):
            y = i +kb10
            if y <= l:
                windows.append([i, i+kb10])
            elif y > l:
                windows.append([i, i + (l - i)])
        for k in windows:
            g = 0 #gene count   
            for z in self.gene_ss:
                if z[0] < k[0] and z[1] > k[1]: #if the gene is larger than the window and the start/end coords are outside of it
                    g += 1
                if z[0] in range(k[0], k[1]+1) or z[1] in range(k[0], k[1]+1): #if the start or end cord is in the range of the window
                    g += 1
                else:
                    None
            
            j += 1
            wind_id = f'w10_{self.chrom_id[:10]}_{j}' #window size, chromosome, #
            
            with conn.cursor() as cursor:
                sql = f"INSERT INTO Windows (accession_id, chrom_id, wind_id, wind_seq_start, wind_seq_end, gene_count) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (self.accession, self.chrom_id, wind_id, k[0], k[1], g,))
                conn.commit()
                
        return self.w_kb3(l)
                

    def w_kb3(self, l):
        j = 0
        kb3 = 3000
        windows = []
        for i in range(0, l, kb3):
            y = i +kb3
            if y <= l:
                windows.append([i, i+kb3])
            elif y > l:
                windows.append([i, i + (l - i)])
        for k in windows:
            g = 0 #gene count   
            for z in self.gene_ss:
                if z[0] < k[0] and z[1] > k[1]: #if the gene is larger than the window and the start/end coords are outside of it
                    g += 1
                if z[0] in range(k[0], k[1]+1) or z[1] in range(k[0], k[1]+1): #if the start or end cord is in the range of the window
                    g += 1
                else:
                    None
            
            j += 1
            wind_id = f'w3_{self.chrom_id[:10]}_{j}' #window size, chromosome, #
            
            with conn.cursor() as cursor:
                sql = f"INSERT INTO Windows (accession_id, chrom_id, wind_id, wind_seq_start, wind_seq_end, gene_count) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (self.accession, self.chrom_id, wind_id, k[0], k[1], g,))
                conn.commit()


    def parse_write(self, gffgen):
        for line in gffgen: #for each line in the gff generator
            if line['feature'] == 'region': 
                if 'chromosome' in line.keys():
                    if line['chromosome'] != 'Unknown':
                        if line['ID'] != self.chrom_id: #if we hit a new chromosome, reset and restart everything
                            l = len(self.gene_ss)
                            if l > 0: #if this is not the first run
                                print('running 100kb')
                                self.w_kb100()
                                #calc windows before igs deletes genes from the list, but once the list is complete.
                                self.intergenic_seq()
                                self.gene_ss = [] #reset 
                                print('next chromosome')
                                self.chrom_id = line['ID']
                                self.chrom_end = line['end']
                                with conn.cursor() as cursor:
                                    sql = f"INSERT INTO Chromosomes (accession_id, chrom_id, chrom_name, chrom_seq_start, chrom_seq_end, chrom_seq) VALUES (%s, %s, %s, %s, %s, %s)"
                                    cursor.execute(sql, (self.accession, line['ID'], line['chromosome'], line['start'], line['end'], self.get_seq(),)) 
                                    conn.commit()
                            else: #if this is the first run and the list is empty,
                                self.chrom_id = line['ID']
                                self.chrom_end = line['end']
                                with conn.cursor() as cursor:
                                    sql = f"INSERT INTO Chromosomes (accession_id, chrom_id, chrom_name, chrom_seq_start, chrom_seq_end, chrom_seq) VALUES (%s, %s, %s, %s, %s, %s)"
                                    cursor.execute(sql, (self.accession, line['ID'], line['chromosome'], line['start'], line['end'], self.get_seq(),)) 
                                    conn.commit()
                                
                                
                            

            if line['feature'] =='gene':
                if line['ID'] != self.gene_id:#when we hit a new gene, reset the property so we can use it for subsequent exons
                    self.introns()
                    self.exon_ss = []
                    self.gene_id = line['ID']
                    self.gene_start = int(line['start'])
                    self.gene_end = int(line['end'])
                    
                    
                    with conn.cursor() as cursor:
                        sql = f"INSERT INTO Genes (accession_id, chrom_id, gene_id, gene_seq_start, gene_seq_end) VALUES (%s, %s, %s, %s, %s)"
                        cursor.execute(sql, (self.accession, self.chrom_id, self.gene_id, line['start'], line['end'],))
                        conn.commit()
                    
                    self.flanking([int(line['start']), int(line['end'])])
                    self.gene_ss.append([int(line['start']), int(line['end'])]) #use this running list to calculate intergenic seqs once the chromosome is over

                
            if line['feature'] == 'exon':
                with conn.cursor() as cursor:
                    sql = f"INSERT INTO Exons (accession_id, chrom_id, gene_id, exon_id, exon_seq_start, exon_seq_end) VALUES (%s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (self.accession, self.chrom_id, self.gene_id, line['ID'], line['start'], line['end'],))
                    conn.commit()
                    
                self.exon_ss.append([int(line['start']), int(line['end'])]) 
                
            else:
                None 
                

#-- SET GLOBAL max_allowed_packet=1073741824; before running script. might have to do it manually, sometimes this doesn't work.
with conn.cursor() as cursor:
    sql = "SET GLOBAL max_allowed_packet=1073741824;"
    cursor.execute(sql)
    conn.commit()
    
    
  
t1 = parse_upload()
t1.csv_data()




#ISSUES
#- one igs out of 3 chromosomes  has a start larger than the end, and it is only one bp long: 'igs_CM019148.1:1..375026955_3817  igs_start = 362322228 igs end = 362322227, chrom_id = CM019148.1:1..375026955'
#- same for introns, a small amount of 1-2bp long seq are backwards. 
# im dropping it for now but need to figure out why it happened before we do the real thing
#find a way to make this faster
