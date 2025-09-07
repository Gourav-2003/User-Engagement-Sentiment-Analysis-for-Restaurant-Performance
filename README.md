Restaurant Performance Analytics Using Yelp Data
Overview
In a highly competitive restaurant industry, understanding the factors that influence business success is crucial. This project analyzes a subset of Yelp data to investigate relationships between user engagement metrics (reviews, tips, check-ins) and business success metrics (review counts, average ratings) for restaurants across 8 metropolitan areas in the USA and Canada.

The goal is to quantify correlations, analyze sentiment impact, identify time trends, and provide actionable insights to help restaurant stakeholders improve performance.


project structure 

C:.
│   .gitignore
│   main.py
│   README.md
│   requirement.txt
│   structure.txt
│
├───data
│   ├───processed
│   └───raw
├───notebooks
│   │   analysis.ipynb
│   │   database_creation.ipynb
│   │   yelp.db
│   │
│   └───.ipynb_checkpoints
│           analysis-checkpoint.ipynb
│           database_creation-checkpoint.ipynb
│
├───outputs
│   └───figures
└───scripts
        analysis.py
        database_creation.py


Key Components
Data Overview
Dataset is a subset of Yelp data spanning 8 metro areas.

Data originally available as JSON files (business, review, user, tip, checkin).

Data stored in a SQLite database (yelp.db) for efficient querying.

Analyses Performed
Correlation between user engagement and restaurant success.

Impact of sentiment on review counts and ratings.

Time trends and seasonal patterns in engagement.

Differences in engagement and success across cities.

Analysis of elite vs non-elite user contributions.

Identification of busiest hours and business recommendations.

Results Summary (From Presentation Images)
Engagement vs Ratings: There is a complex relationship; higher ratings do not always guarantee higher review counts.

User Engagement Over Time: High-rated restaurants maintain steady or growing engagement even after fluctuations like COVID-19.

Differences by City: Philadelphia ranks highest for restaurant success, followed by Tampa, Indianapolis, Tucson.

Elite Users: Though fewer, elite users contribute substantially to reviews and influence business loyalty.

Peak Hours: Engagement spikes from 4 PM to 1 AM; helps optimize staffing.

Sentiment: Positive sentiment (useful, funny, cool reviews) correlates strongly with success metrics.

Recommendations: Focus on elite user collaboration, adjust operation hours to peak times, improve service quality, and target customer feedback for less successful restaurants.

How to Run

Database Creation
 python scripts/database_creation.py

Data Analysis
python scripts/analysis.py

Main Entry Point
python main.py


Saving Figures
All plots and figures generated during analysis are saved in:

outputs/figures/

Tools and Libraries
Python (pandas, matplotlib, seaborn, statsmodels)

SQLite

Jupyter Notebook for exploratory analysis

Future Work
Enrich dataset with additional metadata.

Explore more sophisticated sentiment and trend models.

Build interactive dashboards for business users.

Contact
For questions or collaboration:

GitHub: (https://github.com/Gourav-2003)

Email: gouravmuchhal476@gmail.com




