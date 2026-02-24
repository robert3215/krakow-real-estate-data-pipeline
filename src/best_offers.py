import pandas as pd
import numpy as np
from src.data_cleaning import clean_data


def get_best_offers(path,top_n=20, max_size=100):
    #load 
    df = clean_data(path)
    # Exclude very large apartments
    df = df[df['LivingArea'] <= max_size]
    
    # Remove problematic listings
    exclude_keywords = 'strych|do adaptacji|udział|partycypacja|tbs|poddasze|poddaszu'

    df = df[~df['Title'].str.lower().str.contains(exclude_keywords)]
    
    # District-relative pricing benchmark
    district_median = df.groupby('District')['PricePerM2'].median()
    df['DistrictMean'] = df['District'].map(district_median)

    # Relative pricing vs local market
    df['PriceRatio'] = df['PricePerM2'] / df['DistrictMean']

    # Lower ratio = better opportunity
    df['PriceScore'] = 1 / df['PriceRatio']

    # Implement size scoring 
    df['SizeScore'] = 1.0

    df.loc[df['LivingArea'].between(40, 65), 'SizeScore'] = 1.1
    df.loc[df['LivingArea'] < 30, 'SizeScore'] = 0.8
    df.loc[df['LivingArea'] > 90, 'SizeScore'] = 0.9
    # Floor scoring 
    floor_score_map = {
        'Ground': 0.80,
        'Low': 1.00,
        'Medium': 1.1,
        'High': 0.95}

    df['FloorScore'] = df['FloorCategory'].map(floor_score_map)
    
    # Final Investment Score
    # Price dominates (70%), size and floor adjust liquidity
    df['InvestmentScore'] = (
        df['PriceScore'] * 0.70 +
        df['SizeScore'] * 0.15 +
        df['FloorScore'] * 0.15
    )

    best_offers = df.sort_values('InvestmentScore', ascending=False).head(top_n)
    
    return best_offers
