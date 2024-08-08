# Fujita-Lab--Project
Updated summation of the work completed for the Fujita Lab at the University of Texas at Arlington in the Summer of 2024. Reference for any PhD students looking to replicate or modify any methods.

Contact info for any questions: tyler.dixon.b@gmail.com

### Purpose and Goals
- Create an automatically updating MySQL database for all complete, annotated, and chromosome-level Squamate genomes from NCBI.
- Use the database as a method for analyzing GC content among different parts of each chromosome, and among species.

### Why Study GC Content in Squamates?
Our DNA, made of 'Adenine - Thymine' and 'Cytosine - Guanine' pairs, is constantly mutating due to replication errors and environmental factors. Mutation is the basis for all variety and responsible for the diverse life we have on Earth. When we have mutations, there is a phenomenon called 'mutation bias' that preferentially converts GC -> AT (transversion). Evolutionary biologists are interested in the mechanism of maintinence of GC content in genomes and why mutation bias hasn't eliminated G's and C's altogether. So far, it has been found that gene density and GC content are positively correllated, that GC content is more involved in gene expression than AT, and that areas of recombination have higher GC content and consequently experience stronger selection.
Studying Squamates is of interest to the Fujita Lab because the Green Anole (Squamate), upon sequencing, was found to have less variability in GC content than other vertebrates. This suggests there may be a novel relationship in Squamates to maintain GC content. Our goals are to study diversity of GC content in Squamates amongst themselves, and in relation to vertebrates

## Data
### .gff Files
- Text data organized line-by-line, around 0.1GB in size. Consists of annotations for its respective FNA: string coordinates, IDs and various other information for all identified genes, chromosomes, exons, etc.
### .fna Files
- Text data organized line-by-line, around 2GB in size. Consists of a line to describe each chromosome or scaffold, then the sequence in successive lines of 80 characters.

We dealt with 21 genomes.

## Summary of work
### MySQL Database Design
In the folder 'SQL' you will find the files that show the database script, the model file, and the stored procedures we used to analyze the data. 

![db3pic](https://github.com/user-attachments/assets/97fbadc4-7178-4582-9f33-c4489871c34b)


### Brief Description of Files
**numos.py** *(stands for ncbi updates macOS)*

class NCBI_auto_updates()
- Checks NCBI (ncbi.nlm.nih.gov), using their command-line interface, for any new genomes that are not in the existing collection on our local computer. 
- If it finds new data, it checks for and handles duplicates, downloads the new data, then writes a CSV for easy-viewing and access to file paths.
- A text file is written with a log of each update, a record of changes, successes, and failures.
- An archive of the last metadata file you had before the update is saved.
- A text file 'data_to_upload.txt' with the list of data to be uploaded to MySQL is created to be used in the next class.

class parse_upload()
- Reads 'data_to_upload.txt' into a list, then accesses the file paths in the CSV with those accession numbers.
- Calculates and writes the data we need from the GFFs and FNAs to the MySQL database as it iterates through each GFF line-by-line.

class adams_gff_gen()
- Written by my advisor and PHD student Adam Rosso to make it easier to get the data from the gffs. *(Converts them to a dictionary like the 'json' python package does.)*

This script is set using MacOS Crontab to run every Sunday at 11pm. https://theautomatic.net/2020/11/18/how-to-schedule-a-python-script-on-a-mac/

**dataframes.py**
- Takes information from MySQL to be further analyzed and/or graphed in python.

**window_variation.py**
- Used to determine most and least variable genomes by GC content amongst 100kb windows.
- **Data** folder was derived from this script for quick use in future analyses. Contains all of the genomes and chromosome IDs we used. 

# Analysis
### General Process
- Data is matched to its relatives with the established MySQL relationships, basic joins, and subqueries. Sub-sequences are 'cut' from the main chromosome sequence with the coordinates given in or calculated from the GFF.
- Stored procedures for various desired analyses assign variables, create temporary tables, and use loops to calculate GC content (Number of 'G' and 'C' per sequence  divided by the length of the sequence minus any 'N' content, which is 'unknown').
- Data is taken from temporary tables and queries and converted to Pandas dataframes for further analysis and visualization.

### Vizualization
This set of boxplots represents GC content for the intergenic sequences of the most variable and least variable genomes, respectively. Variability was determined by the average standard deviation for GC content per 100kb window (window_variation.py).
The sequences were put into 10 bins based on length. 
(The mean lines are included as dotted lines)

Modeled after this paper: https://pubmed.ncbi.nlm.nih.gov/21795750/
![Screenshot 2024-08-07 222537](https://github.com/user-attachments/assets/51b9030a-415b-4f84-98e6-a9c44d6deaf6)

![Screenshot 2024-08-07 222120](https://github.com/user-attachments/assets/48a83182-e993-4d84-88b1-ad855436d1fe)




## Requirements and Assumptions for the script to run
- This version was written for MacOS High Sierra
- You must have the NCBI 'datasets' command-line interface downloaded and in your PATH. Instructions for adding to your PATH are under the 'Code' folder --> 'add_cli_to_PATH.txt'.
- You must have a local collection of genomes already downloaded on your computer. The package must be unzipped and rehydrated. The folder with the genomes must only have the genomes, the data catalog and metadata(renamed as <taxon>.jsonl) must be moved to the previous folder.
- This script was written for annotated genomes with the gff3 files. 
- This script was written for genomes with a chromosome-level assembly



## Changes that must be made to the script for it to run for you
- Open the script and adjust the paths indicated in the comment boxes before each class.
- Any deviations from the original purpose (different database design, different taxa, different genomes, no annotations, etc.) will require edits. 


# Issues
- Working with 'big data' like this was, and still is, a learning curve for optimization. Including all of the different sized windows we want drastically increases the upload time to something unreasonable. Downloading to a .csv for bulk insert isn't much faster.
- The GFF files we used are very heterogenous; this code was written specifically to tackle the issues we could see with our 20 genomes and may need changing for any expansions or change of taxon. Examples of these issues include:
  - Different naming conventions for the headers Ex:'assembly_info' vs 'assemblyInfo.'
  - Different parents among regions for the gffs, making it harder to connect exons to genes. Ex: An exon could have an 'mrna', 'gene', or 'ID' parent.
  - Different lengths and conventions of IDs.
  - Some have no names for the chromosomes, causing datatype mismatches in MySQL.
  - The data had no direct relation to the chromosome it belonged to besides ocurring after it in the file- this requires us to iterate line-by-line, which is slow.
  


# Future Work
- This code was written, to the best of my ability, with RAM and speed in mind. The program is still quite slow and I believe that the speed could be improved upon.
- Use BUSCO for annotations rather than the GFFs for more reliable and uniform data.
- Find a way to quickly get window information written to sql. Adding windows of 3kb, 10kb, 50kb, and 500kb exponentially raised the process time, so we only included the 100kb windows for now.
- Tying in with the previous point, find a way to do the initial bulk upload of data quickly and efficiently, possibly with a bulk insert.
- Fix small bug in class parse_upload() functions: igs, introns. Leaves small bits of invalid data that is insignificant to our analyses, but it would be nice to not have to delete them.
