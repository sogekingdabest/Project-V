from unittest import result
from flask import Flask, flash, render_template, request, redirect
from elasticsearch import Elasticsearch
es = Elasticsearch('http://localhost:9200')


app = Flask(__name__)
app.secret_key = 'super secret key'

@app.route('/', methods=['GET', 'POST'])
def index():

    #cargar el "feed" (hacer una query ultimas noticias)
    
    if request.method == 'POST':
        return results()
    
    return render_template('index.html', results="Pagina Principal")



@app.route('/results', methods=['GET','POST'])
def results():
    
    #search_string = request.form["search-input"]
    print(request.form)

    search_input = request.form['search-input']
    console      = request.form['input-console']
    videogame    = request.form['input-videogame']
    company      = request.form['input-company']
    date         = request.form['input-date']
    author       = request.form['input-author']


    #https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-multi-match-query.html


    #peticiones a elastic
    body_query = {
        "query" : {
            "bool": {
                "must": {
                    "multi_match" : {
                        "query": search_input,
                        "fields" : ["title", "description","articleBody"]
                    }
                },
                "filter":{
                    "consoles": console,
                    "companies": company,
                    "games": videogame,
                    "author": author,
                    "date": date
                }
            }
        }
    }

    articulos = es.search(index="articulos", query=body_query)["hits"]["hits"]

    for articulo in articulos:
        print(articulo)



    return render_template('index.html',  noticias=articulos)

if __name__ == '__main__':
    app.run()
