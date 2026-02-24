Kraków Real Estate Market Analysis
End-to-end data pipeline project combining web scraping, analytics, and BI reporting.

The pipeline covers:
- Web scraping
- Data cleaning
- Feature engineering
- Geospatial enrichment
- Investment scoring
- Interactive dashboard reporting in Power BI

The goal was to build a fully automated data pipeline and produce actionable market insights.
__________________________________________________________________________________________________________________________________________________

The project answers:

- Which districts are priced above / below city median?
- What is the distribution of price per m²?
- Where are premium listings concentrated?
- Which offers represent the best relative investment opportunities?
__________________________________________________________________________________________________________________________________________________

Dashboard Preview:

![Krakow Real Estate Dashboard](reports/reports/Dashboard_screenshot.png)

Full interactive Power BI model available in:
- `reports/Apartments_krakow_overview.pbix`
- `reports/Dadshboard_report.pdf`

Dashboard Overview
- Total Listings KPI
- Median Apartment Size
- District Median Price per m²
- District Premium vs City Median
- Price Distribution Histogram
- Geospatial price clustering map
________________________________________________________________________________________________________________________________________________

The program generates an investment ranking exported to Excel

Offers are ranked using a composite InvestmentScore:
- 70% – Relative price vs district median
- 15% – Size liquidity adjustment
- 15% – Floor category attractiveness

Price dominance ensures undervalued properties rank highest
__________________________________________________________________________________________________________________________________________________

After running the pipeline, the program automatically produces:

- data/apartments_cleaned.xlsx
- data/best_20.xlsx
__________________________________________________________________________________________________________________________________________________
Tech Stack:
- Python
- Selenium – web scraping
- Pandas – data transformation & feature engineering
- Seaborn & Matplotlib – exploratory data analysis
- LocationIQ API – geocoding neighborhoods
- Power BI – dashboard & visualization
- Excel – final reporting layer
__________________________________________________________________________________________________________________________________________________

Data Pipeline Architecture:
Scraper → Raw CSV → Cleaning → Feature Engineering → Geocoding → Investment Scoring → Power BI Dashboard 

__________________________________________________________________________________________________________________________________________________

How to Run the Project

Install dependencies:
pip install -r requirements.txt

Run full pipeline:
python main.py

To include fresh scraping, inside main.py set:
main(run_scraping=True)
__________________________________________________________________________________________________________________________________________________

NOTE: Data scraped for educational and analytical purposes only