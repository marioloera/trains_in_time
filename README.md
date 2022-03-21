# Trains Assignment: solving notes

# Instructions and Requirements
Data Engineer Exercise Assignment.pdf

## About Railway traffic
[main](https://www.digitraffic.fi/rautatieliikenne/)

[documentation](https://www.digitraffic.fi/ohjeita/#pakkaus)

[schema](https://rata.digitraffic.fi/api/v2/graphql/schema.svg)

[test](https://rata.digitraffic.fi/api/v2/graphql/graphiql)

## Fetch Railway traffic data
A script to fetch new data making a request to the Railway traffic API using the query:
queries/trainsByDepartureDate.txt

```
python src/fetch_digitraffic_data.py \
    --end_date=2022-03-18 \
    --days_to_fetch=10 \
    --datafile_path=digitraffic_data/trainsByDepartureDates/results
```

## Railway traffic fetched data
fetched data is stored as json files per day in dir.:
digitraffic_data/trainsByDepartureDates/

## Estimate Arrival time using fetched Data
A script that process the json files with Railway data
and estimates the arrival time at target date.

It also suggests an alternative earlier train for target date.

```
python src/estimate_arrival_time_from_digitraffic_data.py \
    --target_date=2022-03-23 \
    --end_date=2022-03-18 \
    --max_days_to_fetch=30 \
    --datafile_path=digitraffic_data/trainsByDepartureDates/
```
output example
```
INFO:root:avg_delay_min: 9.258064516129032
INFO:root:Train no 45 HKI: 2022-02-26 11:03:00+02:00 -> TPE: 2022-02-26 12:53:00+02:00.
Estimated Arrival Time: 2022-03-23 13:02:15.483871+02:00
INFO:root:fetch_all_trains_per_date(2022-03-23)
INFO:root:Earlier train: Train no 143 HKI: 2022-03-23 10:24:00+02:00 -> TPE: 2022-03-23 11:58:00+02:00
```

## Estimate Arrival time using sample data
A python model using pandas dataframe estimates the Arrival time
it uses the average delay of the last 30 days
it takes the input data:

sample_data/train-45-data-2017-01-01_to_2017-07-12.csv

to run:
```
python src/pandas_model.py
```
it also produces:
DifferenceInMinutes.pdf plot

## if more time:
    - build pipeline in beam,
    - stream data from topic, the beam pipeline can be reused
