#! /tmp/python3

# -------------------------------------------------------------------------------------------------
# VERSION: 2.0
#
# Purpose Statement:
# JIRA Ticket Link (if applicable):
#
# Original Author: S Lehnert  Created: May 2020
# Updating Author: S Lehnert  Updated: October 2020
# Updating Author: S Lehnert  Updated: March 2021
# Updating Author:
# Last Updated:
# -------------------------------------------------------------------------------------------------
# Additional Information (Optional):
#  This script is not the same as the SEO_HTML_TitleAndDescriptionComparison
#  script. The other script compares with the Clay API data. This one verifies
#  the <title> tag, og:title, and twitter:title tags on the Listen Live web page
#  match the expected title.
#
# Acceptance Criteria:
# Station Listen Live Web Page: All the HTML title tags should match the title
#  built from Core API Station data.
#
#    API       | |    HTML
#    ---       | |    ----
#    TITLE     | |     TITLE
#    TITLE     | |    OG:TITLE
#    TITLE     | |  TWITTER: TITLE
#
# -------------------------------------------------------------------------------------------------

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

# The Core API - Just grabbing the first 100 stations
api_url = "sanitized"

# Get all of the station data from the core API as a list of dictionaries
station_data_text = functions.call_url(api_url)
station_data = json.loads(station_data_text) # <-- List of dictionaries

# Variables
stations_failed = 0
total_calls = 0

# Starting the for loop to check each station's data content
for station_dictionary in station_data["data"]:
    total_calls += 1

    # Pull out the important Core API variables
    site_slug = station_dictionary["attributes"]["site_slug"]
    station_name  = station_dictionary["attributes"]["name"]
    station_slogan = station_dictionary["attributes"]["slogan"]

    # Building the url to visit the Station Listen Live web page
    listen_url = "sanitized" % site_slug
    # Call for the Listen Live web page
    page_source = functions.call_url(listen_url)[:PAGE_BUFFER]

    # Build the expected title from the Core API data. Core API is the "source
    # of truth" for these tests.
    # If station_slogan is None...or empty....the expected title changes
    if station_slogan == None or station_slogan == "":
        expected_title = 'sanitized' % station_name
    else:
        expected_title = 'sanitized' % (station_name, station_slogan)
    expected_title = expected_title.upper()

    # ------------------------------------------------------------------
    # TEST: Compare Station API title with HTML <title>, og:title and
    # twitter:title. All 4 should match.
    # ------------------------------------------------------------------
    print("   TEST: Title Comparison")

    # Function returns string in upper case
    html_title = functions.get_title(page_source)
    og_title = functions.get_meta_tag_content(page_source, "og:title")
    twitter_title = functions.get_meta_tag_content(page_source,"", "twitter:title")

    # Comparison time - all titles should match
    print("      Looking for    : '%s'" % expected_title)
    print("      Title Tag Found: '%s'" % html_title)
    print("      OG Found       : '%s'" % og_title)
    print("      Twitter Found  : '%s'" % twitter_title)

    if expected_title == og_title and expected_title == twitter_title and \
            expected_title == html_title:
        message = "   TEST: %s\n" % PASSED
    else:
        message = "   TEST: %s\n" % FAILED
        stations_failed += 1
    functions.show_message(message)


# ------------------------------------------
# Outside the for loop, print the results
# ------------------------------------------

print("========\nRESULTS\n========")
print("%d of %d tests failed" % (stations_failed, total_calls))
print("\n")

FillGoogleSheetWithTestResults.fillSheet(MY_FILENAME, stations_failed)

sys.exit(0)
