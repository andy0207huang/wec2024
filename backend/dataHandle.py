import pandas as pd

def getAllData(csv):
    data = pd.read_csv(csv)

    return data



if __name__ == "__main__":
    csv = open('./test/MOCK_DATA.csv', 'r')

    data = getAllData(csv)

    print(data)