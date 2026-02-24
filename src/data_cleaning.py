import pandas as pd

krk_dist = ['Stare Miasto', 'Grzegórzki', 'Prądnik Czerwony', 'Prądnik Biały', 'Krowodrza', 'Bronowice', 'Zwierzyniec', 'Dębniki', 'Łagiewniki-Borek Fałęcki', 'Swoszowice', 'Podgórze Duchackie',
            'Bieżanów-Prokocim', 'Podgórze', 'Czyżyny', 'Mistrzejowice', 'Bieńczyce', 'Wzgórza Krzesławickie', 'Nowa Huta']


# Get the district and street name 
def clean_data(path): 
    """
    Load raw dataset and perform full cleaning pipeline.

    """
    
    # Load raw dataset
    df = pd.read_csv(path)
    
    #Calculating price per sqm
    df["PricePerM2"] = (df["Price"]/df["Living area"]).round(2)

    # Dropping values where is missing 5% or less 
    threshold = len(df) * 0.05
    cols_to_drop = df.columns[df.isna().sum() <= threshold]
    df.dropna(subset=cols_to_drop, inplace=True)
    
    # Get the district and street name 
    def get_district(address):
        """
        Extract Kraków district from structured address string
        """
        whole_address = [i.strip() for i in address.split(',')]

        for item in whole_address:
            if item in krk_dist:
                return item
        return None

    def get_under_district(address):
        """
        Extract neighborhood, based on address position.
        """
        whole_address = [i.strip() for i in address.split(',')]
        return whole_address[-4] if len(whole_address) >= 4 else None


    def get_street(address):
        """
        Extract street name (ul., al., os.).
        """
        street = [i.strip() for i in address.split(',')][0]
        street_name = [i.strip() for i in street.split('.')]
        if street_name[0] == 'ul' or street_name[0] == 'al' or street_name[0] =='os':
            if len(street_name)> 2:
                return '. '.join(street_name[1:]).strip()
            return street_name[1]
        return None


    df['District'] = df['Address'].apply(get_district)
    df['Neighborhood'] = df['Address'].apply(get_under_district)
    df['Street'] = df['Address'].apply(get_street)

    # Drop rows that are not in Krakow
    df = df.dropna(subset=['District'])
    
    # Drop values that are in last floor and the actual floor is not known 
    poddasze = df['Floor']== 'poddasze'
    df = df[~poddasze]

    # Replace values so it can be changed to int values later on
    df['Floor'] = df['Floor'].str.split(' ').str[0].str.strip()
    df['Floor'].replace('10+', '11', inplace=True)
    df['Floor'].replace('parter', '0', inplace=True)
    df['Floor'].replace( 'suterena', '-1', inplace=True)
    df['Floor'] = df['Floor'].astype(int)
    
    # Replace values of Rooms to numeric 
    df['Rooms'] = df['Rooms'].str.split(' ').str[0].str.strip()
    df['Rooms'].replace('10+', '11', inplace=True)
    df['Rooms'] = df['Rooms'].astype(int)
    
    # Get balcony as boolean value
    df['Balcony'] = df['Title'].str.lower().str.contains('balkon|taras|loggia')
    
    def get_floor_category(floor):
        """
        Categorize apartment floor into groups
        """
        if floor == 0:
            cat = 'Ground'
        elif floor >= 1 and floor <= 2:
            cat = 'Low'
        elif floor >= 3 and floor <= 5:
            cat = 'Medium'
        else:
            cat = 'High'
        return cat


    df['FloorCategory'] = df['Floor'].apply(get_floor_category)
    
    
    def get_size_category(size_m):
        """
        Categorize apartment size into bins
        """
        if size_m <=35:
            cat = 'Small'
        elif size_m >= 35 and size_m <= 60:
            cat = 'Medium'
        elif size_m >= 60 and size_m <= 90:
            cat = 'Large'
        else:
            cat = 'XL'
        return cat

    df['ApartmentSizeCategory'] = df['Living area'].apply(get_size_category)
    
    df.rename(columns={'Living area': 'LivingArea'}, inplace=True)
    
    return df

