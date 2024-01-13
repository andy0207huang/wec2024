import pandas as pd
import numpy as np
import datetime
import time

from locations import convertToCountry


def getAllData(csv):
    data = pd.read_csv(csv)

    return data

def editData(data: pd.DataFrame, col: str, value: str, name: str, date: str) -> pd.DataFrame:
    data.loc[(data['Name'] == name) & (data['date'] == date), col] = value

def addCountry(data: pd.DataFrame, col: str):

    data[col] = "Na"

    for i in range(len(data.index)):

        lat = data.iloc[i]['lat']
        long = data.iloc[i]['long']

        country = convertToCountry(lat, long)
        data.loc[i, [col]] = country

    data.to_csv('./test/MOCK_DATA.csv')

if __name__ == "__main__":
    csv = open('./test/MOCK_DATA.csv', 'r')

    data = getAllData(csv)

    print(data)

    # addCountry(data, "Country")
    # print(data)

    date = "1/7/2023"
    editData(data, "Country", "Seria", "Pannier", date)

    print(data)


    