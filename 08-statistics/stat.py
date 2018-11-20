import sys
import pandas
import json

def calcResult(df):
    res = {}
    for col in df:
        item = {}
        item["mean"] = df[col].mean()
        item["median"] = df[col].median()
        item["first"] = df[col].quantile(0.25)
        item["last"] = df[col].quantile(0.75)
        item["passed"] = int(df[col].astype(bool).sum())
        res[df[col].name] = item
    return res

def main(dataFile, mode):
    df = pandas.read_csv(dataFile, index_col='student')
    res = {}

    if mode == "dates":
        dfDates = df.rename(columns = lambda x: x[:10])
        dfDates = dfDates.groupby(axis=1, level=0).sum()
        res = calcResult(dfDates)
    elif mode == "deadlines":
        res = calcResult(df)
    elif mode == "exercises":
        dfExercises = df.rename(columns = lambda x: x[-2:])
        dfExercises = dfExercises.groupby(axis=1, level=0).sum()
        res = calcResult(dfExercises)
    else:
        print("Unknown mode!")

    print(json.dumps(res, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
