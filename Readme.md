# Foodbank

A script to iterate through Trussell Trust foodbanks and find out what items they need, and a simple web server to let people query this and find out what items are needed by nearby foodbanks.

## Getting Started

pip install beautifulsoup4 
(the module we use to grab a webpage's HTML and do stuff with it)

pip install lxml 
(the module that does the XML parsing for beautifulsoup)

pip install requests 
(the module we use to make web requests)

pip install geopy
(the module we use to work out the distance between locations)

pip install web.py
(the module we use for the web server)

For a fresh file of foodbank information you should run:
python get_foodbank_details_and_write_to_file.py

That will create a new, current version of :
foodbank_data_storage.txt

That'll take a couple of hours, so you might prefer to just use the foodbank_data_storage.txt that comes in this repo when you're getting started.

Then run the server:
python server.py


## API Endpoints

The API accepts GET requests. There are two endpoints, shown below with an example request.

http://127.0.0.1:8080/nearest_foodbanks?latitude=52.629958&longitude=1.298408&number_of_foodbanks_to_show=5

http://127.0.0.1:8080/individual_foodbank_information?foodbank_name=Harrow%20Foodbank

## Running the tests

There aren't any unit or integration tests yet. Pull requests will be reviewed!