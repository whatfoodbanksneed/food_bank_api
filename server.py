import web
import ast
from geopy.distance import geodesic
import json
import html

from cheroot.server import HTTPServer
from cheroot.ssl.builtin import BuiltinSSLAdapter
HTTPServer.ssl_adapter = BuiltinSSLAdapter(
        certificate='/etc/letsencrypt/live/whatfoodbanksneed.org.uk/fullchain.pem',
	private_key='/etc/letsencrypt/live/whatfoodbanksneed.org.uk/privkey.pem'
	)


def return_nearest_food_banks_to_given_location (location_lat_long, number_of_food_banks_to_return):
		list_of_food_banks_and_distance_away_from_location = [] # Return list will contain food bank name and distance away, in ascending order of distance.
		for food_bank in list_of_dictionaries_containing_information_on_all_food_banks:
			if 'error' in list_of_dictionaries_containing_information_on_all_food_banks[food_bank]:
				continue # Skip the food bank if it has an error
			else:
				food_bank_lat_long = (list_of_dictionaries_containing_information_on_all_food_banks[food_bank]["latitude"], list_of_dictionaries_containing_information_on_all_food_banks[food_bank]["longitude"])
				distance_between_points = geodesic(location_lat_long, food_bank_lat_long).miles
				distance_between_points = round(distance_between_points)
				list_of_food_banks_and_distance_away_from_location.append([food_bank, distance_between_points])
		list_of_food_banks_and_distance_away_from_location.sort(key = return_second_element) # Sort the list by its second element (distance)
		return(list_of_food_banks_and_distance_away_from_location[0:number_of_food_banks_to_return]) # Return the number of food banks requested

def return_second_element (input_list): # Return the second element of an input list. Used when sorting by distance
	return(input_list[1])

def return_relevant_information_for_given_list_of_food_banks(list_of_food_banks_to_print):
	dictionary_to_return = {}
	for nearby_food_bank in list_of_food_banks_to_print: # Add some information before returning
		if 'error' in list_of_dictionaries_containing_information_on_all_food_banks[nearby_food_bank[0]]:
			continue # Skip the food bank if it has an error 
		else:
			tidy_food_bank_name =  html.unescape(nearby_food_bank[0])
			dictionary_to_return[tidy_food_bank_name] = {"Distance" : str(nearby_food_bank[1]) + " miles", "Address" : list_of_dictionaries_containing_information_on_all_food_banks[nearby_food_bank[0]]["address"], "Latitude" : float(list_of_dictionaries_containing_information_on_all_food_banks[nearby_food_bank[0]]["latitude"]), "Longitude" : float(list_of_dictionaries_containing_information_on_all_food_banks[nearby_food_bank[0]]["longitude"]), "Website" : list_of_dictionaries_containing_information_on_all_food_banks[nearby_food_bank[0]]["website"].replace("\\", ""), "Items needed" : list_of_dictionaries_containing_information_on_all_food_banks[nearby_food_bank[0]]["items_needed"], }
	return json.dumps(dictionary_to_return)

def show_nearby_food_banks_and_items_needed (location_tuple, number_of_food_banks_to_show):
	list_of_nearby_food_banks = return_nearest_food_banks_to_given_location(location_tuple, number_of_food_banks_to_show)
	return return_relevant_information_for_given_list_of_food_banks(list_of_nearby_food_banks)

def return_items_needed_by_given_food_bank (name_of_food_bank): # Give a food bank name. Get back a list of items needed
	if (name_of_food_bank in list_of_dictionaries_containing_information_on_all_food_banks):
		dictionary_to_return = {"Food bank name" : name_of_food_bank, "Items needed" : list_of_dictionaries_containing_information_on_all_food_banks[name_of_food_bank]["items_needed"]}
		return json.dumps(dictionary_to_return)
	else:
		return "This food bank isn't in our database, sorry"
	
urls = (
	'/', 'index',
	'/individual-food-bank-information', 'individual_food_bank_information',
	'/individual-food-bank-information/', 'individual_food_bank_information',
	'/nearest-food-banks', 'nearest_food_banks',
	'/nearest-food-banks/', 'nearest_food_banks'
)

class index:
	def GET(self):
		return "Hello! This is an API that gives information on nearby food banks and the items they need. Check out the documentation, when it exists..."

class individual_food_bank_information:
	def GET(self):
		user_data = web.input()
		try:
			return(return_items_needed_by_given_food_bank(user_data.name))
		except: 
			return("Please make a GET request to this endpoint with a name parameter")

class nearest_food_banks:
	def GET(self):
		user_data = web.input()
		try: # Raise an exception if we can't cast all 3 inputs as the right type below
			given_location = (float(user_data.lat), float(user_data.long))
			return(show_nearby_food_banks_and_items_needed(given_location, int(user_data.number)))
		except:
			return("Please make a GET request to this endpoint with lat, long, and number")

with open("food_bank_data_storage.txt", "r") as data_storage_file:
		list_of_dictionaries_containing_information_on_all_food_banks = ast.literal_eval(data_storage_file.readline())
		print("Information loaded from file\n")
		
if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
