from wtforms import Form, StringField, SelectField

class QuerySearchForm(Form):
    #choices = [('Artist', 'Artist'),
    #           ('Album', 'Album'),
    #           ('Publisher', 'Publisher')]
    
    search = StringField('')