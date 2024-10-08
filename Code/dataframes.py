import pandas as pd
import pymysql
from sqlalchemy import create_engine, URL, text
import matplotlib.pyplot as plt
import matplotlib.cbook as pltc
import numpy as np


engine = create_engine("mysql+pymysql://root:td2001@localhost:3306/ncbi")
connection = engine.connect()

def flankGC3_analysis(aid): # each gene in the genome, give me all of the exons, join the chrom seq, return the seq and find gc3 per exon, store the values, calc gc3 for gene
    query = f"SELECT genes.gene_id, (SELECT SUBSTR(chromosomes.chrom_seq, exon_seq_start, (SELECT exon_seq_end - exon_seq_start FROM chromosomes LIMIT 1))) AS seq FROM exons JOIN genes ON genes.gene_id = exons.gene_id JOIN chromosomes ON chromosomes.chrom_id = exons.chrom_id WHERE exons.accession_id = '{aid}' ORDER BY genes.gene_id;"
    df = pd.read_sql(query, con = connection) #makes a dataframe out of the sql result
    genes = df.iloc[:,0].unique() #get list of IDs
    ex_gcc = {i:[] for i in genes} #make dictionary with empty list for each one
    
    for i in genes:
        print('next gene')
        exons = df['seq'].where(df.iloc[:,0] == i).dropna() #identify the exons that belong to the gene
        for j in exons: #calculate for each exon
            h = j[0:len(i):3] #include 3rd position only for gc3
            gc = h.count('G')
            cc = h.count('C')
            nc = h.count('N')
            if len(h) - nc == 0 or gc+cc == 0:
                None
            else:
                gcc = (gc +cc) / (len(h) - nc)
                ex_gcc[i].append(gcc)
        l = len(ex_gcc[i])
        s = sum(ex_gcc[i])
        gene_gc3 = s/l
        ex_gcc[i] = gene_gc3 #the dict now has the gene gc3
       
    query = 'CALL flank_gc;'
    connection.execute(text(query))
    df = pd.read_sql('SELECT * FROM flank_analysis;', con = connection) #get data from flanking gc content calculation in sql per gene as a df
    df['geneGC3'] = df['gene_id'].map(ex_gcc) #insert into df['ex_gcc'] the flanking gcc where the gene id matches
    print(df.head())
            
            
            
#flankGC3_analysis('GCA_009733165.1')
    
# https://matplotlib.org/stable/gallery/statistics/bxp.html#sphx-glr-gallery-statistics-bxp-py 

def igs_analysis(a_id): #takes a little too long to complete the first query...
    query = f"CALL igs_gc('{a_id}');" #running the stored procedure
    connection.execute(text(query))
    print('making df')
    df = pd.read_sql(f"SELECT * FROM igs_analysis;", con = connection) #getting data from temporary table
    b = int(round(max(df.iloc[:,0])/10)) #we want 10 bins of = length
    print('# of datapoints:', len(df.iloc[:,0]))
    print('this range of length interval per bin:', b)
    print('max:', max(df.iloc[:,0]))
    print('making bins')
    bins = [i for i in range (0, max(df.iloc[:,0])+b, b)] #establishing the bins
    print(bins)
    l = [i for i in range(1, len(bins))] #for use below
    print(l)
    df['bin'] = (np.select([df['seq_len'].between(i, j, inclusive='right') for i,j in zip(bins, bins[1:])], l)) #adding feature to dataframe
    print(df.head())
    bs = [] #list for graph data
    j = 1
    for i in range(1, len(bins)):
        filter = df.where(df.iloc[:,2] == j).dropna() #get data for each bin and add it to the list
        print(f'number of data points in bin {i}:', len(filter))
        stats = pltc.boxplot_stats(filter['GCcontent']) #making stats for each boxplot to grapg
        bs.append(stats[0])
        j += 1
    print('graphing')
    #graph design
    boxprops = dict(linestyle='-', linewidth=1, color='black')
    medianprops = dict(linestyle='-', linewidth=.5, color='black')
    meanlineprops = dict(linestyle='--', linewidth=.5, color='grey')
    flierprops = dict(marker='o', markerfacecolor='black', markersize=1,
                  markeredgecolor='none')
    whiskerprops = dict(linewidth = .5, color = 'black')
    capprops = dict(linewidth = .5)
    
    fig, ax = plt.subplots()
    ax.bxp(bs, showmeans = True, meanline = True, flierprops = flierprops, boxprops = boxprops, medianprops=medianprops, meanprops=meanlineprops, 
       whiskerprops = whiskerprops, capprops = capprops)
    fig.set_figheight(10)
    fig.set_figwidth(10)
    ax.set_xlabel(f'Bins (Intervals of {b} Bases)')
    ax.set_ylabel('GC Content')
    ax.set_title(f'GC Content by Intergenic Sequence Length: {a_id}')
    plt.show()


# igs_analysis('GCA_009733165.1')
    

def wind_analysis():
    query = f"CALL wind_gc;" #running the stored procedure
    connection.execute(text(query))
    print('making df')
    df = pd.read_sql(f"SELECT * FROM wind_analysis;", con = connection) #getting data from temporary table
    species = df.iloc[:,0].unique() #unique accessions
    x = {i:[] for i in species}
    colors = ['grey', 'black']
    g = 0
    for i in species:
        x[i] = df['GCcontent'].where(df.iloc[:,0] == i).dropna()
        _= plt.hist(x[i], bins = 200, density = True, histtype = 'step', lw = 2, color = colors[g], label = f'{i}')
        g += 1
    _= plt.legend()
    plt.title('GC Content for 100kb Windows')
    plt.xlabel('GC Content')
    plt.ylabel('Density')
    plt.show()
   
wind_analysis()