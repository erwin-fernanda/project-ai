import pandas as pd
import pycountry as pc


def merge_data(df1, df2):
    data_geom = []
    data_loc = []

    for country in df1['country']:
        data_geom.append(df2[df2['country'] == country]['geometry'])
        data_loc.append(pc.countries.search_fuzzy(country)[0].alpha_3)

    df1['geometry'] = data_geom
    df1['iso_alpha'] = data_loc

    return df1


def transform_data(df1, df2):
    df1_final = df1.reset_index(drop=True)
    country = []
    year = []
    geometry = []
    loc = []

    for i, index in enumerate(df1.index.values):
        country.append(index[0])
        year.append(index[1])
        geometry.append(df2[df2['country'] == index[0]]['geometry'].values[0])
        loc.append(df2[df2['country'] == index[0]]['iso_alpha'].values[0])

    df1_final['country'] = country
    df1_final['year'] = year
    df1_final['geometry'] = geometry
    df1_final['iso_alpha'] = loc

    return df1_final


def transpose_data(df):
    df_new = pd.DataFrame()

    col_target = ['oil_consumption', 'renewable_production', 'CO2_emission']
    country = []
    year = []
    value = []
    kind = []

    for i, index in enumerate(df.index.values):
        for col in col_target:
            country.append(index[0])
            year.append(index[1])
            value.append(df[col].iloc[i])
            kind.append(col)

    df_new['country'] = country
    df_new['year'] = year
    df_new['commodity'] = kind
    df_new['value'] = value

    df_new.sort_values(by=['year', 'commodity'], inplace=True)

    return df_new