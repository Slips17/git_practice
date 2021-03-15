#! /tmp/python3

# --------------------------------------------------------------------------------------------------------------
# VERSION: 2.0
#
# Purpose:
# JIRA Ticket Link (if applicable):
#
# Original Author: H Wilson   Created: May 2020
# Updating Author: S Lehnert  Updated: August 2020
# Updating Author: S Lehnert  Updated: October 2020
# Updating Author: S Lehnert  Updated: March 2021
# Updating Author:
# Last Updated:
#
# TODO: This script needs better error handling for call urls. Script simply
# ends if the call response is 500 and does not report a failure to the
# Google Sheet
# --------------------------------------------------------------------------------------------------------------
# Additional Information (Optional): Not all Stations have the Clay Meta Title
# and Meta Description data. QA was given a list of Station IDs from the Product
# Team to validate against. This script calls a JSON file with the list of IDs.
#
# Note: This script uses two APIs. They are not the same.
# 1) One is the Core API. Looks like "sanitzed"
# 2) The other is the Clay API.
#
# Acceptance Criteria:
# 1) Expected title is formatted "sanitized"
#
# 2) Pull metaTitle from the Clay API for the station and verify it matches the
#    expected title.
#
# 3) Pull og:title from the Station Listen Live Url page and verify it matches
#    the expected title.
#
# 4) Pull the metaDescription from the Clay API for the station. Pull the
#    og:description from the Station Listen Live Url page. Verify the two
#    match.
#
# --------------------------------------------------------------------------------------------------------------

# Standard Library Imports
import json
import sys
import os
import logging

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

# Function for the script
# ----------------------------------------------------------------------------- compareAndPrint()
def compareAndPrint(expected, actual):
    """ This function simply makes a compare, prints PASSED/FAILED, and
        returns True/False.
    """
    match = functions.compare(expected, actual)
    if match:
        message = "   TEST: %s\n" %PASSED
    else:
        message = "   TEST: %s\n" %FAILED
    functions.show_message(message)
    return match


# Not all Stations have the Clay Meta Title and Meta Description data
# So we need to load a specific list of Station IDs from a JSON file
with open(LIBRARY_PATH + "/SEOIDs.json") as file:
    id_list = json.load(file)

# Counters to keep track of the number of tests that failed
clay_meta_title_failed = 0
meta_tag_og_title_failed = 0
meta_tag_og_description_failed = 0
stations_failed = 0
total_calls = 0

# Loop through each Station using the ID in the list
for item in id_list:
    total_calls += 1
    tests_failed = 0

    station_id = item["id"] #<-- Given in the json file

    # Build URLs for the testing
    api_url = "sanitized" % station_id
    meta_title_url = "sanitized" % station_id
    meta_description_url = "sanitized" % station_id

    # Get the station data from the Core API
    station_data_text  = functions.call_url(api_url)
    station_data       = json.loads(station_data_text)
    station_dictionary = station_data["data"]

    # Pull out the important Core API variables
    station_name        = station_dictionary["attributes"]["name"]
    station_slogan      = station_dictionary["attributes"]["slogan"]
    site_slug           = station_dictionary["attributes"]["site_slug"]

    # Build the expected title from the Core API data. Core API is the "source
    # of truth" for these tests.
    # If station_slogan is None...or empty....the expected title changes
    if station_slogan == None or station_slogan == "":
        expected_title = 'sanitized' % station_name
    else:
        expected_title = 'sanitized' % (station_name, station_slogan)
    expected_title = expected_title.upper()

    # Build the url for the Listen Live web page
    listen_url = "sanitized" % site_slug
    # Call for the Listen Live page data
    page_source = functions.call_url(listen_url)[:PAGE_BUFFER]


    # ------------------------------------------------------------------
    # TEST 1 of 3: Check Clay API metaTitle with expected_title
    # ------------------------------------------------------------------
    print("   TEST 1 of 3: Compare metaTitle to expected title" )

    # Call the Clay API for the dynamic meta title data
    meta_title_text = functions.call_url(meta_title_url)
    meta_title_data = json.loads(meta_title_text)

    # If there is no data, the function returns an empty string. Make the title
    # empty too. Otherwise, check the metaTitle content values.
    if meta_title_data == "":
        meta_title = ""
    else:
        meta_title = meta_title_data["_computed"]["metaTitle"]
        meta_title = functions.isNoneOrEmpty(meta_title, "Meta Title")

    # Compare and print expected vs actual metaTitle
    match = compareAndPrint(expected_title, meta_title)

    # Add to the counters if there wasn't a match
    if match == False:
        clay_meta_title_failed += 1
        tests_failed += 1


    # ---------------------------------------------------------
    # TEST 2 of 3: Match HTML og:title to expected_title
    # ---------------------------------------------------------
    print("   TEST 2 of 3 : Compare og.title to expected title")

    # Get the og:title content value from the Listen Live web page
    og_title = functions.get_meta_tag_content(page_source, "og:title")

    # Compare and print expected vs actual og:title
    match = compareAndPrint(expected_title, og_title)

    # Add to the counters if there wasn't a match
    if match == False:
        meta_tag_og_title_failed += 1
        tests_failed += 1


    # --------------------------------------------------------------------
    # TEST 3 of 3: Match HTML og:description to Clay API metaDescription
    # --------------------------------------------------------------------
    print("   TEST 3 of 3 : Compare og.description to metaDescription")

    # Call the Clay API for the dynamic meta description data
    meta_description_text = functions.call_url(meta_description_url)
    meta_description_data = json.loads(meta_description_text)

    # Set the Clay API description content value
    meta_description = meta_description_data["_computed"]["description"]
    meta_description = meta_description.upper()

    # Get the og:description content value from the Listen Live web page
    og_description = functions.get_meta_tag_content(page_source, "og:description")

    # Compare and print Clay API description vs og:description
    match = compareAndPrint(meta_description, og_description)

    # Add to the counters if there wasn't a match
    if match == False:
        meta_tag_og_description_failed += 1
        tests_failed += 1


    # -----------------------------
    # End of Loop tally
    # -----------------------------

    # If a test failed, the station is marked as failed
    if tests_failed != 0:
        stations_failed += 1

    # Makes the console printout easier to read
    message = "\n"
    functions.show_message(message)


# ------------------------------------------
# Outside the for loop, print the results
# ------------------------------------------

print("==========\nRESULTS\n============")
print("metaTitle failed      = %d of %d" % (clay_meta_title_failed, total_calls))
print("og.title failed       = %d of %d" % (meta_tag_og_title_failed, total_calls))
print("og.description failed = %d of %d" % (meta_tag_og_description_failed, total_calls))
print("---------------------------------")
print ("Stations failed      = %d of %d" % (stations_failed, total_calls))

FillGoogleSheetWithTestResults.fillSheet(MY_FILENAME, stations_failed)

sys.exit(0)
