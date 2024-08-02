# Fujita-Lab--Project
Updated summation of the work completed for the Fujita Lab at the University of Texas at Arlington in the Summer of 2024. Reference for any PhD students looking to replicate or modify any methods.
Contact info for any questions: tyler.dixon.b@gmail.com

## Purpose and Goals
- Create an automatically updating MySQL database for all complete, annotated, and chromosome-level Squamate genomes from NCBI.
- Use the database as a method for analyzing GC content among different parts of each chromosome, and among species.

## Why study GC Content in Squamates?
Our DNA, made of 'Adenine - Thymine' and 'Cytosine - Guanine' pairs, is constantly mutating due to replication errors and environmental factors. Mutation is the basis for all variety and responsible for the diverse life we have on Earth. When we have mutations, there is a phenomenon called 'mutation bias' that preferentially converts GC -> AT (transversion). Evolutionary biologists are interested in the mechanism of maintinence of GC content in genomes and why mutation bias hasn't eliminated G's and C's altogether. So far, it has been found that gene density and GC content are positively correllated, that GC content is more involved in gene expression than AT, and that areas of recombination have higher GC content and consequently experience stronger selection.
Studying Squamates is of interest to the Fujita Lab because the Green Anole (Squamate), upon sequencing, was found to have less variability in GC content than other vertebrates. This suggests there may be a novel relationship in Squamates to maintain GC content. Our goals are to study diversity of GC content in Squamates amongst themselves, and in relation to vertebrates

## Database Design
In the folder 'SQL' you will find the files that show the database script, the model file, and the stored procedures we used to analyze the data. 
![Screenshot 2024-08-02 151032](https://github.com/user-attachments/assets/13e9e0f2-d483-494b-b6de-94381b2d0820)



This script can be set on a schedule using your computer's scheduler (Automator tool or Task scheduler). We converted it to an executable with 'pyinstaller'.
This is how it works in our lab:

It checks NCBI (ncbi.nlm.nih.gov), using their command-line interface, for any new genomes that are not in our existing collection on our local computer. 
If it finds new data, it downloads it to your collection and writes it to an existing MySQL database. 
A text file is written with a log of each update, a record of changes, successes, failures, and an archive of the last metadata file you had before the update. 

Then we utilize the MySQL database to calculate GC content among different parts of the genome, compare them, and see trends.

Analysis results and graphs:





Description of classes, class relationships, and functions:







Requirements and Assumptions for the script to run:
-This version was written for MacOS High Sierra
-You must have the NCBI 'datasets' command-line interface downloaded and in your PATH. (instructions on how to do so)
-You must have a local collection of genomes already downloaded on your computer. The package must be unzipped and rehydrated. The folder with the genomes must only have the genomes, the data catalog and metadata must be moved to the previous folder. 
-This script was written for annotated genomes with the gff3 files. 
-This script was written for genomes with a chromosome-level assembly



Changes that must be made to the script for it to run for you:
- Open the script and adjust the paths indicated in the box at the very top. 
- any deviations from the original purpose such as different database design, different taxa, no annotations, etc. will require edits. 



The MySQL database script:




Issues:
GFF files can be very heterogenous. This code was written specifically to tackle the issues we could see with our 20 genomes and may need changing for any expansions or change of taxon. Examples of these issues include:
-differences among the .json formatting for the summary file
-different naming conventions in the gffs
-different parents among regions for the gffs


Future work:
- This code was written, to the best of my ability, with RAM and speed in mind. The program is very slow and I believe that the speed could be improved upon.
