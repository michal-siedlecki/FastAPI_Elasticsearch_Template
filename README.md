
# FastAPI Elasticsearch Template 


![GitHub repo size](https://img.shields.io/github/license/michal-siedlecki/FastAPI_Elasticsearch_Template)
![GitHub repo size](https://img.shields.io/github/repo-size/michal-siedlecki/FastAPI_Elasticsearch_Template)


REST API template with Oauth2 authentication and google account login implementation. 
Created in Python with FastAPI framework The data is stored using Elasticsearch engine.

## Prerequisites

Before you begin, ensure you have met the following requirements:
* You have installed `python` >= 3.6.2
* You have a `<Windows/Linux/Mac>` machine.

## Installing FastAPI Elasticsearch Template

To install FastAPI Elasticsearch Template, follow these steps:

Linux and macOS activate virtual environment and install dependencies:
```
git clone https://github.com/michal-siedlecki/FastAPI_Elasticsearch_Template
source venv/bin/activate
pip install -r requirements.txt
```

Install and set up Elasticsearch engine adn run it locally


## Using FastAPI Elasticsearch Template

In order to use FastAPI Elasticsearch Template type:

```
uvicorn  core.main:app --reload
```

Now app is available under localhost:8000.
all `users/` endpoints require authentication. 


## Tests

Several unit tests have been prepared for the application. To run the tests type:
````buildoutcfg
pytest
````

## Contact

* [@michal-siedlecki](https://github.com/michal-siedlecki) 😎 [author]

If you want to contact me you can reach me at <siedlecki.michal@gmail.com>.

## License

This project uses the following license: MIT (<https://github.com/michal-siedlecki/FastAPI_Elasticsearch_Template/blob/master/LICENSE>).


