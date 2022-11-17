import json
import re
from elasticsearch import Elasticsearch
es = Elasticsearch('http://localhost:9200')

def find_word_in_text(text, word):
    return re.compile(r'\b({0})\b'.format(word), flags=re.IGNORECASE).search(text)


def get_article_categories(articleBody, category_dict):
    categories = []
    for category, words in category_dict.items():
        for word in words:
            if find_word_in_text(articleBody, word):
                categories.append(category)
                break
    return categories

def upload_data(indexName, fileName):
    with open(fileName) as input:
        articles = json.load(input)
        es.options(ignore_status=[400,404]).indices.delete(index=indexName)
        for article in articles:
            print('---------------------------------------------------------------')
            print(article)
            es.index(index=indexName, ignore=400, document=article)


if __name__ == "__main__":
    articles_file = open('articles.json')
    articles_data = json.load(articles_file)

    categories_file = open('categories.json')
    categories_data = json.load(categories_file)


    for article in articles_data:
        #print(article['description'])
        articleBody = article['articleBody']

        for category_name, category_elements in categories_data.items():
            elements_found = get_article_categories(articleBody, category_elements)
            article[category_name] = elements_found

    #es.index(index='articulosprueba', ignore=400, body=articles_data)



    with open('articles_post.json', 'w') as output:
        json.dump(articles_data, output)

    upload_data('articulosprueba', 'articles_post.json')
    
