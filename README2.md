# Exploring GC Content in Squamate Genomes: A Fujita Lab Project

In the summer of 2024, I had the privilege of contributing to the Fujita Lab at the University of Texas at Arlington. This project explored the unique variability of GC content in squamate genomes, aiming to uncover novel relationships that help maintain GC content within these reptiles.

## Purpose and Goals
The project focused on two primary objectives:

1. **Building an automated MySQL database**: We compiled all complete, annotated, and chromosome-level squamate genomes from NCBI, creating a streamlined process for updates and access.
2. **Analyzing GC content variability**: Using the database, we investigated GC content across chromosomes, between intergenic and coding regions, and among different species to identify patterns and anomalies.

### Why Study GC Content in Squamates?
GC content plays a vital role in gene expression, recombination, and evolutionary stability. Despite the natural mutation bias favoring GC-to-AT transitions, squamates like the Green Anole exhibit remarkably consistent GC content compared to other vertebrates. This suggests a unique mechanism in squamates that counteracts mutation bias, presenting a compelling subject for evolutionary research.

## Highlights of the Work

### Database Design and Automation
I developed a robust MySQL database to manage the large-scale genomic data efficiently. The system automatically updates with new genome releases from NCBI, avoiding duplicates and ensuring consistent metadata tracking. Bulk data uploads streamlined processing, enabling us to perform advanced analyses without manual intervention.

<img width="1037" alt="Screen Shot 2024-10-25 at 6 06 43 PM" src="https://github.com/user-attachments/assets/78803e06-db09-4e27-9919-763eca6dc27f">

### Analytical Process
Using Python and SQL, I designed scripts to:
- Extract, process, and upload data from genome files.
- Data is matched to its relatives with the established MySQL relationships, basic joins, and subqueries. Sub-sequences are 'cut' from the main chromosome sequence with the coordinates given in or calculated from the GFF.
- Stored procedures for various desired analyses assign variables, create temporary tables, and use loops to calculate GC content (Number of 'G' and 'C' per sequence  divided by the length of the sequence minus any 'N' content, which is 'unknown').
- Data is taken from temporary tables and queries and converted to Pandas dataframes for further analysis and visualization.

Key analyses included:
- **Variability Assessments**: We used sliding window analyses to evaluate GC content standard deviation across 100kb regions, identifying the most and least variable genomes.
- **Intergenic Sequence Studies**: Length-normalized GC content comparisons revealed distinct patterns, informing hypotheses about the interplay between sequence length and GC stability.

### Data Visualization
To communicate findings effectively, I created:
- **Boxplots**: Highlighting variability in GC content across genomes, categorized by sequence length.
![Screenshot 2024-08-07 222537](https://github.com/user-attachments/assets/51b9030a-415b-4f84-98e6-a9c44d6deaf6)

![Screenshot 2024-08-07 222120](https://github.com/user-attachments/assets/48a83182-e993-4d84-88b1-ad855436d1fe)

- **Density Plots**: Showcasing genome-wide GC distribution trends, offering insights into selection pressures and evolutionary dynamics.
![image](https://github.com/user-attachments/assets/c7b58fde-22b9-4898-b2ea-ece9d6721c8f)

Modeled after this paper: https://pubmed.ncbi.nlm.nih.gov/21795750/

## Challenges and Achievements

### Tackling Data Heterogeneity
One major hurdle was the inconsistency in GFF annotation files, which required extensive preprocessing and algorithmic adjustments. By creating reusable scripts and workflows, I ensured data integrity and adaptability for future research.

### Impact and Future Directions
This project provided the Fujita Lab with:
- A scalable, automated database system.
- Foundational insights into squamate GC content variability, sparking further research into evolutionary mechanisms.

Looking ahead, I proposed optimizing database performance, and refining error-handling mechanisms to enhance analysis accuracy.

--- 
## Reflections
Through this project, I gained invaluable experience in large-scale data management, analytical modeling, and cross-disciplinary collaboration. It reinforced my passion for using data to uncover patterns and drive impactful conclusions—skills I am eager to bring to future roles.

---

Feel free to contact me at tyler.dixon.b@gmail.com for any questions or collaboration opportunities.

--- 
#  About
## Requirements and Assumptions for the script to run
- This version was written for MacOS High Sierra
- You must have the NCBI 'datasets' command-line interface downloaded and in your PATH. Instructions for adding to your PATH are under the 'Code' folder --> 'add_cli_to_PATH.txt'.
- You must have a local collection of genomes already downloaded on your computer. The package must be unzipped and rehydrated. The folder with the genomes must only have the genomes, the data catalog and metadata(renamed as <taxon>.jsonl) must be moved to the previous folder.
- This script was written for annotated genomes with the gff3 files. 
- This script was written for genomes with a chromosome-level assembly
### Changes that must be made to the script for it to run for you
- Open the script and adjust the paths indicated in the comment boxes before each class.
- Any deviations from the original purpose (different database design, different taxa, different genomes, no annotations, etc.) will require edits.

## File Descriptions
### Code
**numos** uses the ncbi command-line interface to compare the computer's local database to the cloud. It automatically updates the local and MySQL databases with new genome releases from NCBI, avoiding duplicates and ensuring consistent metadata tracking. It then utilizes shell commands to parse and search the downloaded .gff and .fna files for desired information, uploads the information to the MySQL database. 
**dataframes** takes information from MySQL to be further analyzed and/or graphed in python.
**window_variation** determined most and least variable genomes by GC content amongst 100kb windows.

### SQL
Folder contains all of the text needed to recreate the database. 

### Data
Folder was derived from this script for quick use in future analyses. Contains all of the genomes and chromosome IDs we used. 

### Revisions
Archive for older versions of code. 
