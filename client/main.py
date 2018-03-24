
import os
import http.client
import json
import csv
import xml.etree.ElementTree as ET


MIN_LENGTH = 1000
FILENAME = "sports.xml"
CSV_FILENAME = "result.csv"
HEADERS = {'Content-type': 'application/json'}
MODEL = 'lsi'


def parse_xml():
    path = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources"), FILENAME)
    root = ET.parse(path).getroot()

    data = []
    counter = 0
    for child in root:
        text = child.attrib['Body']
        if len(text) > MIN_LENGTH:
            data.append(text)
            counter += 1

        # if counter > 10:
        #    break

    print('Count of accepted: ')
    print(counter)

    return data


def categorize(connection):
    data = parse_xml()
    ids = []
    for post in data:
        connection.request('POST', '/classify/?model={}'.format(MODEL), json.dumps({'text': post}), HEADERS)
        response = json.loads(connection.getresponse().read().decode())
        if response['status']:
            ids.append(response['payload']['id'])

    return ids


def update_category_dict(classification, categories):
    # first is accumulated prob, second counter
    for (cid, prob) in classification:
        entry = categories.setdefault(cid, [0, 0])
        if prob < 0.05:
            # skip
            continue
        entry[0] += prob
        entry[1] += 1


def process_classification(ids, connection):
    posts = {}
    categories = {}
    for i in ids:
        connection.request('GET', '/classification/?model={}&id={}'.format(MODEL, i), headers=HEADERS)
        response = json.loads(connection.getresponse().read().decode())
        if response['status']:
            posts[i] = response['payload']['entries'][0]['categories']
            update_category_dict(response['payload']['entries'][0]['categories'], categories)

    return categories, posts


def compute_graphs(categories):
    graph1 = []     # sum of articles
    graph2 = []     # sum of probs
    graph3 = []     # sum of probs divided by sum of articles
    for (cid, entry) in categories.items():
        graph1.append((cid, entry[1]))
        graph2.append((cid, entry[0]))
        graph3.append((cid, entry[0] / max(1, entry[1]) * 100))

    return [
        list(sorted(graph1, key=lambda x: x[0])),
        list(sorted(graph2, key=lambda x: x[0])),
        list(sorted(graph3, key=lambda x: x[0]))
    ]


def write_csv(data, filename):
    path = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources"), filename)
    with open(path, 'w') as csvfile:
        w = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        w.writerows(data)


def main():
    connection = http.client.HTTPConnection('localhost:5000')
    ids = categorize(connection)
    categories, posts = process_classification(ids, connection)
    r = compute_graphs(categories)
    for i, graph in enumerate(r):
        write_csv(graph, '{}-{}-{}'.format(MODEL, i, CSV_FILENAME))


if __name__ == "__main__":
    main()
