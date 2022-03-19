# Trains Assignment: solving notes

# Instructions and Requirements
Data Engineer Excercise Assignment.pdf

## About Railway traffic
[main](https://www.digitraffic.fi/rautatieliikenne/)

[documentation](https://www.digitraffic.fi/ohjeita/#pakkaus)

[schema](https://rata.digitraffic.fi/api/v2/graphql/schema.svg)

[test](https://rata.digitraffic.fi/api/v2/graphql/graphiql)


## Fetch Railway trafic data
A script to fetch new data making a request to the Railway trafic API using the query:
queries/trainsByDepartureDate.txt

```
python src/fetch_digitraffic_data.py \
    --end_date=2022-03-18 \
    --days_to_fetch=10 \
    --datafile_path=digitraffic_data/trainsByDepartureDates/results
```

## Railway trafic fetched data
fetched data is stored as json files per day in dir:
digitraffic_data/trainsByDepartureDates/

## Estimate Arrival time using fetched Data
A script that process the json files wiht Railway data
and estimates the arrival time

```
python src/process_digitraffic_data.py \
    --end_date=2022-03-18 \
    --max_days_to_fetch=10 \
    --datafile_path=digitraffic_data/trainsByDepartureDates/
```

## Estimate Arrival time using sample data
A python model using pandas dataframe estimates the Arrival time
it use the average delay of the last 30 days
it take the input data:

sample_data/train-45-data-2017-01-01_to_2017-07-12.csv

to run:
```
python src/pandas_model.py
```
it also produce:
DifferenceInMinutes.pdf plot


## if more time:
    - build pipeline in beam,
    - stream data from topic, the beam pipeline can be reused
