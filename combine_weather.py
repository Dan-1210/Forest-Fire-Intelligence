
import pandas as pd

variables = {
    "temperature": "T2M",
    "humidity": "RH2M",
    "rainfall": "PRECTOTCORR",
    "wind": "WS10M"
}

data = {}

for name, column in variables.items():
    files = [f"{name}_{year}.csv" for year in range(2023, 2026)]
    df = pd.concat([
        pd.read_csv(f, skiprows=9) for f in files
    ], ignore_index=True)

    keys = ["LAT", "LON", "YEAR", "MO", "DY"]
    data[name] = df[keys + [column]]

weather = data["temperature"]

for name in ["humidity", "rainfall", "wind"]:
    weather = weather.merge(data[name], on=keys)

weather["DATE"] = pd.to_datetime(
    weather[["YEAR", "MO", "DY"]].rename(
        columns={"YEAR": "year", "MO": "month", "DY": "day"}
    )
)

weather = weather.drop(columns=["YEAR", "MO", "DY"])
weather.to_csv("tamil_nadu_weather.csv", index=False)

print(weather.head())
print("Shape:", weather.shape)
print("Saved tamil_nadu_weather.csv")
