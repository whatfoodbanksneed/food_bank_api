# Foodbank

One Paragraph of project description goes here

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why







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

N.B. tabs are tabs, not 4 spaces. Sorry / not sorry.