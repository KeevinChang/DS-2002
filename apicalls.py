import sys
import pandas as pd
import requests
import json
import os


def main():
    file_exists = True
    try:
        f = open("country.json", "r")
        country_json = json.load(f)
        countrydf = pd.DataFrame(country_json)
        f.close()
    except FileNotFoundError:
        file_exists = False
    country = input("Enter the name of the country: ")
    try:
        info = requests.get(f"https://restcountries.com/v3.1/name/{country}")
        info.raise_for_status()
        df = pd.DataFrame(info.json())
        print(df[["capital", "population"]])
        if file_exists:
            this_country = countrydf[countrydf["name"] == country]
            if this_country.empty:
                countrydf.loc[len(countrydf.index)] = [country, df["capital"].iloc[0], df["population"][0]]
        else:
            countrydf = pd.DataFrame([[country, df["capital"].iloc[0], df["population"].iloc[0]]], columns=['name', 'capital', 'population'])
        with open("country.json", "w") as f:
            f.write(countrydf.to_json(orient='records'))
            f.close()
    except requests.exceptions.HTTPError:
        print("Country not found", file=sys.stderr)
    except requests.exceptions.RequestException:
        print("API call failed", file=sys.stderr)


if __name__ == "__main__":
    main()
