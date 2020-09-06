import requests
import ast
import time
from bs4 import BeautifulSoup

def show_items_needed_by_food_bank(food_bank_give_food_page_url): # Takes a food bank's "give food" page URL, and returns a list of items needed by that foodbank
	items_needed = []
	try:
		r = requests.get(food_bank_give_food_page_url)
	except: # Handle exceptions, e.g. the request library uncovering an SSL problem with a site
		return("Request failed. Likely an SSL certificate error")
	else:
		if ((r.status_code != 200) and (r.status_code != 304)): # If status code is neither 200 nor 304
			return("Bad status code")
		soup = BeautifulSoup(r.text, "lxml")
		ul_with_first_shopping_list = soup.find_all("ul", class_="page-section--sidebar__block-shopping-list", limit=1) # Only return the first 1
		if (not ul_with_first_shopping_list): # If no items were found, although the assumed give food page URL returned a good status code
			return("No items found")
		lis_of_first_shopping_list = ul_with_first_shopping_list[0].find_all("li") # Need to specify the index, even though it's a single item result set https://stackoverflow.com/questions/24108507/beautiful-soup-resultset-object-has-no-attribute-find-all
		for desired_item in lis_of_first_shopping_list:
			desired_item_in_unicode = str(desired_item.string)
			items_needed.append(desired_item_in_unicode) # Convert to unicode for more efficient memory use, as per https://www.crummy.com/software/BeautifulSoup/bs4/doc/#navigablestring
		return items_needed

response = requests.get("https://www.trusselltrust.org/get-help/find-a-foodbank/foodbank-search/?foodbank_s=all&callback=?")
if ((response.status_code == 200) or (response.status_code == 304)):
    print('Successful response from server')
else:
	print("Bad response from server:")
	print(response.status_code)
	raise SystemExit
print("")

trimmed_response_string = response.text[2:-2] # response.content would be in bytes. response.text gives a string. Trim the top and tail, to just give the list.
trimmed_response_string = trimmed_response_string.replace("false", "False") # Capitalise so Python understands the boolean 
trimmed_response_string = ast.literal_eval(trimmed_response_string) # Interrogate the string value as a variable - hopefully a list of dictionary objects. May cause stack overflow if too complex

number_of_food_banks = 0 # Including nonconforming ones
number_of_nonconforming_food_banks = 0 # A.K.A. "poorly" or "non-standard" food banks. Their website doesn't work, or are different to the usual model.

# Create a dictionary, with each food bank name as a key to its own dictionary object
# {address, latitude, longitude, website, donate_food_url, food needed (only populated if we successfully got this information), error (only populated if there was a problem getting the information)}
dictionary_of_food_banks_and_information = {}

for food_bank in trimmed_response_string:
	#if (food_bank['foodbank_information']['name'][0] == "B"): ## We work through food banks alphabetically. Stop at the start of the given letter. For debugging
	#	break
	number_of_food_banks += 1
	print(food_bank['foodbank_information']['name'])
	if (not food_bank['foodbank_information']['website']): # If this food bank doesn't have a website, add it, but without website or items needed info
		dictionary_of_food_banks_and_information[food_bank['foodbank_information']['name']] = {"address" : food_bank['foodbank_information']['geolocation']['address'], "latitude" : food_bank['foodbank_information']['geolocation']['lat'], "longitude" : food_bank['foodbank_information']['geolocation']['lng'], "website" : "", "error" : "No website given by master list", "location_type" : "food_bank"}
		number_of_nonconforming_food_banks += 1
	else:
		if (food_bank['foodbank_information']['website'][-1] == "/"): # Handle the URL, whether its given with a trailing slash or not
			likely_donate_food_page_url = food_bank['foodbank_information']['website'] + "give-help/donate-food/"
		else:
			likely_donate_food_page_url = food_bank['foodbank_information']['website'] + "/give-help/donate-food/"
		tidied_likely_donate_food_page_url = likely_donate_food_page_url.replace("\\", "") # Need to put backslash twice because it's an escape character
		items_needed_by_this_food_bank = show_items_needed_by_food_bank(tidied_likely_donate_food_page_url)	
		if type(items_needed_by_this_food_bank) == str: # If an error (string) was returned for this food bank, instead of a list of items, record the food bank with this information
			number_of_nonconforming_food_banks += 1			
			if (items_needed_by_this_food_bank == "Request failed. Likely an SSL certificate error"):
				dictionary_of_food_banks_and_information[food_bank['foodbank_information']['name']] = {"address" : food_bank['foodbank_information']['geolocation']['address'], "latitude" : food_bank['foodbank_information']['geolocation']['lat'], "longitude" : food_bank['foodbank_information']['geolocation']['lng'], "website" : "", "error" : items_needed_by_this_food_bank, "location_type" : "food_bank"} # Like the other cases of errors, but in this case we hide the website because there might be a security issue
			else:
				dictionary_of_food_banks_and_information[food_bank['foodbank_information']['name']] = {"address" : food_bank['foodbank_information']['geolocation']['address'], "latitude" : food_bank['foodbank_information']['geolocation']['lat'], "longitude" : food_bank['foodbank_information']['geolocation']['lng'], "website" : food_bank['foodbank_information']['website'], "error" : items_needed_by_this_food_bank, "location_type" : "food_bank"} # Don't populate items needed as we don't know what they are.
		if type(items_needed_by_this_food_bank) == list:
			dictionary_of_food_banks_and_information[food_bank['foodbank_information']['name']] = {"address" : food_bank['foodbank_information']['geolocation']['address'], "latitude" : food_bank['foodbank_information']['geolocation']['lat'], "longitude" : food_bank['foodbank_information']['geolocation']['lng'], "website" : food_bank['foodbank_information']['website'], "items_needed" : items_needed_by_this_food_bank, "location_type" : "food_bank"} # Add this food bank's information to the dictionary of food banks, as a dictionary itself
	if (food_bank['foodbank_centre'] != False): # If the food bank has child food bank centres
		# It looks like items needed and website are the same as the overall food bank.
		# Its name, telephone number, opening times, and various address values, are specific
		dictionary_of_food_banks_and_information[food_bank['foodbank_information']['name']]['food_bank_centres'] =  [] # Initialise empty list, to contain names of child food bank centres
		for food_bank_centre in food_bank['foodbank_centre']:
			if (('foodbank_name' in food_bank_centre) and ('address' in food_bank_centre['centre_geolocation']) and ('lat' in food_bank_centre['centre_geolocation']) and ('lng' in food_bank_centre['centre_geolocation'])): # Check that all the expected values are present for this food bank centre
				if type(items_needed_by_this_food_bank) == str: # As above. If a food bank centre's child food bank has an error or no website, store it differently.
					number_of_nonconforming_food_banks += 1			
					if (items_needed_by_this_food_bank == "Request failed. Likely an SSL certificate error"):
						if (food_bank_centre['foodbank_name'] in dictionary_of_food_banks_and_information): # If the food bank centre name is the same as an existing food bank name, append 'food bank centre' to the end. To avoid a key clash 
							dictionary_of_food_banks_and_information[food_bank_centre['foodbank_name'] + ' food bank centre'] = {"address" : food_bank_centre['centre_geolocation']['address'], "latitude" : food_bank_centre['centre_geolocation']['lat'], "longitude" : food_bank_centre['centre_geolocation']['lng'], "website" : "", "error" : items_needed_by_this_food_bank,  "location_type" : "food_bank_centre", "parent_food_bank" : food_bank['foodbank_information']['name']}
							dictionary_of_food_banks_and_information[food_bank['foodbank_information']['name']]['food_bank_centres'].append(food_bank_centre['foodbank_name'] + " food bank centre") # Record this food bank centre as a child in the entry for its parent food bank
						else:
							dictionary_of_food_banks_and_information[food_bank_centre['foodbank_name']] = {"address" : food_bank_centre['centre_geolocation']['address'], "latitude" : food_bank_centre['centre_geolocation']['lat'], "longitude" : food_bank_centre['centre_geolocation']['lng'], "website" : "", "error" : items_needed_by_this_food_bank, "location_type" : "food_bank_centre", "parent_food_bank" : food_bank['foodbank_information']['name']}
							dictionary_of_food_banks_and_information[food_bank['foodbank_information']['name']]['food_bank_centres'].append(food_bank_centre['foodbank_name']) # Record this food bank centre as a child in the entry for its parent food bank
					else:
						if (food_bank_centre['foodbank_name'] in dictionary_of_food_banks_and_information):
							dictionary_of_food_banks_and_information[food_bank_centre['foodbank_name']  + ' food bank centre'] = {"address" : food_bank_centre['centre_geolocation']['address'], "latitude" : food_bank_centre['centre_geolocation']['lat'], "longitude" : food_bank_centre['centre_geolocation']['lng'], "website" : food_bank['foodbank_information']['website'], "error" : items_needed_by_this_food_bank, "location_type" : "food_bank_centre", "parent_food_bank" : food_bank['foodbank_information']['name']}					
							dictionary_of_food_banks_and_information[food_bank['foodbank_information']['name']]['food_bank_centres'].append(food_bank_centre['foodbank_name']  + " food bank centre")
						else:
							dictionary_of_food_banks_and_information[food_bank_centre['foodbank_name']] = {"address" : food_bank_centre['centre_geolocation']['address'], "latitude" : food_bank_centre['centre_geolocation']['lat'], "longitude" : food_bank_centre['centre_geolocation']['lng'], "website" : food_bank['foodbank_information']['website'], "error" : items_needed_by_this_food_bank, "location_type" : "food_bank_centre", "parent_food_bank" : food_bank['foodbank_information']['name']}					
							dictionary_of_food_banks_and_information[food_bank['foodbank_information']['name']]['food_bank_centres'].append(food_bank_centre['foodbank_name'])
				if type(items_needed_by_this_food_bank) == list:
					if (food_bank_centre['foodbank_name'] in dictionary_of_food_banks_and_information):
						dictionary_of_food_banks_and_information[food_bank_centre['foodbank_name'] + ' food bank centre'] = {"address" : food_bank_centre['centre_geolocation']['address'], "latitude" : food_bank_centre['centre_geolocation']['lat'], "longitude" : food_bank_centre['centre_geolocation']['lng'], "website" : food_bank['foodbank_information']['website'], "items_needed" : items_needed_by_this_food_bank, "location_type" : "food_bank_centre", "parent_food_bank" : food_bank['foodbank_information']['name']}					
						dictionary_of_food_banks_and_information[food_bank['foodbank_information']['name']]['food_bank_centres'].append(food_bank_centre['foodbank_name'] + " food bank centre")
					else:
						dictionary_of_food_banks_and_information[food_bank_centre['foodbank_name']] = {"address" : food_bank_centre['centre_geolocation']['address'], "latitude" : food_bank_centre['centre_geolocation']['lat'], "longitude" : food_bank_centre['centre_geolocation']['lng'], "website" : food_bank['foodbank_information']['website'], "items_needed" : items_needed_by_this_food_bank, "location_type" : "food_bank_centre", "parent_food_bank" : food_bank['foodbank_information']['name']}					
						dictionary_of_food_banks_and_information[food_bank['foodbank_information']['name']]['food_bank_centres'].append(food_bank_centre['foodbank_name'])
			else: #If we don't have the all the expected pieces of information about this food bank's child food bank centres
				number_of_nonconforming_food_banks += 1
				continue ## If this food bank centre has doesn't have all the information we need, skip it. TODO think of what we might do here.
		#print(dictionary_of_food_banks_and_information[food_bank['foodbank_information']['name']]['food_bank_centres'])
	else:
		dictionary_of_food_banks_and_information[food_bank['foodbank_information']['name']]['food_bank_centres'] =  False # Record that this food bank does not have child food bank centres
	time.sleep(10) # Avoid hammering the server too aggressively.

	
print("Finished iterating through the list of food banks")
print("Number of food banks in total: " + str(number_of_food_banks))
print("Number of nonconforming food banks: " + str(number_of_nonconforming_food_banks))
print("")
for food_bank_name in dictionary_of_food_banks_and_information:
	print(food_bank_name)
	print(dictionary_of_food_banks_and_information[food_bank_name])
	print("")

with open("food_bank_data_storage.txt", "w") as data_storage_file:
	data_storage_file.write(str(dictionary_of_food_banks_and_information))
	print("Information written to file")
