import os
import subprocess
import csv
import pymysql
import numpy as np
from Bio.SeqIO import parse
import itertools 
import json
import jsonlines
import datetime
from datetime import date
import shutil
import sys
import pandas as pd
import pathlib
import re
import gzip
import ast



# Hi :)
###########################################################################################################################################################################################################
#                                                                                                                                                                                                         #
#                  CHECK THESE CLASS PROPERTIES BEFORE RUNNING THE PROGRAM:                                                                                                                              #
#   -local_genomes_folder_pathway  #the folder that contains your rehydrated genomes(fna files) and records_updates and jsonl and csv file                                                                 #
#   -local_genomes_jsonl_pathway   #JSON FOR SPECIFIC TAXON OR INFO YOU NEED IF THERE ARE MULTIPLE GENOME COLLECTIONS ON THE COMPUTER.                                                                     #
#   -taxon   #add to this list if you want more or different taxa checked and downloaded                                                                                                                   #
#   -ncbi_tags                                                                                                                                                                                             #
#   THIS IS WHAT YOUR NCBI_TAGS SHOULD LOOK LIKE OR THINGS WONT WORK:                                                                                                                                     #
#   ncbi_tags = f'./datasets summary genome taxon {self.taxon} --annotated --assembly-level chromosome --assembly-level complete --assembly-source refseq --as-json-lines > {self.taxon}_updates.jsonl' 
#   -conn properties for MySQL connection
#
#   - mysql data in conn if using a different database or host or something
#   - mysql data in uploads function [line 394ish] because it is in the string as ncbi, not a variable at the moment.
#                                                                                                                                                                                                         #
###########################################################################################################################################################################################################

#   HOW TO RUN THE PROGRAM
# -Check the github for configuration info and how to set up your local data and sql database.
#       https://github.com/tielyrr/Fujita-Lab--Project

# If you want to run a check and an upload, leave these un-commented at the end of the script:
#       today = numos()
#       today.check_records()
#       today.do_mac_setup()
#       today.check_for_new_data()
#       today.files()
#       today.csv_data()

# If you want to just run a check to make the csv, stop after today.check_for_new-data()
# If you want to just do an upload of one or more specified genomes without a check (like for initial database setup):
#       today.species('GCA_020142125.1', '/Users/biollab-120475/Desktop/ncbi_dataset/data/GCA_020142125.1/ncbi_dataset/data/GCA_020142125.1') how it can be called if you just want one genome and dont want to use the csv data. 
# If wanting to run without update check or csv data, edit the csv_data() [line 400ish] function to say for every i in successfully_uploaded_ data and use f string to change end of string above



conn = pymysql.connect(  #connection to sql for single-line uploads.
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
        self.csv_path = ''
        self.local_genomes_folder_pathway = r'/Users/biollab-120475/Desktop/ncbi_dataset/data' #folder with all genomes in it
        self.local_genomes_jsonl_pathway = r'/Users/biollab-120475/Desktop/ncbi_dataset/squamata.jsonl'  
        self.local_folder = r'/Users/biollab-120475/Desktop/ncbi_dataset' #directory above folder with all genomes in it, for storing csv and records files
        self.taxon = 'squamata'
        self.ncbi_tags = f'datasets summary genome taxon {self.taxon} --annotated --reference --assembly-level chromosome --assembly-level complete --as-json-lines > {self.taxon}_updates.jsonl'
        self.updates_file_path = []
        self.data = [] #used for updating what is and isnt going to be downloaded throughout the first half of the script
        self.successfully_downloaded_data = []
        ###############properties below are for second half of script: uploading.###################
        self.sp_path = ''#'/Users/biollab-120475/Desktop/ncbi_dataset/data/GCA_020142125.1/ncbi_dataset/data' #path to accession folder with gff and fna
        self.sp_id = ''#'GCA_020142125.1'
        self.c_id = '' #chromosome id, will reset with each iteration of the loop
        self.chrom_end = '' #will also update
        self.gene_ss = {} #start/stop lists
        self.exon_ss = []
        
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


 ################################################################                          
 ################################################################
 ##  Everything past here is only if new data has been found.  ##
 ################################################################     
 ################################################################ 

 
    def find_duplicates(self): 
        # if duplicates are found, we will delete all old files, replace them with updated ones in directory, then go to sql and delete cascade everything with that accession - make new data
        # only issue is sometimes updates change the accession to a .3 or .2, in that case 2 different accessions would reference the same genome, just one more updated
        # so i cant check if the accessions are equal anymore... just the data before the decimal and then after the decimal, then do a replacement for those. also a regular 
        # equality check, though, just in case they did not change the accession with the update.

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
        
        for i in self.data:
            os.chdir(self.local_genomes_folder_pathway)  #download all new data to the right directory
            exit_value = os.system(f"datasets download genome accession {i['accession']} --include genome,gff3 --filename {i['accession']}.zip") #this runs the command and stores the exit value
            if exit_value != 0: #if the download was unsuccessful or incomplete in any way
                r_data = f"\n****************EXIT VALUE ERROR: {exit_value} for {i['accession']} --DOWNLOAD UNSUCCESSFUL--\nACTION REQUIRED: FILE METADATA NOT WRITTEN ONTO LOCAL JSONL OR CSV-- CHECK WORKING DIRECTORY FOR INCOMPLETE DATA\n***************\n"
                self.records_writing(r_data)
            else:
                r_data = f"\nDownload successful for {i['accession']}"
                self.successfully_downloaded_data.append(i['accession']) #for next class to read
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
                self.csv_path = f'{self.local_folder}/{self.taxon}_metadata.csv'
            
                return None


########################################################################################
########################################################################################
# This is now the second half of the script that's responsible for uploading the data. ## I could try and do child classes but can i update parent class properties from a child class?
########################################################################################
########################################################################################


    def files(self): #write all files to be used for bulk inserts so functions can access and append to them as needed.
        print('writing tsv files')
        #change directory to sql uploads, this is where they are all stored.
        os.chdir('/Users/biollab-120475/mysqlUploads')  
        with open('gene_records.tsv', 'w', newline='') as tsvfile: 
            writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n') #tab separated files are easily uploaded to MySQL
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
            
    def upload(self, filepath, fields, table): #bulk insert to sql -- *** adjust database name if changed ***
        with conn.cursor() as cursor:
            cursor.execute(f"LOAD DATA LOCAL INFILE '{filepath}' INTO TABLE ncbi.{table} FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n' IGNORE 1 LINES ({fields});")
            conn.commit()
        return None #return a successful or unsuccessful value in the future? So we can catch it and make a record before moving on. So far, I can't get it to give me errors.

    def csv_data(self): #Will run the loop for every genome. 
        print('reading csv...')
        df = pd.read_csv(self.csv_path)
        for i in self.successfully_downloaded_data: #this is the loop that the whole update will ride on for each accession-- if empty, nothing will happen.
            print(i)
            index_of_accession = np.where(df["accession"] == i) #find the accession in the file so we can get the path
            gp = f'{df.loc[index_of_accession]["path_to_gff"].item()}'
            p = gp[:-11] #just need path to folder with data in it, using gff path and subtracting the 11 characters for 'genomic.gff'
            print(p)
            self.species(i, p) #will initiate upload of all info

            

    def species(self, sp_id, sp_folder_path): #will set the class property values and insert the info for the species table so all other data can be uploaded
        print('on species function') 
        self.sp_path = sp_folder_path
        self.sp_id = sp_id
        with conn.cursor() as cursor:
            sql = f"INSERT INTO Species (accession_id) VALUES (%s)"
            cursor.execute(sql, (sp_id)) 
            conn.commit()
        return self.chromosomes()


    def chromosomes(self): #starts cascade of functions and uploads for each chrom within the genome
        print('on chrom function')
        os.chdir(self.sp_path) #get to the gff
        chroms = subprocess.run(["cut -f 9 genomic.gff | cut -d ';' -f 4 | grep -i -n 'chromosome='| less"], shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip().split('\n') #get output for all chromosomes with line numbers
        
        for i in chroms: #does the loop for the whole genome, each chrom. 
            if len(i) > 0:
                i = i.split(':') #split the string after the line number
                os.chdir(self.sp_path) #gets lost here if this isnt here
                romo = subprocess.run([f"sed -n '{i[0]}'p genomic.gff"], shell = True, stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip().split('\t') #use the line numbers to grab the line of the chromosome you want
                rom = romo[-1].split(';')[2].split('=')[1] #get the chrom name by splitting the last gff column info by ; and getting what's after the = in column 2 of the split
                l, seq = self.get_seq(romo[0]) #get the length of genome and genome seq
                with conn.cursor() as cursor:
                    sql = f"INSERT INTO Chromosomes (accession_id, chrom_id, chrom_name, chrom_seq_start, chrom_seq_end, chrom_seq) VALUES (%s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (self.sp_id, romo[0], rom, romo[3], romo[4], seq,)) #indexes for romo are the splits in  the last column for the gff 
                    conn.commit()
            
                self.c_id = romo[0] #reassign with each one
                self.chrom_end = l
                self.genes(l) #dont return or else it wont do the loop, l for windows later


    def get_seq(self, cid): #takes a minute. called when chromosome is resetting
        print('on seq function')
        fnap = [] #fna path
        for i in os.listdir(self.sp_path): #change to an if statement? get rid of unecessary loops?
            if i != 'genomic.gff':
                fnap = i
        for seq_record in parse(fnap, "fasta"): #biopython method for getting string by finding the matching chrom id
            if cid in seq_record.id:
                return len(seq_record.seq), seq_record.seq 

            
    def genes(self, l): 
        print('on genes function')
        results = [] #to store records for writing to tsv file
        g = subprocess.run([f'grep "^{self.c_id}.*ID=gene.*" genomic.gff | less'], shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip().split('\n') #get all genes for current chromosome
        self.gene_ss = {} #reset for each chrom so we can properly caculate igs and windows gene counts
        for i in g: #for each gene in the chromosome
            if len(i) >1: #theres an empty space at the end for some reason
                i = i.split('\t') #split the line on tabs
                ene = {} #info for gene
                ene['accession_id'] = self.sp_id
                ene['chrom_id'] = self.c_id
                ene['gene_id'] = i[-1].split(';')[0][3::] #split that last gff column again, gene_id is column 3
                ene['strand'] = i[6]
                ene['start'] = i[3] 
                ene['end'] = i[4]

                results.append(ene)

                self.gene_ss[ene['gene_id']] = [int(ene['start']), int(ene['end'])] #allows introns to get gene parent in this format with self.intron_gids
                self.flanking(ene['gene_id'], ene['strand'], [int(ene['start']), int(ene['end'])])  #call the flanking function for each gene, it only writes and doesn't upload yet

        os.chdir('/Users/biollab-120475/mysqlUploads')
        with open('gene_records.tsv', 'a') as tsvfile: #write all records at once
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
            j += 1 #for naming
            flank_id = f'f_{gid}_{j}' #adding the gene_id makes it unique

            flank_rec = {'accession_id':self.sp_id, 'chrom_id':self.c_id,'gene_id': gid, 'flank_id':flank_id, 'flank_strand':strand,'up_start':upstart, 'up_stop':upend, 'down_start':downstart, 'down_end':downend}
            os.chdir('/Users/biollab-120475/mysqlUploads')
            with open('flank_records.tsv', 'a') as tsvfile:
                    writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
                    writer.writerow(flank_rec.values()) 
        #dont upload because the genes havent been inserted to the database yet-- violates foreign key constraints
        return None


    def windows(self, l):
        print('on windows function')
        kbs = [500000,100000,50000,10000,3000] #kb sizes you want
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
                    if gene_end < window_start or gene_start > window_end:  # if the gene is not in the window in any way- completely outside, skip it
                        continue
                    g += 1  # Overlapping or contained gene

                j += 1
                size = int(b/1000) #easier for id
                wind_id = f'w{size}_{self.c_id[:10]}_{j}' #window size, chromosome, #
                    
                window_rec = {'accession_id':self.sp_id, 'chrom_id':self.c_id,'wind_id':wind_id, 'wind_seq_start':window_start, 'wind_seq_end':window_end, 'gene_count':g}
                results.append(window_rec)
        os.chdir('/Users/biollab-120475/mysqlUploads')
        with open('window_records.tsv', 'a') as tsvfile: #write all at once
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
        rnas = subprocess.run([f'grep "^{self.c_id}.*ID=rna.*" genomic.gff | less'], shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip().split('\n') #get all rnas for the chrom ur on
        for i in rnas:
            p = i.split('\t')
            p2 = p[-1].split(';') #parent info in last gff column
            rnaid = p2[0][3::]
            grandparent = p2[1][7::] #gene id
            grandparents[rnaid] = grandparent

        os.chdir(self.sp_path) #get to the directory with ur file
        exs = subprocess.run([f'grep "^{self.c_id}.*ID=exon.*" genomic.gff | less'], shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip().split('\n') #gives me all exons for chromosome
        for i in exs: #for each exon
            e = i.split('\t') #break it
            e2 = e[-1].split(';') #break the last field
            if 'gene='in e2:
                exon_rec = {'accession_id':self.sp_id, 'chrom_id':self.c_id, 'gene_id': f"gene-{grandparents[e2[5]]}",'exon_id':e2[0][3::], 'exon_strand':e[6],'exon_seq_start':e[3], 'exon_seq_end':e[4]} #search grandparents dict for rnaid to get gene parent
                print(exon_rec)
                results.append(exon_rec)
                self.exon_ss.append([int(e[3]), int(e[4])]) #for the intron function
            elif 'Parent=gene' in e2[1]:
                exon_rec = {'accession_id':self.sp_id, 'chrom_id':self.c_id, 'gene_id': e2[1][7::],'exon_id':e2[0][3::], 'exon_strand':e[6],'exon_seq_start':e[3], 'exon_seq_end':e[4]} 
                results.append(exon_rec)
                self.exon_ss.append([int(e[3]), int(e[4])]) #for the intron function
            elif 'Parent=rna' in e2[1]:
                exon_rec = {'accession_id':self.sp_id, 'chrom_id':self.c_id, 'gene_id': grandparents[e2[1][7::]],'exon_id':e2[0][3::], 'exon_strand':e[6],'exon_seq_start':e[3], 'exon_seq_end':e[4]} #search grandparents dict for rnaid to get gene parent
                results.append(exon_rec)
                self.exon_ss.append([int(e[3]), int(e[4])]) #for the intron function
            else:
                print(f'new parent found. record {i} not added to database')

        os.chdir('/Users/biollab-120475/mysqlUploads')
        with open('exon_records.tsv', 'a') as tsvfile: #write all at once
            writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
            for rec in results:
                writer.writerow(rec.values())

        self.upload('/Users/biollab-120475/mysqlUploads/exon_records.tsv', 'accession_id, chrom_id, gene_id, exon_id, exon_strand, exon_seq_start, exon_seq_end', 'Exons')

        self.cds(grandparents)
        self.fix_overlap(self.exon_ss) #do the introns now that the exon_ss list is complete. need the gene_ss as a dict to get keys, igs function changes the dict to a list so it is called after. Didn't end up changing the class property anyways, so the order of these two doesnt matter but i kept it this way just in case. 
        self.fix_overlap(self.gene_ss) #we can mess up the gene list now for igs,
        return None


    def cds(self, grandparents): #just like the exon function
        print('on cds function')
        results = []
        os.chdir(self.sp_path) #get to the directory with ur file
        cdss = subprocess.run([f'grep "^{self.c_id}.*ID=cds.*" genomic.gff | less'], shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip().split('\n') #gives me all exons for chromosome
        for i in cdss: #for each cds
            c = i.split('\t') #break it
            c2 = c[-1].split(';') #break the last field
            if 'gene=' in c2:
                cds_rec = {'accession_id':self.sp_id, 'chrom_id':self.c_id, 'gene_id': f"gene-{grandparents[c2[5]]}",'exon_id':c2[0][3::], 'exon_strand':c[6],'exon_seq_start':c[3], 'exon_seq_end':c[4]} #search grandparents dict for rnaid to get gene parent
                print(cds_rec)
                results.append(cds_rec)
            elif 'Parent=gene' in c2[1]:
                cds_rec = {'accession_id':self.sp_id, 'chrom_id':self.c_id, 'gene_id': c2[1][7::],'cds_id':c2[0][3::], 'cds_strand':c[6],'cds_seq_start':c[3], 'cds_seq_end':c[4]} #cant use self.gene_id because this is called outside the gene loop      
                results.append(cds_rec)
            elif 'Parent=rna' in c2[1]:
                cds_rec = {'accession_id':self.sp_id, 'chrom_id':self.c_id, 'gene_id': grandparents[c2[1][7::]],'cds_id':c2[0][3::], 'cds_strand':c[6],'cds_seq_start':c[3], 'cds_seq_end':c[4]}
                results.append(cds_rec)
            else:
                print('new parent found, record not added to file:', i)
            
            
        os.chdir('/Users/biollab-120475/mysqlUploads')
        with open('cds_records.tsv', 'a') as tsvfile: #write all at once
            writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
            for rec in results:
                writer.writerow(rec.values())
        self.upload('/Users/biollab-120475/mysqlUploads/cds_records.tsv', 'accession_id, chrom_id, gene_id, cds_id, cds_strand, cds_seq_start, cds_seq_end', 'CDS')
        

        return None



    def fix_overlap(self, ss_list): #fix overlap on either genes or exons before igs and intron calcs 
        print('fixing overlaps')
        v = 0
        if type(ss_list) == dict:
            ss_list = list(ss_list.values()) #does not replace the class property
            v = 1
        else:
            None

        ss_list.sort(key=lambda x: x[0]) #sort by the start coordinate!!! 

        def merge_intervals(sorted_list):
            if not sorted_list:
                return []

            # Initialize the merged intervals list with the first interval
            merged = [sorted_list[0]]

            # Traverse through the sorted intervals
            for current in sorted_list[1:]:
                # Compare with the last merged interval
                last_merged = merged[-1]

                # If there's an overlap, merge the intervals
                if last_merged[1] >= current[0]:  # Overlapping
                    merged[-1] = (last_merged[0], max(last_merged[1], current[1]))
                else:
                    # No overlap, add the current interval
                    merged.append(current)

            return merged

        # Merge overlapping intervals
        ss_list = merge_intervals(ss_list)
        if v == 1: #if it was a dict it was the genes
            return self.igs(ss_list)
        else:
            return self.introns()


    def igs(self, ss_list): #we are now working with the edited list, no strand info for igs yet
        print('on igs function')
        j = 0 
        if len(ss_list) > 1: #if there is more than one gene, so at least one seq
            for index, i in enumerate(ss_list):
                if index < len(ss_list)-1: #if its not the last gene
                    start = int(i[1])+1 #running into errors converting to int, is this an empty string???
                    next_gene = ss_list[index+1]
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
                    intron_rec = {'accession_id':self.sp_id, 'chrom_id':self.c_id,'gene_id':key ,'inton_id':int_id, 'intron_strand':None,'int_seq_start':start, 'int_seq_end':stop}
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
                return key #also return strand
            else:
                continue #i may be skipping a lot idk yet. 






today = numos() #

today.check_records()
today.do_mac_setup()
today.check_for_new_data() 

today.files() #
today.csv_data()
#today.species('GCA_020142125.1', '/Users/biollab-120475/Desktop/ncbi_dataset/data/GCA_020142125.1/ncbi_dataset/data/GCA_020142125.1') 


############
#WORK TO DO#
############
#new parent 'id' for accession below. 'new parent found, record not added to file: NC_090026.1	Gnomon	CDS	54251889	54252244	.	+	2	ID=cds-LOC132778422;Parent=id-LOC132778422;Dbxref=GeneID:132778422;exception=rearrangement required for product;gbkey=CDS;gene=LOC132778422;product=immunoglobulin kappa variable 3-20-like'
# also this error after a long time: 
#       on cds function
#       Traceback (most recent call last):
  #     File "/Users/biollab-120475/Downloads/numos_updates 6.py", line 752, in <module>
  #     File "/Users/biollab-120475/Downloads/numos_updates 6.py", line 409, in csv_data
  #     File "/Users/biollab-120475/Downloads/numos_updates 6.py", line 420, in species
  #     File "/Users/biollab-120475/Downloads/numos_updates 6.py", line 442, in chromosomes
  #     File "/Users/biollab-120475/Downloads/numos_updates 6.py", line 488, in genes
  #     File "/Users/biollab-120475/Downloads/numos_updates 6.py", line 587, in exons
  #     File "/Users/biollab-120475/Downloads/numos_updates 6.py", line 611, in cds
#IndexError: list index out of range
#'GCF_037176765.1' 
#make sql give warnings? incorporate record writing and error catching in second half like you did in the first half. 
#change to 2 child classes? or one?
#check out ensemble and add to database


##old merging function:
"""
# Merge overlapping intervals
    ss_list = merge_intervals(ss_list)
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
"""
