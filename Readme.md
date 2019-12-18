# Foodbank API

A script to iterate through Trussell Trust foodbanks and find out what items they need, and a simple web server to let people query this and find out what items are needed by nearby foodbanks.

Read this blog post on the [background to this API](https://www.martinlugton.com/build-a-food-bank-api-part-1/)


## Getting Started

Start by installing the dependencies:

```
pip install beautifulsoup4
pip install lxml
pip install requests
pip install geopy
pip install web.py
```

For a fresh file of foodbank information you should run:
```
python get_foodbank_details_and_write_to_file.py
```

That will create a new, current version of foodbank_data_storage.txt

That'll take a couple of hours, so you might prefer to just use the foodbank_data_storage.txt that comes in this repo when you're getting started. It'll become increasingly out-of-date, but you can use it to make sure you've set things up correctly.

Then run the server:
```
python server.py
```


## API Endpoints

The API accepts GET requests. There are two endpoints, shown below with an example request.

http://127.0.0.1:8080/nearest_foodbanks?latitude=52.629958&longitude=1.298408&number_of_foodbanks_to_show=5

http://127.0.0.1:8080/individual_foodbank_information?foodbank_name=Harrow%20Foodbank


## Running the tests

There aren't any unit or integration tests yet. Pull requests will be reviewed!
