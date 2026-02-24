
from src.scraper import run_scraper
from src.data_cleaning import clean_data
from src.data_enrichment import add_coordinates
from src.best_offers import get_best_offers


raw_data_path = "data/raw/apartments_raw.csv"
coords_path= "data/neighborhood_coordinates.csv"

def main(run_scraping=False):

    if run_scraping:
        print("Running scraper...")
        df_raw = run_scraper()
        df_raw.to_csv(raw_data_path, index=False)

    print("Cleaning...")
    df_clean = clean_data(raw_data_path)

    print("Adding coordinates...")
    df_enriched = add_coordinates(df_clean, coords_path)
    df_enriched.to_excel("data/apartments_cleaned.xlsx", index=False)

    print("Generating ranking...")
    # get_best_offers arguments:
    # top_n (default=20)
    # max_size (default=100 m²)
    best = get_best_offers(raw_data_path)
    best.to_excel("data/best_20.xlsx", index=False)

    print("Done")


if __name__ == "__main__":
    main(run_scraping=False)