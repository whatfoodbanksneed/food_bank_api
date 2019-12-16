import web
import ast
from geopy.distance import geodesic
import json

def return_nearest_foodbanks_to_given_location (location_lat_long, number_of_foodbanks_to_return):
		list_of_foodbanks_and_distance_away_from_location = [] # Return list will contain foodbank name and distance away, in ascending order of distance.
		for foodbank in list_of_dictionaries_containing_information_on_all_foodbanks:
			print(foodbank)
			if 'error' in list_of_dictionaries_containing_information_on_all_foodbanks[foodbank]:
				continue # Skip the foodbank if it has an error
			else:
				foodbank_lat_long = (list_of_dictionaries_containing_information_on_all_foodbanks[foodbank]["latitude"], list_of_dictionaries_containing_information_on_all_foodbanks[foodbank]["longitude"])
				distance_between_points = geodesic(location_lat_long, foodbank_lat_long).miles
				distance_between_points = round(distance_between_points)
				list_of_foodbanks_and_distance_away_from_location.append([foodbank, distance_between_points])
		list_of_foodbanks_and_distance_away_from_location.sort(key = return_second_element) # Sort the list by its second element (distance)
		return(list_of_foodbanks_and_distance_away_from_location[0:number_of_foodbanks_to_return]) # Return the number of foodbanks requested

def return_second_element (input_list): # Return the second element of an input list. Used when sorting by distance
	return(input_list[1])

def return_relevant_information_for_given_list_of_foodbanks(list_of_foodbanks_to_print):
	dictionary_to_return = {}
	for nearby_foodbank in list_of_foodbanks_to_print: # Add some information before returning
		if 'error' in list_of_dictionaries_containing_information_on_all_foodbanks[nearby_foodbank[0]]:
			continue # Skip the foodbank if it has an error
		else:
			dictionary_to_return[nearby_foodbank[0]] = {"Distance" : str(nearby_foodbank[1]) + " miles", "Address" : list_of_dictionaries_containing_information_on_all_foodbanks[nearby_foodbank[0]]["address"],  "Website" : list_of_dictionaries_containing_information_on_all_foodbanks[nearby_foodbank[0]]["website"].replace("\\", ""),  "Items needed" : list_of_dictionaries_containing_information_on_all_foodbanks[nearby_foodbank[0]]["items_needed"], }
	return json.dumps(dictionary_to_return)

def show_nearby_foodbanks_and_items_needed (location_tuple, number_of_foodbanks_to_show):
	list_of_nearby_foodbanks = return_nearest_foodbanks_to_given_location(location_tuple, number_of_foodbanks_to_show)
	return return_relevant_information_for_given_list_of_foodbanks(list_of_nearby_foodbanks)

def return_items_needed_by_given_foodbank (name_of_foodbank): # Give a foodbank name. Get back a list of items needed
	if (name_of_foodbank in list_of_dictionaries_containing_information_on_all_foodbanks):
		dictionary_to_return = {"Foodbank name" : name_of_foodbank, "Items needed" : list_of_dictionaries_containing_information_on_all_foodbanks[name_of_foodbank]["items_needed"]}
		return json.dumps(dictionary_to_return)
	else:
		return "This foodbank isn't in our database, sorry"
	
urls = (
	'/', 'index',
	'/individual_foodbank_information', 'individual_foodbank_information',
	'/nearest_foodbanks', 'nearest_foodbanks'
)

class index:
	def GET(self):
		return "Hello! This is an API that gives information on nearby foodbanks and the items they need. Check out the documentation, when it exists..."

class individual_foodbank_information:
	def GET(self):
		user_data = web.input()
		try:
			return(return_items_needed_by_given_foodbank(user_data.foodbank_name))
		except: 
			return("Please make a GET request to this endpoint with a 'foodbank_name' value given")

class nearest_foodbanks:
	def GET(self):
		user_data = web.input()
		try: # Raise an exception if we can't cast all 3 inputs as the right type below
			given_location = (float(user_data.latitude), float(user_data.longitude))
			return(show_nearby_foodbanks_and_items_needed(given_location, int(user_data.number_of_foodbanks_to_show)))
		except:
			return("Please make a GET request to this endpoint with latitude, longitude, and a 'number_of_foodbanks_to_show' integer")

with open("foodbank_data_storage.txt", "r") as data_storage_file:
		list_of_dictionaries_containing_information_on_all_foodbanks = ast.literal_eval(data_storage_file.readline())
		print("Information loaded from file\n")
		
if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()