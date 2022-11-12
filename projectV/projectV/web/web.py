from unittest import result
from flask import Flask, flash, render_template, request, redirect, url_for
from elasticsearch import Elasticsearch
es = Elasticsearch('http://localhost:9200')

DEFAULT_SIZE = 10

app = Flask(__name__)
app.secret_key = 'super secret key'

@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        return results()

    return render_template('index.html', results="Pagina Principal")



@app.route('/results', methods=['GET','POST'])
def results():

    # if request.method == 'POST':
    #     search_input = request.form['search-input']
    #     console      = request.form['input-console']
    #     videogame    = request.form['input-videogame']
    #     company      = request.form['input-company']
    #     date_ini     = request.form['input-date-ini']
    #     date_end     = request.form['input-date-end']
    #     author       = request.form['input-author']
    # else:
    search_input = request.args.get('search_input')
    console      = request.args.get('console')
    videogame    = request.args.get('videogame')
    company      = request.args.get('company')
    date_ini     = request.args.get('date_ini')
    date_end     = request.args.get('date-end')
    author       = request.args.get('author')


    page = request.args.get('page', 1, type=int)
    size = DEFAULT_SIZE
    _from = (page-1)*size
    
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
        "from": _from,
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
        
    articulos = es.search(index="articulos", body=body_query)["hits"]

    next_url = ""
    prev_url = ""
    total_noticias = articulos["total"]["value"]
    if (_from + size < total_noticias):
        next_url = url_for('results', page=page+1, search_input=search_input, console=console, videogame=videogame, company=company, date_ini=date_ini, author=author, date_end=date_end)
    
    if page != 1:
        prev_url = url_for('results', page=page-1, search_input=search_input, console=console, videogame=videogame, company=company, date_ini=date_ini, author=author, date_end=date_end)

    return render_template('index.html', next_url=next_url, prev_url=prev_url, noticias=articulos["hits"], total_noticias=total_noticias)

if __name__ == '__main__':
    app.run()
