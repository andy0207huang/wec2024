import datetime
import pandas as pd

from .locations import convertToCountry


def getAllData(csv):
    data = pd.read_csv(csv)

    return data

def editData(path: str, data: pd.DataFrame, value: str, name: str, date: str) -> None:
    data.loc[(data['Name'] == name) & (data['date'] == date)] = value

    data.to_csv(path, index=False)

def addRow(path: str, data: pd.DataFrame, row: dict) -> None:
    # Gets the country from lat and long
    row['Country'] = convertToCountry(row['lat'], row['long'])
    
    # Converts the date to month/day/year
    row['date'] = pd.to_datetime(row['date']).strftime("%#m/%#d/%Y")

    # Adds the row
    data.loc[len(data.index)] = row

    # Save CSV
    data.to_csv(path, index=False)



def addCountry(path: str, data: pd.DataFrame, col: str) -> None:

    # Creates a new column called country and populate it with Na
    data[col] = "Na"

    # Loop through all the rows
    for i in range(len(data.index)):

        # Get latitude and longitude
        lat = data.iloc[i]['lat']
        long = data.iloc[i]['long']

        # Gets the country
        country = convertToCountry(lat, long)

        # Updates the Country column of the row
        data.loc[i, [col]] = country

    # Save csv
    data.to_csv(path, index=False)

if __name__ == "__main__":
    csv = open('./test/MOCK_DATA.csv', 'r')

    data = getAllData(csv)

    print(data)

    # addCountry(data, "Country")
    # print(data)

    row = {
        'Name': 'Test',
        'long': -81.276223,
        'lat': 43.003999,
        'date': "1/2/24",
        'intensity': 3,
        'type': 'tornado'
    }

    addRow('./test/MOCK_DATA.csv', data, row)
    print(data.tail)

    # row = {
    #     'Name': 'Test',
    #     'long': -81.276223,
    #     'lat': 43.003999,
    #     'date': "1/12/24",
    #     'intensity': 3,
    #     'type': 'tornado',
    #     'Country': "Canda"
    # }

    # date = "1/2/2024"
    # editData('./test/MOCK_DATA.csv', data, row, "Test", date)

    # print(data)

    



    