# Information retrieval system (Search Engine)
## Requirements

* Python 3.9+
* Django 4.2
* Elasticsearch 7.15.0

Elasticsearch is used as the search engine for the project. It is used to index the documents and search the documents based on the query. The project uses the Elasticsearch python client to interact with the Elasticsearch server.

## Elasticsearch setup:
1. Download and install Elasticsearch from the official website.

2. Start the Elasticsearch server.
    
3. Run elastic search server on 
```localhost:9200```


## Installation Steps
Run the following management commands for initial setup:

The Project includes single app:
- retriever

## Installation
Create a Virtual Environment

```sh
pip install virtualenv
virtualenv env
```
Activate Virtual Environment

```sh
 .\env\Scripts\activate
```

Install dependencies and Run the app

```sh
 pip install -r requirements.txt
```

Make migrations

```sh
 python manage.py makemigrations
 python manage.py migrate
```

Run the app

```sh
 cd SearchEngine
 python manage.py runserver
```

### Fronted library used: Bootstrap 5

Usage:
1. The user can insert files it can be a text file, pdf, image, or any other image format. The Use can also add links of the web pages.
2. The system will extract the text from the file and index it in the Elasticsearch server.
3. The user can search the documents based on the query.
4. The system will return the documents that match the query.
5. The user can click on the document to view the content of the document.

