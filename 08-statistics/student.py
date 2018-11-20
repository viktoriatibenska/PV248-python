import sys
import pandas
import json
import numpy as np
from datetime import datetime, timedelta

def calculateRes(df):
    res = {}

    dfExercises = df.rename(index = lambda x: x[-2:])
    dfExercises = dfExercises.groupby(axis=0, level=0).sum()
    res["mean"] = dfExercises.mean()
    res["median"] = dfExercises.median()
    res["total"] = dfExercises.sum()
    res["passed"] = int(dfExercises.astype(bool).sum())

    # regression
    startDate = datetime.strptime('2018-09-17', "%Y-%m-%d").date()
    dfDates = df.rename(index = lambda x: x[:10])
    dfDates = dfDates.groupby(axis=0, level=0).sum()
    dfDates = dfDates.sort_index().cumsum()
    y = dfDates.values
    x = np.array([(datetime.strptime(date, "%Y-%m-%d").date() - startDate).days for date in dfDates.index])
    x = x[:, np.newaxis]
    regress = np.linalg.lstsq(x, y, rcond=None)[0]
    res["regression slope"] = regress[0]
    if regress[0] != 0.0:
        res["date 16"] = str(startDate + timedelta(16 / regress[0]))
        res["date 20"] = str(startDate + timedelta(20 / regress[0]))
    else:
        res["date 16"] = "inf"
        res["date 20"] = "inf"

    return res

def main(dataFile, mode):
    df = pandas.read_csv(dataFile, index_col='student')

    if mode == "average":
        df = df.mean(axis=0)
        print(json.dumps(calculateRes(df), ensure_ascii=False, indent=4))
    elif mode.isdigit():
        try:
            df = df.loc[int(mode)]
            print(json.dumps(calculateRes(df), ensure_ascii=False, indent=4))
        except KeyError:
            print("No student with ID:", mode)
    else:
        print("Unknown mode!")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
