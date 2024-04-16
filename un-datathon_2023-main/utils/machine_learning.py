from statsmodels.tsa.arima.model import ARIMA
from pmdarima import auto_arima
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def arima(dataset_train, country, cols):
    # Loop through each unique country in the DataFrame
    unique_countries = dataset_train['country'].unique()
    unique_commodities = dataset_train['commodity_transaction_x'].unique()

    df_train = dataset_train[(dataset_train['year'] >= 1990) & (dataset_train['year'] <= 2017)]
    df_test = dataset_train[(dataset_train['year'] >= 2018) & (dataset_train['year'] <= 2020)]

    df_train.sort_values('year', inplace=True)
    df_test.sort_values('year', inplace=True)

    # for commodity in unique_commodities:
    country_data = df_train[(df_train['country'] == country)]
    test_country_data = df_test[(df_test['country'] == country)]

    cleaned_df = country_data.dropna(subset=[cols])
    rates = cleaned_df[cols].tolist()
    years = cleaned_df['year'].tolist()
    if len(rates) <= 1:
        pass

    # Using auto_arima to find the best PDQ parameters
    model = auto_arima(rates, stepwise=True, suppress_warnings=True, error_action="ignore")
    p, d, q = model.order

    # Fit the ARIMA model with the chosen parameters
    model_fit = model.fit(rates)

    # Forecast rates
    forecast = model_fit.predict(n_periods=3)  # Forecast next 3 steps

    model_arima = ARIMA(rates, order=(p, d, q))
    model_trend = model_arima.fit()
    predictions = model_trend.predict(start=0, end=len(rates) - 1, typ='levels')

    max_year = max(years)

    # Create DataFrames from the lists
    arima_data = {'Year': years, f'ARIMA_{cols}': predictions}
    original_data = {'Year': years, f'{cols}': rates}
    forecast_data = {'Year': [max_year + 1, max_year + 2, max_year + 3], 'Forecast': forecast}
    test_data = {'Year': test_country_data['year'].tolist(), f'Actual_{cols}': test_country_data[cols].tolist()}

    ARIMA_df = pd.DataFrame(arima_data)
    original_df = pd.DataFrame(original_data)
    forecast_df = pd.DataFrame(forecast_data)
    test_df = pd.DataFrame(test_data)

    # Plotting using Seaborn
    sns.set(style="whitegrid")

    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111)

    sns.lineplot(x='Year', y=f'ARIMA_{cols}', data=ARIMA_df, marker='o', label=f'ARIMA {cols}', ax=ax)
    sns.lineplot(x='Year', y=f'{cols}', data=original_df, marker='s', label=f'Actual {cols}', ax=ax)
    sns.lineplot(x='Year', y='Forecast', data=forecast_df, marker='o', label='Forecast', ax=ax)
    sns.lineplot(x='Year', y=f'Actual_{cols}', data=test_df, marker='s', label=f'Actual Test {cols}', ax=ax)

    ax.set_title(f'{country} {cols} Over Years \n AIC: {model_trend.aic}')
    ax.set_xlabel('Year')
    ax.set_ylabel(f'{country} {cols} ')

    plt.legend()

    return fig




