from fastapi import FastAPI

app = FastAPI()

@app.get('/')

def username():
    return {'data': {'name':'Hashir'}}

@app.get('/about')
def about():
    return{'data':'about page'}