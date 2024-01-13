import datetime
import pandas as pd
import numpy as np

from locations import convertToCountry


def getAllData(csv):
    data = pd.read_csv(csv)

    return data

def editData(path: str, data: pd.DataFrame, col: str, value: str, name: str, date: str) -> None:
    data.loc[(data['Name'] == name) & (data['date'] == date), col] = value

    data.to_csv(path, index=False)

def addRow(path: str, data: pd.DataFrame, row: dict) -> None:
    row['Country'] = convertToCountry(row['lat'], row['long'])

    data.loc[len(data.index)] = row

    data.to_csv(path, index=False)


def addCountry(path: str, data: pd.DataFrame, col: str) -> None:

    data[col] = "Na"

    for i in range(len(data.index)):

        lat = data.iloc[i]['lat']
        long = data.iloc[i]['long']

        country = convertToCountry(lat, long)
        data.loc[i, [col]] = country

    data.to_csv(path, index=False)

if __name__ == "__main__":
    csv = open('./test/MOCK_DATA.csv', 'r')

    data = getAllData(csv)

    print(data)

    # addCountry(data, "Country")
    # print(data)

    # date = "1/7/2023"
    # editData('./test/MOCK_DATA.csv', data, "Country", "Serbia", "Pannier", date)

    # print(data)

    row = {
        'Name': 'Test',
        'long': -81.276223,
        'lat': 43.003999,
        'date': datetime.date(2024, 1, 12),
        'intensity': 3,
        'type': 'tornado'
    }

    addRow('./test/MOCK_DATA.csv', data,row)
    print(data.tail)

    