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
- Extract and process data from genome files.
- Calculate GC content for various genomic regions using efficient algorithms.
- Organize results into query-ready formats for visualization and reporting.

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

## Reflections
Through this project, I gained invaluable experience in large-scale data management, analytical modeling, and cross-disciplinary collaboration. It reinforced my passion for using data to uncover patterns and drive impactful conclusions—skills I am eager to bring to future roles.

---

Feel free to contact me at tyler.dixon.b@gmail.com for any questions or collaboration opportunities.

