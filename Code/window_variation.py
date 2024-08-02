import numpy as np
import os
import re
import json
import ast
#make a folder of all of the fnas
#for every file in the folder...


class adams_gff_gen():
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



class window_variation():
    def __init__(self) :
        self.self = self 
        
    def fna_gen(self, fnap): #generator for each line in the fna 
        with open(fnap, 'r') as fh:
            for line in fh:
                yield line
                
    def get_seq(self, accession, chrom_id, fnap):  #get seq from the chrom given
        fna_g = self.fna_gen(fnap) 
        sequences = []
        print('searching for seq')
        for line in fna_g:
            if line.startswith(">"):
                if chrom_id[:10] in line or chrom_id[:11] in line or chrom_id[:17] in line:  #covers all i think. change to .partition?
                    x = next(fna_g) #go to the first line of the seq- this should never reach the end, but the next one might if its the last chrom
                    while not x.startswith(">"):
                        l = x.rstrip()
                        sequences.append(l.upper())
                        try:                             
                            x = next(fna_g)
                        except StopIteration:
                            x = ">"
        print('joining seq for current chromosome')
        seq = "".join(sequences)
        return self.w_kb100(seq, accession) 
    
    def w_kb100(self, seq, accession): #calculate the gc for that chrom
        window_gcc = []
        l = len(seq)
        kb100 = 100000
        print('making windows')
        for i in range(0, l, kb100):
            y = i +kb100
            if y <= l:
                w = seq[i:i+kb100]
            elif y > l:
                w = seq[i:i + (l - i)]
            nc = w.count('N')/ len(w)
            g = w.count('G')
            c = w.count('C')
            if nc > .5:
                None
            else:
                if g + c != 0 or len(w)-nc != 0:
                    gcc = (g + c) / (len(w) - nc) 
                    window_gcc.append(gcc)
                else:
                    None
        if len(window_gcc) > 0: 
            std = np.std(window_gcc)
            stds[accession].append(std) 
            print(stds)
            
        
stds = {i:[] for i in os.listdir(r"\Users\tyler\dataset\ncbi_dataset\data") if 'GC' in i} #list of stds for each chromosome in the genome  
today_wv= window_variation()
today_gff = adams_gff_gen()

#this was ran first to get all of the chromosome IDs. It is very slow and could be done in a more efficient way.

#chroms = {i:[] for i in os.listdir(r"\Users\tyler\dataset\ncbi_dataset\data") if 'GC' in i}
#for i in os.listdir(r"\Users\tyler\dataset\ncbi_dataset\data"): #for every accession
 #   if 'GC' in i:
  #      gp = today_gff.lines(fr"\Users\tyler\dataset\ncbi_dataset\data\{i}\genomic.gff")
   #     for line in gp:
    #        if line['feature'] == 'region':
     #           if 'chromosome' in line.keys():
      #              if line['chromosome'] != 'Unknown':
       #                 chroms[i].append(line['ID']) #should be the format for the fna, list od all chroms for an accession-- some are identical up to 11....see if fna id is a substring of the id?
    #print(chroms)
#chromtxt = open('chroms.txt', 'w')
#chromtxt.write(json.dumps(chroms))
#chromtxt.close()

with open('chroms.txt') as file: 
    data = file.read() 
chroms = ast.literal_eval(data)


for i in os.listdir(r"\Users\tyler\dataset\ncbi_dataset\data"):
    if 'GC' in i:
        for j in os.listdir(fr"\Users\tyler\dataset\ncbi_dataset\data\{i}"):
            if '.fna' in j:
                for k in chroms[i]: #for each accession list of chroms
                    print(f'calling {i}, {k}')
                    today_wv.get_seq(i, k, fr"\Users\tyler\dataset\ncbi_dataset\data\{i}\{j}")
                    

stdtxt = open('std.txt', 'w')
stdtxt.write(json.dumps(stds))
stdtxt.close()
    
print('summing up all stds')                    
for i in stds.keys():
    if len(stds[i]) > 0:
        s = sum(stds[i])
        l = len(stds[i])
        total_std = s/l #right? average of all stds?
        print(i, total_std)
        with open('std.txt', 'a') as writer:
            writer.write(f'\n\n{i}, {total_std}')
            writer.close()
    else:
        None
   
#Results:
"""
GCA_009733165.1 0.041204202061625624
GCA_020142125.1 0.018561921785926135
GCA_039797435.1 0.035079462219099675
GCA_947686815.1 0.021571088968925862
GCF_004329235.1 0.02103208820533652
GCF_009769535.1 0.032123306063717744
GCF_009819535.1 0.02238660881365952
GCF_019175285.1 0.028946539740487828
GCF_023053635.1 0.025337207520752723
GCF_027172205.1 0.02194047109570835
GCF_027244095.1 0.029377944079231753
GCF_028583425.1 0.021917409526061672
GCF_028640845.1 0.025244203068480096
GCF_029931775.1 0.02359147085961867
GCF_030035675.1 0.0207682494044729
GCF_032191835.1 0.02544957763041557
GCF_035046505.1 0.025132020241740216
GCF_035149785.1 0.03185880043500275
GCF_035594765.1 0.019328844526211936
GCF_963506605.1 0.022629825426128725
"""
                    
