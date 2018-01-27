
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
            # counter += 1

        # if counter > 10:
        #    break

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
        entry[0] += prob
        entry[1] += 1


def process_classification(ids, connection):
    categories = {}
    for i in ids:
        connection.request('GET', '/classification/?model={}&id={}'.format(MODEL, i), headers=HEADERS)
        response = json.loads(connection.getresponse().read().decode())
        if response['status']:
            update_category_dict(response['payload']['entries'][0]['categories'], categories)

    return categories


def compute_graph(categories):
    result = []
    for (cid, entry) in categories.items():
        result.append((cid, entry[0] / entry[1] * 100))

    return list(sorted(result, key=lambda x: x[1], reverse=True))


def write_csv(data):
    path = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources"), CSV_FILENAME)
    with open(path, 'w') as csvfile:
        w = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        w.writerows(data)


def main():
    connection = http.client.HTTPConnection('localhost:5000')
    ids = categorize(connection)
    categories = process_classification(ids, connection)
    r = compute_graph(categories)
    write_csv(r)


if __name__ == "__main__":
    main()
