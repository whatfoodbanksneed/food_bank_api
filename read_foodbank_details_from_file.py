import ast
from geopy.distance import geodesic

def return_nearest_foodbanks_to_given_location (location_lat_long, number_of_foodbanks_to_return):
		list_of_foodbanks_and_distance_away_from_location = [] # Return list will contain foodbank name and distance away, in ascending order of distance.
		for foodbank in list_of_dictionaries_containing_information_on_all_foodbanks:
			if 'error' in foodbank:
				continue # Skip the foodbank if it has an error
			foodbank_lat_long = (list_of_dictionaries_containing_information_on_all_foodbanks[foodbank]["latitude"], list_of_dictionaries_containing_information_on_all_foodbanks[foodbank]["longitude"])
			distance_between_points = geodesic(location_lat_long, foodbank_lat_long).miles
			distance_between_points = round(distance_between_points)
			list_of_foodbanks_and_distance_away_from_location.append([foodbank, distance_between_points])
		list_of_foodbanks_and_distance_away_from_location.sort(key = return_second_element) # Sort the list by its second element (distance)
		return(list_of_foodbanks_and_distance_away_from_location[0:number_of_foodbanks_to_return]) # Return the number of foodbanks requested

def return_second_element (input_list): # Return the second element of an input list. Used when sorting by distance
	return(input_list[1])

def print_relevant_information_for_given_list_of_foodbanks(list_of_foodbanks_to_print):
	for nearby_foodbank in list_of_foodbanks_to_print:
		print(nearby_foodbank[0] + " needs: ")
		print(list_of_dictionaries_containing_information_on_all_foodbanks[nearby_foodbank[0]]["items_needed"])
		print("Address: " + list_of_dictionaries_containing_information_on_all_foodbanks[nearby_foodbank[0]]["address"])
		print("Distance: " + str(nearby_foodbank[1]) + " miles\n")

def show_nearby_foodbanks_and_items_needed (location_tuple, number_of_foodbanks_to_show):
	list_of_nearby_foodbanks = return_nearest_foodbanks_to_given_location(location_tuple, number_of_foodbanks_to_show)
	print_relevant_information_for_given_list_of_foodbanks(list_of_nearby_foodbanks)

def return_items_needed_by_given_foodbank (name_of_foodbank): # Give a foodbank name. Get back a list of items needed
	## TODO currently assumes this key wil be present. Handle it if it isn't present.
	return  list_of_dictionaries_containing_information_on_all_foodbanks[name_of_foodbank]["items_needed"]
	
with open("foodbank_data_storage.txt", "r") as data_storage_file:
	list_of_dictionaries_containing_information_on_all_foodbanks = ast.literal_eval(data_storage_file.readline())
	print("Information read from file\n")

	#origin_lat_long = (51.590973, -0.362381) # harrow
	origin_lat_long = (52.458904, -1.947980) # harborne
	show_nearby_foodbanks_and_items_needed(origin_lat_long, 5)