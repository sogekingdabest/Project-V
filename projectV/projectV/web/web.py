from unittest import result
from flask import Flask, flash, render_template, request, redirect
from elasticsearch import Elasticsearch
es = Elasticsearch('http://localhost:9200')

DEFAULT_SIZE = 25

app = Flask(__name__)
app.secret_key = 'super secret key'

@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        return results()

    return render_template('index.html', results="Pagina Principal")



@app.route('/results', methods=['GET','POST'])
def results():

    search_input = request.form['search-input']
    console      = request.form['input-console']
    videogame    = request.form['input-videogame']
    company      = request.form['input-company']
    date_ini     = request.form['input-date-ini']
    date_end     = request.form['input-date-end']
    author       = request.form['input-author']

    size = DEFAULT_SIZE
    
    filters = []
    if console != "ANY":
        filters.append({"term" : {"consoles": console}})
    if videogame != "ANY":
        filters.append({"term" : {"games": videogame}})
    if company != "ANY":
        filters.append({"term" : {"companies": company}})
    if author != "":
        filters.append({"term" : {"author": author}})
    if date_ini != "":
        filters.append({"range" : {"date": {"gte": date_ini}}})
    if date_end != "":
        filters.append({"range" : {"date": {"lte": date_end}}})

    #peticiones a elastic
    body_query = {
        "size" : size,
        "query" : {
            "bool": {
                "must": {
                    "multi_match" : {
                        "query": search_input,
                        "fields" : ["title", "description","articleBody"]
                    }
                },
                "filter": filters                
            }
        }
    }

    articulos = es.search(index="articulos", body=body_query)["hits"]["hits"]
    print(len(articulos))


    return render_template('index.html',  noticias=articulos)

if __name__ == '__main__':
    app.run()
