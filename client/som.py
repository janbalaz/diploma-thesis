import os
import json
import http.client
import numpy as np
import sompy
import mediawiki

HEADERS = {'Content-type': 'application/json'}
MIN_LEN = 1000
MODEL = 'lda'


def get_wiki_articles(count=0, target=0, load_from_file=False):
    pages_filename = 'pages'

    if load_from_file:
        return read_json(pages_filename)
    else:
        wikipedia = mediawiki.MediaWiki()
        pages = []
        counter = 0
        for page_name in wikipedia.random(pages=count):
            try:
                if len(pages) >= target:
                    break

                page = wikipedia.page(page_name)
                if len(page.content) > MIN_LEN:
                    pages.append({counter: {
                        'title': page.title,
                        'content': page.content
                    }})
                    counter += 1
            except (mediawiki.exceptions.DisambiguationError, mediawiki.exceptions.PageError):
                continue
            except Exception:
                continue

        write_json(pages, pages_filename)

        print(len(pages))
        return pages


def get_categorization(wiki_articles=None, load_from_file=False):
    categorization_filename = 'pages-categorization'

    if load_from_file:
        return read_json(categorization_filename)
    else:
        connection = http.client.HTTPConnection('localhost:5000')
        categorization = []
        for i, article in enumerate(wiki_articles):
            post_id = categorize(connection, article[str(i)]['content'])
            result = zero_fill(get_categorized(connection, post_id))
            categorization.append({i: {
                'post_id': post_id,
                'result': result
            }})

        write_json(categorization, categorization_filename)

        return categorization


def get_som_data(categorization):
    som_data = []
    for i, record in enumerate(categorization):
        som_data.append(list(map(lambda x: x[1], record[str(i)]['result'])))

    mapsize = [20, 20]
    som = sompy.SOMFactory.build(np.array(som_data), mapsize, mask=None, mapshape='planar', lattice='rect',
                                 normalization='var', initialization='pca', neighborhood='gaussian', training='batch',
                                 name='sompy')
    som.train(n_job=1, verbose='debug')
    som.cluster(n_clusters=100)
    #print("old labels (if any): ", som.cluster_labels)
    #labels = som.build_data_labels()
    #som.cluster_labels = labels
    #print("new labels: ", som.cluster_labels)
    som.data_labels = np.array([str(i*1000) for i in range(len(categorization))])

    # h = sompy.hitmap.HitMapView(10, 10, 'hitmap')
    #h.show(som)
    umat = sompy.umatrix.UMatrixView(40, 40, "rand data")
    umat.show(som, labels=True)
    #v = sompy.mapview.View2D(50, 50, 'test', text_size=8)
    ##cl = som.cluster(n_clusters=100)
    #v.show(som, what='cluster', col_sz=6)
    # v.show(som, what='codebook', which_dim='all', cmap='jet', col_sz=6)

    # v = sompy.mapview.View2DPacked(2, 2, 'test', text_size=8)
    # first you can do clustering. Currently only K-means on top of the trained som
    # cl = som.cluster(n_clusters=100)
    #v.show(som, what='cluster')


def zero_fill(topics):
    existing = list(map(lambda x: x[0], topics))
    for i in range(100):
        if i in existing:
            continue
        topics.append([i, 0.0])

    return sorted(topics, key=lambda x: x[0])


def write_json(data, filename):
    path = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources"), filename)
    with open(path, 'w') as outfile:
        json.dump(data, outfile)


def read_json(filename):
    path = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources"), filename)
    with open(path) as data_file:
        data = json.load(data_file)

    return data


def categorize(connection, post):
    connection.request('POST', '/classify/?model={}'.format(MODEL), json.dumps({'text': post}), HEADERS)
    response = json.loads(connection.getresponse().read().decode())
    if response['status']:
        return response['payload']['id']

    return None


def get_categorized(connection, post_id):
    connection.request('GET', '/classification/?model={}&id={}'.format(MODEL, post_id), headers=HEADERS)
    response = json.loads(connection.getresponse().read().decode())
    if response['status']:
        return response['payload']['entries'][0]['categories']

    return []


def main():
    # wiki_articles = get_wiki_articles(count=500000, target=1100)
    wiki_articles = get_wiki_articles(load_from_file=True)
    # categorized = get_categorization(wiki_articles)
    categorized = get_categorization(load_from_file=True)
    get_som_data(categorized)
    # print(len(categorized))


if __name__ == "__main__":
    main()
