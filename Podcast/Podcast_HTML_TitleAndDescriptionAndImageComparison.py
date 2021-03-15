#! /tmp/python3

# -------------------------------------------------------------------------------------------------
# VERSION: 2.0
#
# Purpose Statement: For testing Podcast Show Pages - NOT Episode pages
#
# JIRA Ticket Link (if applicable):
#
# Original Author: S Lehnert  Created: April 2020
# Updating Author: S Lehnert  Updated: October 2020
# Updating Author: S Lehnert  Updated: March 2021
# Updating Author:
# Last Updated:
# -------------------------------------------------------------------------------------------------
# Additional Information (Optional):
# URL Format: sanitized
#
# Acceptance Criteria:
# 1) Match api title with: HTML <title>, og:title, and twitter:title
# 2) Match api description with: HTML <description>, twitter:description, and
#    og:description
# 3) Match api dynamic-meta-image with: HTML twitter:image and og:image
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

# Podcast API URL
podcast_api_url  = "sanitized"

# Get all of the podcast data from the API as a list of dictionaries
podcast_data_text = functions.call_url(podcast_api_url)
podcast_data = json.loads(podcast_data_text) # <-- List of dictionaries

# Variables
failed_title_calls = 0
failed_description_calls = 0
failed_image_calls = 0
podcasts_failed = 0
total_calls = 0

# Starting the for loop to check data for each podcast
for podcast_dictionary in podcast_data["data"]:
    total_calls += 1
    tests_passed_for_this_podcast = 0

    # Pull out the important API variables
    site_slug       = podcast_dictionary["attributes"]["site_slug"]
    api_title       = podcast_dictionary["attributes"]["title"]
    api_description = podcast_dictionary["attributes"]["description"]
    api_image       = podcast_dictionary["attributes"]["image"]

    # Build the url to visit the podcast web page
    podcast_url = "sanitized" % site_slug
    # Call for the podcast web page data
    page_data = functions.call_url(podcast_url)[:PAGE_BUFFER]


    # ------------------------------------------------------------------------
    # TEST 1 of 3: Compare API title with HTML <title>, og:title and
    # twitter:title. All 4 should match.
    # ------------------------------------------------------------------------
    print("   TEST 1 of 3: Title Check")
    # If None/Empty, return empty string. Else return in uppercase.
    api_title     = functions.isNoneOrEmpty(api_title, "Podcast API Title")

    # Function returns string in upper case
    html_title    = functions.get_title(page_data)
    og_title      = functions.get_meta_tag_content(page_data, "og:title")
    twitter_title = functions.get_meta_tag_content(page_data,"", "twitter:title")

    # Comparison time - all titles should match
    print("      Looking for       : '%s'" % api_title)
    print("      OG Found          : '%s'" % og_title)
    print("      Twitter Found     : '%s'" % twitter_title)
    print("      HTML Title Found  : '%s'" % html_title)

    # If they all match, test passes. Else, test fails.
    if api_title == og_title and api_title == twitter_title and \
            api_title == html_title:
        message = "   TEST 1 of 3: %s" % PASSED
        tests_passed_for_this_podcast += 1
    else:
        message = "   TEST 1 of 3: %s" % FAILED
        failed_title_calls += 1
    functions.show_message(message)


    # ------------------------------------------------------------------------
    # TEST 2 of 3: Compare API description with HTML <description>,
    # og:description and twitter:description. All 4 should match.
    # ------------------------------------------------------------------------
    print("   TEST 2 of 3: Description Check")
    # If None/Empty, return empty string. Else return in uppercase.
    api_description     = functions.isNoneOrEmpty(api_description, "Podcast API Description")

    # Function returns string in upper case
    html_description    = functions.get_meta_tag_content(page_data,"", "description")
    og_description      = functions.get_meta_tag_content(page_data, "og:description")
    twitter_description = functions.get_meta_tag_content(page_data,"","twitter:description")

    # Sometimes descriptions have ${PARAMVALUE} and we want an empty string
    # if that happens.
    og_description      = functions.check_for_empty(og_description)
    twitter_description = functions.check_for_empty(twitter_description)
    html_description    = functions.check_for_empty(html_description)

    # Comparison time - all four descriptions should match
    print("      Looking for     : '%s'" % api_description)
    print("      OG Found        : '%s'" % og_description)
    print("      Twitter Found   : '%s'" % twitter_description)
    print("      HTML Desc Found : '%s'" % html_description)

    # If they all match, test passes. Else, test fails.
    if api_description == og_description and \
            api_description == twitter_description and \
            api_description == html_description:
        message = "   TEST 2 of 3: %s" % PASSED
        tests_passed_for_this_podcast += 1
    else:
        message = "   TEST 2 of 3: %s" % FAILED
        failed_description_calls += 1
    functions.show_message(message)


    # ------------------------------------------------------------------------
    # TEST 3 of 3: Compare API image with HTML og:image and HTML twitter:image.
    # All 3 should match.
    # ------------------------------------------------------------------------
    print("   TEST 3 of 3: Image Check")
    # If None/Empty, return empty string. Else return in uppercase.
    api_image     = functions.isNoneOrEmpty(api_image, "Podcast API Image")

    # Function returns string in upper case
    og_image      = functions.get_meta_tag_content(page_data, "og:image")
    twitter_image = functions.get_meta_tag_content(page_data, "", "twitter:image")

    # Comparison time - all three image urls should match
    print("      Looking for     : '%s'" % api_image)
    print("      OG Found        : '%s'" % og_image)
    print("      Twitter Found   : '%s'" % twitter_image)

    # If they all match, test passes. Else, test fails.
    if api_image == og_image and api_image == twitter_image:
        message = "   TEST 3 of 3: %s" % PASSED
        tests_passed_for_this_podcast += 1
    else:
        message = "   TEST 3 of 3: %s" % FAILED
        failed_image_calls += 1
    functions.show_message(message)


    # -----------------------------
    # End of Loop tally
    # -----------------------------

    # If a test failed, the podcast fails.
    if tests_passed_for_this_podcast != 3:
        podcasts_failed += 1

    # Makes the console printout easier to read
    message = "\n"
    functions.show_message(message)


# ------------------------------------------
# Outside the for loop, print the results
# ------------------------------------------
print("=======\nRESULTS\n=======")
print("Titles failed        = %d of %d" % (failed_title_calls, total_calls))
print("Descriptions failed  = %d of %d" % (failed_description_calls, total_calls))
print("Images failed        = %d of %d" % (failed_image_calls, total_calls))
print("-------------------------------")
print("Podcasts failed      = %d of %d" % (podcasts_failed, total_calls))

FillGoogleSheetWithTestResults.fillSheet(MY_FILENAME, podcasts_failed)

sys.exit(0)
