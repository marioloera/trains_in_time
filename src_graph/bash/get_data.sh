URL=https://rata.digitraffic.fi/api/v2/graphql/graphql
OUTPUT_FILE=src_graph/bash/sample_data_01.json
curl $URL --compressed -H 'content-type: application/json' --data-binary '{"query":"{\n  currentlyRunningTrains(where: {operator: {shortCode: {equals: \"vr\"}}}) {\n    trainNumber\n    departureDate\n    trainLocations(where: {speed: {greaterThan: 30}}, orderBy: {timestamp: DESCENDING}, take: 1) {\n      speed\n      timestamp\n    }\n  }\n}","variables":null,"operationName":null}' > $OUTPUT_FILE

# try the command below but din not work
QUERY=`cat src_graph/query.txt`
echo $QUERY
OUTPUT_FILE=src_graph/bash/sample_data_02.json
curl $URL --compressed -H 'content-type: application/json' --data-binary '{"query":"$(QUERY)","variables":null,"operationName":null}' > $OUTPUT_FILE
