import requests


def get_query(date=None):
    with open("src_graph/query.txt", mode="r") as f:
        query = f.read()
        if date is None:
            return query
        return query.replace("2022-03-16", date)


date = "2022-03-17"
query = get_query(date)

url = "https://rata.digitraffic.fi/api/v2/graphql/graphql"
headers = {"Content-Type": "application", "jsonandAccept-Encoding": "gzip"}


# could not figurore out the request
r = requests.post(url, data=query, headers=headers)
print(r.text)

x = requests.get(url, data=query, headers=headers)
print(r.text)
