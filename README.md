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


<img width="1037" alt="Screen Shot 2024-10-25 at 6 06 43 PM" src="https://github.com/user-attachments/assets/78803e06-db09-4e27-9919-763eca6dc27f">


### Brief Description of Files
**numos.py** *(stands for ncbi updates macOS)*

- Checks NCBI (ncbi.nlm.nih.gov), using their command-line interface, for any new genomes that are not in the existing collection on our local computer. 
- If it finds new data, it checks for and handles duplicates, downloads the new data, then writes a CSV for easy-viewing and access to file paths.
- A text file is written with a log of each update, a record of changes, successes, and failures.
- An archive of the last metadata file you had before the update is saved.
- A text file 'data_to_upload.txt' with the list of data to be uploaded to MySQL is created to be used in the next class.

- Reads data_to_upload.txt, then accesses the file paths in the CSV with those accession numbers.
- Calculates and writes the data we need from the GFFs and FNAs to the MySQL database utilizing bulk inserts.

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

This is a density plot for both genomes and their GC content by window. 
![image](https://github.com/user-attachments/assets/c7b58fde-22b9-4898-b2ea-ece9d6721c8f)


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
- I am in the process of editing the script to make up for heterogeneity in the gff files.
  

# Future Work
- This code was written, to the best of my ability, with RAM and speed in mind. I believe some optimization could improve the speed.
- Use BUSCO for annotations rather than the GFFs for more reliable and uniform data.
- Fix small bug in class parse_upload() functions: igs, introns. Leaves small bits of invalid data that is insignificant to our analyses, but it would be nice to not have to delete them.
