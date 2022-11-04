from unittest import result
from flask import Flask, flash, render_template, request, redirect


from forms import QuerySearchForm

app = Flask(__name__)
app.secret_key = 'super secret key'

@app.route('/', methods=['GET', 'POST'])
def index():

    #cargar el "feed" (hacer una query ultimas noticias)
    search = QuerySearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    
    return render_template('index.html', form=search, results="Pagina Principal")



@app.route('/results')
def search_results(search):
    
    search_string = search.data['search']
    results = [search_string]
    if search.data['search'] == '':
        #lanzar la query
        pass

    if not results:
        flash('No results found!')
        print(search_string)
        return redirect('/')
    else:
        # display results
        search = QuerySearchForm(request.form)
        return render_template('index.html',form=search,  results=results)

if __name__ == '__main__':
    app.run()
