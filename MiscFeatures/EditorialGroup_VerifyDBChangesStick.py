#! /tmp/python3

# -------------------------------------------------------------------------------------------------
# VERSION: 2.0
#
# Purpose Statement:
# JIRA Ticket Link (if applicable):
#
# Original Author: S Lehnert  Created: May 2020
# Updating Author: S Lehnert  Updated: November 2020
# Updating Author: S Lehnert  Updated: March 2021
# Updating Author:
# Last Updated:
# -------------------------------------------------------------------------------------------------
# Additional Information (Optional):
# Verify that changing editorial-group values in the database - sticks
#
# Acceptance Criteria:
# 1) Get editorial-group data: GET <sanitized-url>
# 2) Verify it has 3 fields: Feeds (which is a nested dict), Market, Site Slug
# Example:
# {
#     "id": 2,
#     "data": {
#         "feeds": {
#             "Urban": true,
#             "Hip Hop": true,
#             "Trending": true
#         },
#         "market": "Atlanta, GA",
#         "siteSlug": "siteSlug"
#     }
# },
#
# 3) Change values using a PUT statement. Only for ID = xxx
# 4) Get editorial-group data again and verify the change is displayed
# -------------------------------------------------------------------------------------------------

# Standard Library Imports
import json
import sys
import os
import time
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

# Variables
editorial_group_data_new = {}
editorial_feeds_new = {}
failed = 0

# ------------------------------------------------
# Step 1: GET editorial group data from database
# ------------------------------------------------

editorial_group_url = "sanitized-url"
editorial_group_text = functions.call_url(editorial_group_url)
editorial_group_data_original = json.loads(editorial_group_text)

# For each entry item returned in the GET response
for entry in editorial_group_data_original:

    # ------------------------------------------------------------
    # Step 2: Get the Original Values specifically for the entry
    # with id = xxx.
    #
    # Note: The xxx entry was created for testing with this script
    # so that changing information doesn't influence other
    # editorial group testing.
    # ------------------------------------------------------------

    editorial_id       = entry["id"]
    editorial_feeds    = entry["data"]["feeds"]  # <-- Feeds is a dictionary
    editorial_market   = entry["data"]["market"]
    editorial_siteSlug = entry["data"]["siteSlug"]

    # Currently only want to edit the entry for id: xxx - otherwise could break other testing
    if editorial_id == xxx:
        message = "<-- Original Values Start --> " \
                  "\nEditorial Feeds: %s " \
                  "\nEditorial Market: %s " \
                  "\nEditorial Site Slug: %s " \
                  "\n<-- Original Values End -->" \
                  % (editorial_feeds, editorial_market, editorial_siteSlug)
        functions.show_message(message)

        # ------------------------------------------------------------
        # Step 3: Make some changes to the 3 editable values
        # ------------------------------------------------------------

        # Change the Market Name
        if editorial_market == "Shana Market": # if we changed this before to Shana Market
            editorial_market_new = "Fake Market" # use Fake Market instead
        else:
            editorial_market_new = "Shana Market"

        # Change the siteSlug
        if editorial_siteSlug == "Shana siteSlug": # if we changed this before to Shana siteSlug
            editorial_siteSlug_new = "Fake siteSlug" # use Fake siteSlug instead
        else:
            editorial_siteSlug_new = "Shana siteSlug"

        # Change all the True to False and all the False to True in the Feeds section
        for key,value in editorial_feeds.items():
            print("Key is: " + key)
            if value == True:
                value_new = False
            else:
                value_new = True
            editorial_feeds_new[key] = value_new

        message = "<-- Edited Values Start -->   " \
                  "\nEditorial Feeds: %s " \
                  "\nEditorial Market: %s " \
                  "\nEditorial Site Slug: %s " \
                  "\n<-- Edited Values End -->" \
                  % (editorial_feeds_new, editorial_market_new, editorial_siteSlug_new)
        functions.show_message(message)

        # ------------------------------------------------------------
        # Step 4: Save all the edits into a payload dictionary and
        #         prep for the PUT command
        # ------------------------------------------------------------

        # Use the GET URL add /id_number and save it as the PUT URL
        editorial_put_url = editorial_group_url + "/" + str(editorial_id)
        # Save all the changes into a dictionary to use in the PUT command
        payload = {"feeds": editorial_feeds_new,
                   "market": editorial_market_new,
                   "siteSlug": editorial_siteSlug_new
                  }
        print("\nPayload is %s" % payload)

        # ------------------------------------------------------------
        # Step 5: Still inside the For loop -
        #         PUT in the changes for this item
        # ------------------------------------------------------------

        #PUT needs to be in json not Python
        try:
            print("Attempting to PUT the Payload into the database")
            headers = {"sanitized"}
            response_object = requests.put(editorial_put_url, headers=headers, json=payload)
            print("PUT response_object is %s\n" % response_object.text)

            if response_object == "": # Call Timed out
                message = "Call timed out"
                #FillGoogleSheetWithTestResults.fillSheet(MY_FILENAME, 1)
                raise ValueError(message)

            elif response_object.status_code == 200: # Good Response
                message = "   Success, Call returned %d\n" % response_object.status_code
                functions.show_message(message)
                # Get the text response from the call and translate it
                # to a Python Dictionary
                return_value = response_object.text

            else: # Bad response
                message = "Call to %s returned (%d)\n   %s ..." % (editorial_put_url, response_object.status_code,
                                                                   response_object.text[:80])
                #FillGoogleSheetWithTestResults.fillSheet(MY_FILENAME, 1)
                raise ValueError(message)

        except Exception  as e:
            #FillGoogleSheetWithTestResults.fillSheet(MY_FILENAME, 1)
            sys.stderr.write("   %s -- %s\n" %(ERROR, str(e)))
            sys.stderr.flush()
            logger.error(str(e))

# ------------------------------------------------------------
# Step 6: Wait 3 minutes for database sync.
# ------------------------------------------------------------

message = "Timer for 180 seconds. Waiting for PUT data to sync in the database."
functions.show_message(message)
print("Start time: %s" % time.ctime())
time.sleep(180)
print("End time: %s\n" % time.ctime())

# ------------------------------------------------------------
# Step 7: GET the values and
#         save into a new/updated dictionary
# ------------------------------------------------------------

editorial_group_text = functions.call_url(editorial_group_url)
editorial_group_data_after_edits = json.loads(editorial_group_text)
message = "Get the new values. Saving values into a second dictionary."
functions.show_message(message)

# ------------------------------------------------------------
# Step 8: Compare the original dictionary with the Edited one
# ------------------------------------------------------------

for entry in editorial_group_data_after_edits:
    # We don't care about any entries other than id = xxx
    if entry["id"] == xxx:
        actual_feeds = entry["data"]["feeds"]
        actual_market = entry["data"]["market"]
        actual_siteSlug = entry["data"]["siteSlug"]

        message = "<-- Second GET Values Start --> " \
                  "\nEditorial Feeds: %s " \
                  "\nEditorial Market: %s " \
                  "\nEditorial Site Slug: %s " \
                  "\n<-- Second GET Values End -->" \
                  % (actual_feeds, actual_market, actual_siteSlug)
        functions.show_message(message)

        # Loop for original data and compare
        for entry in editorial_group_data_original:
            # Again, only care about id = xxx
            if entry["id"] == xxx:
                original_feeds = entry["data"]["feeds"]
                original_market = entry["data"]["market"]
                original_siteSlug = entry["data"]["siteSlug"]

                message = "<-- Repeat Original Values Start --> " \
                          "\nEditorial Feeds: %s " \
                          "\nEditorial Market: %s " \
                          "\nEditorial Site Slug: %s " \
                          "\n<-- Repeat Original Values End -->" \
                          % (original_feeds, original_market, original_siteSlug)
                functions.show_message(message)

                # If any actual matches original, then the data change didn't stick
                if original_feeds == actual_feeds:
                    message = "Feeds Failed.\nOriginal feeds: %s" % original_feeds
                    functions.show_message(message)
                    failed += 1
                if original_market == actual_market:
                    message = "Market Failed.\nOriginal market: %s" % original_market
                    functions.show_message(message)
                    failed += 1
                if original_siteSlug == actual_siteSlug:
                    message = "siteSlug Failed.\nOriginal siteSlug: %s" % original_siteSlug
                    functions.show_message(message)
                    failed += 1

        if failed == 0:
            message = "\nChanges were accepted. Test %s." % PASSED
        else:
            message = "\nNot all changes were accepted. Test %s." % FAILED
        functions.show_message(message)
        message = "Failed: %d of 3\n" % failed
        functions.show_message(message)

# Report Passed/Failed to the GoogleSheet
FillGoogleSheetWithTestResults.fillSheet(MY_FILENAME, failed)

sys.exit(0)
