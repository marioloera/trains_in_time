import pandas as pd

data_file = "sample_data/train-45-data-2017-01-01_to_2017-07-12.csv"
df = pd.read_csv(data_file)

# filter row
df = df[
    (df["trainNumber"] == 45)
    & (df["trainType"] == "S")
    & (df["timeTableRowCommercialStop"] == (True))
    & (df["timeTableRowTrainStopping"] == (True))
    & (df["timeTableRowStationShortCode"] == "TPE")
    & (df["timeTableRowType"] == "ARRIVAL")
    & (df["timetableType"] == "REGULAR")
]

# filter the last x days,
# one week, one month, one year?
# could check for weekdays: Tuesday, Wednesday, Thursday only
days = 30
df = df[-days:-1]

# filter columns
print("filtered")
# filter columns
df = df[
    [
        "timeTableRowScheduledTime",
        "departureDate",
        "timeTableRowDifferenceInMinutes",
    ]
]

df["TempereScheduledTime"] = pd.to_datetime(df["timeTableRowScheduledTime"], infer_datetime_format=True)
# assuming Tampere is two hours ahead UTC
df["TempereScheduledTime"] += pd.to_timedelta(2, unit="h")

print(df[["TempereScheduledTime", "timeTableRowDifferenceInMinutes"]])

# filter columns
mean = df["timeTableRowDifferenceInMinutes"].mean()
print("mean", mean)

std = df["timeTableRowDifferenceInMinutes"].std()
print("std", std)


# plot
lines = df[
    [
        "departureDate",
        "timeTableRowDifferenceInMinutes",
    ]
].plot.line()
# plt.show()
lines.figure.savefig("DifferenceInMinutes.pdf")

# estimated arrival time
estimated_arriva_time = df.iloc[0]["TempereScheduledTime"] + pd.to_timedelta(mean, unit="m")
result = f'Tempere Estimated Arrival Time: {estimated_arriva_time.strftime("%H:%M:%S")}'
print(result)
