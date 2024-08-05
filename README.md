# Fujita-Lab--Project
Updated summation of the work completed for the Fujita Lab at the University of Texas at Arlington in the Summer of 2024. Reference for any PhD students looking to replicate or modify any methods.
Contact info for any questions: tyler.dixon.b@gmail.com

### Purpose and Goals
- Create an automatically updating MySQL database for all complete, annotated, and chromosome-level Squamate genomes from NCBI.
- Use the database as a method for analyzing GC content among different parts of each chromosome, and among species.

### Why Study GC Content in Squamates?
Our DNA, made of 'Adenine - Thymine' and 'Cytosine - Guanine' pairs, is constantly mutating due to replication errors and environmental factors. Mutation is the basis for all variety and responsible for the diverse life we have on Earth. When we have mutations, there is a phenomenon called 'mutation bias' that preferentially converts GC -> AT (transversion). Evolutionary biologists are interested in the mechanism of maintinence of GC content in genomes and why mutation bias hasn't eliminated G's and C's altogether. So far, it has been found that gene density and GC content are positively correllated, that GC content is more involved in gene expression than AT, and that areas of recombination have higher GC content and consequently experience stronger selection.
Studying Squamates is of interest to the Fujita Lab because the Green Anole (Squamate), upon sequencing, was found to have less variability in GC content than other vertebrates. This suggests there may be a novel relationship in Squamates to maintain GC content. Our goals are to study diversity of GC content in Squamates amongst themselves, and in relation to vertebrates

## Summary of work
### MySQL Database Design
In the folder 'SQL' you will find the files that show the database script, the model file, and the stored procedures we used to analyze the data. 

![ncbi_db_p](https://github.com/user-attachments/assets/2f869eca-aa7c-4298-a7a7-8c794da172f5)

### Brief Description of Files
**numos_27.py**

class NCBI_auto_updates()
- It checks NCBI (ncbi.nlm.nih.gov), using their command-line interface, for any new genomes that are not in our existing collection on our local computer. 
- If it finds new data, it checks for and handles duplicates, downloads the new data, then writes a CSV to be used in the inheriting class.
- A text file is written with a log of each update, a record of changes, successes, failures.
- An archive of the last metadata file you had before the update is created.

class parse_upload()
- Takes a given list of genomes and calculates the sequence coordinates for introns, windows, intergenic sequences, and flanking sequences.
- Parses information given in the GFF.
- Writes the data we need to the MySQL database.

class adams_gff_gen
- Written by my advisor and PHD student Adam Rosso to make it easier to get the data from the gffs. (Converts them to a dictionary like the json package does)

*once the process is properly streamlined, the numos_27.py file can be made into an executable using pyinstaller to auto-update*

**dataframes.py**
- Takes information from SQL to be further analyzed and/or graphed in python.

**window_variation.py**
- Used to determine most and least variable genomes by GC content amongst 100kb windows.

# Analysis
- A preliminary analysis to show that the project was a success.

This set of graphs represents GC content for the intergenic sequences of the most variable and least variable genomes, respectively. Variability was determined by the average standard deviation for GC content per 100kb window (window_variation.py).
The sequences were put into 10 bins based on length. As you can see, there is an inverse relationship with GC content and sequence length. 
(The mean lines are included as dotted lines)
![Screenshot 2024-08-03 143832](https://github.com/user-attachments/assets/10e39419-17d7-4387-b3c7-1d6eda1def99)

![Screenshot 2024-08-03 144629](https://github.com/user-attachments/assets/8efbd252-b7df-4429-97e3-3972bc21aff1)



## Requirements and Assumptions for the script to run:
- This version was written for MacOS High Sierra
- You must have the NCBI 'datasets' command-line interface downloaded and in your PATH. https://www.ncbi.nlm.nih.gov/datasets/docs/v2/download-and-install/ (add instructions for how to put in path - on mac)
- You must have a local collection of genomes already downloaded on your computer. The package must be unzipped and rehydrated. The folder with the genomes must only have the genomes, the data catalog and metadata must be moved to the previous folder.
- This script was written for annotated genomes with the gff3 files. 
- This script was written for genomes with a chromosome-level assembly



## Changes that must be made to the script for it to run for you:
- Open the script and adjust the paths indicated in the box at the very top. 
- Any deviations from the original purpose (different database design, different taxa, different genomes, no annotations, etc.) will require edits. 


# Issues:
- The data we are using is very large. Working with 'big data' like this was, and still is, a learning curve for optimization. Including all of the different sized windows we want drastically increases the upload time to something unreasonable. Downloading to a csv for bulk insert isn't much faster.
- The GFF files we used are very heterogenous; this code was written specifically to tackle the issues we could see with our 20 genomes and may need changing for any expansions or change of taxon. Examples of these issues include:
  - Different naming conventions for the headers Ex:'assembly_info' vs 'assemblyInfo.'
  - Different parents among regions for the gffs, making it harder to connect exons to genes. Ex: An exon could have an 'mrna', 'gene', or 'ID' parent.
  - Different lengths and conventions of IDs.
  - Some have no names for the chromosomes, causing datatype mismatches in MySQL.
  - The data had no direct relation to the chromosome it belonged to besides ocurring after it in the file- this requires us to iterate line-by-line, which is slow.
  
  
  
  


# Future Work:
- Streamline the process of updating, downloading, uploading, and data analysis to one executable that works on GFFs with different formats. The files are currently separate.
- This code was written, to the best of my ability, with RAM and speed in mind. The program is still quite slow and I believe that the speed could be improved upon.
- Use BUSCO for annotations rather than the GFFs for more reliable and uniform data.
- Find a way to quickly get window information written to sql.
- Fix bug in class parse_upload() functions: igs, introns.
