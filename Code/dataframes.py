import pandas as pd
import pymysql
from sqlalchemy import create_engine, URL, text
import matplotlib.pyplot as plt
import matplotlib.cbook as pltc


engine = create_engine("mysql+pymysql://root:td2001@localhost:3306/ncbi")
connection = engine.connect()

def flankGC3_analysis(): # each gene in the genome, give me all of the exons, join the chrom seq, return the seq and find gc3 per exon, store the values, calc gc3 for gene
    query = "SELECT genes.gene_id, (SELECT SUBSTR(chromosomes.chrom_seq, exon_seq_start, (SELECT exon_seq_end - exon_seq_start FROM chromosomes LIMIT 1))) AS seq FROM exons JOIN genes ON genes.gene_id = exons.gene_id JOIN chromosomes ON chromosomes.chrom_id = exons.chrom_id ORDER BY genes.gene_id LIMIT 10;"
    df = pd.read_sql(query, con = connection) #makes a dataframe out of the sql result
    genes = df.iloc[:,0].unique() #get list of IDs
    ex_gcc = {i:[] for i in genes} #make dictionary with empty list for each one
    
    for i in genes:
        exons = df['seq'].where(df.iloc[:,0] == i).dropna() #identify the exons that belong to the gene
        for j in exons: #calculate for each exon
            h = j[0:len(i):3] #change to include 3rd position only
            gc = h.count('G')
            cc = h.count('C')
            nc = h.count('N')
            gcc = (gc +cc) / (len(h) - nc)
            ex_gcc[i].append(gcc)
        l = len(ex_gcc[i])
        s = sum(ex_gcc[i])
        gene_gc3 = s/l
        ex_gcc[i] = gene_gc3 #the dict now has the gene gc3
       
    query = 'CALL flank_gc;'
    connection.execute(text(query))
    df = pd.read_sql('SELECT * FROM flank_analysis;', con = connection) #get data from flanking gc content calculation in sql per gene as a df
    df['geneGC3'] = df['gene_id'].map(ex_gcc) #havent tested if this works yet.
    #insert into df['ex_gcc'] the flanking gcc where the gene id matches
    print(df.head())
            
            
            
flankGC3_analysis()
    

#also calculate gc3 using seq from sql
# https://matplotlib.org/stable/gallery/statistics/bxp.html#sphx-glr-gallery-statistics-bxp-py 

def igs_aanlysis():
    query = 'CALL igs_gc;'
    connection.execute(text(query))
    df = pd.read_sql("SELECT * FROM igs_analysis;", con = connection)
    f = open('dumb.txt', 'w')
    f.write(f'{list(df.iloc[:,0][:100])} \n \n {list(df.iloc[:,1][:100])}')
    f.close()


# need to be able to order all things by accession. call the procedure multiple times?
  