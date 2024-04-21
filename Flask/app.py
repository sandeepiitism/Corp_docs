from flask import Flask, request

app = Flask(__name__) ## name of python file i.e app.py should be same as variable here for (__name__)

stores = [
    {"name": "My Store",
     "items": [
         {"name":"chair",
          "price":15}
     ]}
]

@app.get("/page1")   ## API endpoint: https://127.0.0.1:5000/page1 --> get is to push value to client/webpage
def get_store_details():
    return {"stores": stores}

@app.post("/page1") ## API endpoint: https://127.0.0.1:5000/page1 --> post is to get the user input from webapp, so use request library
def create_store(): 
    req_data = request.get_json()
    new_store = {"name": req_data["name"], "items": []}
    stores.append(new_store)
    return new_store