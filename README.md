# CUSTOM PYTHON PLAGIARISM CHECKER BY NICO 

This is a python project where I challenged myself to not use AI in its production. This checker isnt the fastest or the best, however, it was a great learning experience and authored soley by me!
The plagiarism checker focuses on similarity detection using **Total Frequency Inverse Document Frequency (TF-IDF) + Cosine Similarity to give a similarity score.** It does not measure intent or authorship.
The checker is effective for both direct copy paste and paraphrasing and rewording.
The checker measures 3 similarity scores: max score, top 3 average, coverage (fraction of document paragraphs exceeding a similarity threshold)

# HOW IT WORKS

1. Your input document is split into paragraphs and sentences, then a relative amount of samples are selected from your document.
2. Using the **Requests** searches each sample and fetches the resulting articles.
3. The pages are cleaned up to be just the body text using **Beautiful Soup** , error pages and login walls are filtered out
4. Cheap Relevance Filtering: Each fetched article is scored against a sample sentence for a fast similarity check, only the top 1-2 most relevant articles per sample are kept
5. Detailed Similarity Scoring: the main document is compared against each article using: Character-n-gram TF-IDF similarity (checks for copying) and Word n-gram TF-IDF similarity(checks for paraphrase). These scores are combined for a weighted similarity score
6. Final Metrics: For each article comparison, it reports: max score , top 3 average, and coverage. Then if these scores exceed a certain threshold with any article, plagiarism classification is returned

# Output Interpretation

Scores can range from 0.0 - 1.0:

VERY LIKELY PLAGIARIZED: Highest scoring article w/ max score greater than .45 OR (any top3 avg greater than .3 AND coverage greater than .3)

POSSIBLY PLAGIARIZED: Highest scoring article w/ max score greater than .22 and less than .45 or ( any top3 avg greater than .2 and less than .3 AND coverage greater than .2 and less than .3)

UNLIKELY PLAGIARIZED: Highest scoring article w/ max score less than .22 or top avg AND coverage less than .2

# How To Use
1. Create a .txt file with your essay/text or use one of the sample texts
2. Download and run "run.py"
3. Enter the file name including .txt
4. Wait for your output!

# Example Runs

**Short Original Text**

<img width="789" height="239" alt="image" src="https://github.com/user-attachments/assets/5ba96058-fc74-4fa2-bca9-dbf602c9046a" />

**Paraphrased Essay about WaterGate**

<img width="813" height="318" alt="image" src="https://github.com/user-attachments/assets/2b875dd1-f6b2-436d-898f-9f530265f33b" />

**Exact Watergate Speech**

<img width="834" height="233" alt="image" src="https://github.com/user-attachments/assets/876f0a89-e712-4e57-8682-fffb146e4428" />





