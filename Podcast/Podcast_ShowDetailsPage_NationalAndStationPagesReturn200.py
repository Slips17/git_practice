#! /tmp/python3

# -------------------------------------------------------------------------------------------------
# VERSION: 2.0
#
# Purpose Statement: Verify Podcast show detail pages return 200 OK
# JIRA Ticket Link:
#
# Original Author: S Lehnert  Created: March 2020
# Updating Author: S Lehnert  Updated: November 2020
# Updating Author: S Lehnert  Updated: March 2021
# Updating Author:
# Last Updated:
# -------------------------------------------------------------------------------------------------
# Additional Information (Optional):
# URL Format: sanitized
# AND sanitized
#
# Acceptance Criteria:
# Verify the station's podcast detail page renders -> 200 OK for both URL formats
# -------------------------------------------------------------------------------------------------

# Standard Library Imports
import json
import sys
import os
import logging
import requests

# Variables
ME          = os.path.basename(__file__)        # Name of this file
MY_PATH     = os.path.dirname(os.path.realpath(__file__)) # Path for this file
MY_FILENAME = ME.split(".")[0]
LIBRARY_PATH    = os.path.join(MY_PATH, "../lib")
LOG_PATH    = os.path.join(MY_PATH)
LOG_FILE    = ME.replace(".py", ".log")  # filename.log
LOG_FORMAT  = "%(asctime)s, %(levelname)s, %(message)s"
PASSED      = "\033[32mPASSED\033[0m"  #\
WARNING     = "\033[33mWARNING\033[0m" # \___ Linux-specific colorization
FAILED      = "\033[31mFAILED\033[0m"  # /
ERROR       = "\033[31mERROR\033[0m"   #/
PAGE_BUFFER = 8192

# Custom library imports
sys.path.append(LIBRARY_PATH)
import functions, FillGoogleSheetWithTestResults

# Initialize the logger
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=LOG_FORMAT, filemode="w")
logger = logging.getLogger()
logger.info("Logging Started =================================================")


# ----- Here Be Functions! Arr! -----
# ----------------------------------------------------------------------------- get_station_site_slug()
def get_station_site_slug(station_call_sign):
    """ Call the station api with the call sign and get the corresponding
        station site slug
    """
    for station_dictionary in station_data["data"]:
        callsign = station_dictionary["attributes"]["callsign"]
        if callsign == station_call_sign:
            return_value = station_dictionary["attributes"]["site_slug"]
            return return_value


# ----------------------------------------------------------------------------- call_url()
def check_url(url, descriptor):
    """ Call a url and return True if the status code is 200 OK. Else return
        False. If there are any problems, then return an error.
    """
    functions.show_message("Calling: %s" % url)
    response_object = requests.get(url, timeout=30) #time out if 30 seconds passes with no response
    code = response_object.status_code

    if code != 200:
        functions.show_message("   %s. %s returned %d \n" % (FAILED, descriptor, code))
        return False
    else:
        functions.show_message("   %s, %s returned 200 \n" % (PASSED, descriptor))
        return True


# ---- End Functions section -----

# Set up for Station data
core_api_url  = "sanitized"
# Get the API data - used for finding station site slugs
station_data_text = functions.call_url(core_api_url)
station_data = json.loads(station_data_text)

# Set up for Podcast data
podcast_api_url  = "sanitized"
# Get the podcast API data
podcast_data_text = functions.call_url(podcast_api_url)
podcast_data = json.loads(podcast_data_text)


# Variables
page1_failed_calls = 0
page2_failed_calls = 0
total_calls = 0
total_podcasts = 0

# Starting the for loop to check data for each podcast
for podcast_dictionary in podcast_data["data"]:
    total_calls += 1

    podcast_base_url = "sanitized"
    podcast_site_slug = podcast_dictionary["attributes"]["site_slug"]

    # For podcasts with station info...continue on
    for station_info in podcast_dictionary["attributes"]["station"]:
        total_podcasts += 1

        callsign = station_info["callsign"]

        # Station callsign is used get the station site slug
        station_site_slug = get_station_site_slug(callsign)
        station_base_url = "sanitized" % station_site_slug

        # These two URLs are what we want to test!
        page1_url = "sanitized" % (station_base_url, podcast_site_slug)
        page2_url = "sanitized" % (podcast_base_url, podcast_site_slug)

        # Returns True if the URL responds with 200 OK. Else returns False.
        pg1_result = check_url(page1_url, "Podcast URL with Station Site Slug")
        pg2_result = check_url(page2_url, "Podcast URL without Station Site Slug")

        # Add up failures for results tally
        if pg1_result == False:
            page1_failed_calls += 1
        if pg2_result == False:
            page2_failed_calls += 1

# Printing out the results
print("=======PODCAST 200 RESPONSE RESULTS=======")
print ("Skipping all podcasts with empty station information.")
print ("Podcast URLs with Station Site Slugs failed    = %d" % page1_failed_calls)
print ("Podcast URLs without Station Site Slugs failed = %d" % page2_failed_calls)
print ("Total Podcasts checked = %d of %d" % (total_podcasts, total_calls))
print("=====END PODCAST 200 RESPONSE RESULTS=====\n\n")

total_failed = page1_failed_calls + page2_failed_calls
FillGoogleSheetWithTestResults.fillSheet(MY_FILENAME, total_failed)

sys.exit(0)
