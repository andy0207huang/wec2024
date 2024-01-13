import pandas as pd
import numpy as np

from locations import convertToCountry


def getAllData(csv):
    data = pd.read_csv(csv)

    return data

def editData(path: str, data: pd.DataFrame, col: str, value: str, name: str, date: str) -> pd.DataFrame:
    data.loc[(data['Name'] == name) & (data['date'] == date), col] = value
    
    data.to_csv(path)

def addCountry(path: str, data: pd.DataFrame, col: str) -> None:

    data[col] = "Na"

    for i in range(len(data.index)):

        lat = data.iloc[i]['lat']
        long = data.iloc[i]['long']

        country = convertToCountry(lat, long)
        data.loc[i, [col]] = country

    data.to_csv(path)

if __name__ == "__main__":
    csv = open('./test/MOCK_DATA.csv', 'r')

    data = getAllData(csv)

    print(data)

    # addCountry(data, "Country")
    # print(data)

    date = "1/7/2023"
    editData('./test/MOCK_DATA.csv', data, "Country", "Serbia", "Pannier", date)

    print(data)


    