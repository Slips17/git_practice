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
# For station podcast show page urls - different script checks national urls
#
# Acceptance Criteria:
# 1) Match the Podcast API information with the HTML meta tags
#    API            | |    HTML
#    ---            | |    ----
#    TYPE           | |    TYPE
#    TITLE          | |    PODCAST NAME
#    ID             | |    PODCAST ID
#    PARTNER ID     | |    PARTNER ID
#    PARTNER NAME   | |    PARTNER NAME
#    CATEGORY NAME  | |    PODCAST CATEGORY
#    IMAGE          | |    PODCAST LOGO
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


# ----- Here Be Functions! Arr! -----
# ----------------------------------------------------------------------------- get_station_site_slug()
def get_station_site_slug(station_call_sign):
    """ Call the station api with the call sign and get the corresponding station
        site slug
    """
    for station_dictionary in station_data["data"]:
        callsign = station_dictionary["attributes"]["callsign"]
        if callsign == station_call_sign:
            return_value = station_dictionary["attributes"]["site_slug"]
            return return_value


# ----------------------------------------------------------------------------- runTagCheck()
def runTagCheck(api_value, web_page_data, tag):
    """ Using the provided web page data source, find the content for the tag.
        Then compare that content value with the expected api value. Return True
        or False. This function expects a single content value and a single web
        page data source.
    """

    # Function returns string in upper case
    branch_io_tag_from_html_url = functions.get_meta_tag_content(web_page_data, "", tag)

    # Comparison time
    match = functions.compare(api_value, branch_io_tag_from_html_url)

    if match == True:
        message = "   TEST for %s: %s\n" % (tag, PASSED)
    else:
        message = "   TEST for %s: %s\n" % (tag, FAILED)
    functions.show_message(message)

    return match


# ---- End Functions section -----

# Calling the API URLs
core_api_url  = "sanitized"
# Get station data from the core API
station_data_text = functions.call_url(core_api_url)
station_data = json.loads(station_data_text)

podcast_api_url = "sanitized"
# Get podcast data from the podcast API
podcast_data_text = functions.call_url(podcast_api_url)
podcast_data = json.loads(podcast_data_text)


# Variables
failed_type          = 0
failed_title         = 0
failed_id            = 0
failed_partner_id    = 0
failed_partner_name  = 0
failed_category_name = 0
failed_image         = 0

podcasts_passed = 0
podcasts_failed = 0
skipped = 0
total_calls = 0

# For info in the podcast api data
for podcast_dictionary in podcast_data["data"]:
    total_calls += 1

    podcast_site_slug  = podcast_dictionary["attributes"]["site_slug"]

    # -------------------------------------------------------------
    # Get the podcast varialbes for testing.
    # These are from the podcast API so they are all "expected"
    # values to be compared with HTML tag "actual" values
    # -------------------------------------------------------------
    expected_type      = podcast_dictionary["type"]
    expected_id        = podcast_dictionary["id"]
    expected_title     = podcast_dictionary["attributes"]["title"]
    expected_image     = podcast_dictionary["attributes"]["image"]

    # Partner data
    podcast_partner        = podcast_dictionary["attributes"]["partner"]
    expected_partner_id    = podcast_partner["id"]
    expected_partner_name  = podcast_partner["name"]

    # Category is a LIST (of ONE dictionary) that is nested inside of "attributes"
    # Right now HTML only contains the first one from the list
    podcast_category       = podcast_dictionary["attributes"]["category"]
    expected_category_name = podcast_category[0]["name"]

    # -------------------------------------------------------------
    # Check if the variables are null/None/empty
    # Set them to empty strings for comparison if they are
    # -------------------------------------------------------------
    expected_id            = functions.isIDEmpty(expected_id)
    expected_partner_id    = functions.isIDEmpty(expected_partner_id)
    expected_type          = functions.isNoneOrEmpty(expected_type, "Podcast Type")
    expected_title         = functions.isNoneOrEmpty(expected_title, "Podcast Title")
    expected_partner_name  = functions.isNoneOrEmpty(expected_partner_name, "Partner Name")
    expected_category_name = functions.isNoneOrEmpty(expected_category_name, "Category Name")
    expected_image         = functions.isNoneOrEmpty(expected_image, "Image")

    # ----------------------------------------------------------------
    # Only testing Station podcast pages; not National podcasts
    # ----------------------------------------------------------------
    if podcast_dictionary["attributes"]["station"] == []:
        print("\n***\nThis Podcast %s is National and has no Station data." % expected_id)
        print("\nSkipping to the next one.\n***\n")
        skipped += 1

    # ----------------------------------------------------------------
    # For each station podcast page, get station info and build the URL
    # Then run the tests against the URL
    # ----------------------------------------------------------------
    for station_info in podcast_dictionary["attributes"]["station"]:
        # Get the station site slug
        callsign = station_info["callsign"]
        station_site_slug = get_station_site_slug(callsign)

        # Building the podcast url
        podcast_url = "sanitized" % (station_site_slug, podcast_site_slug)
        # Get the podcast web page data
        page_data = functions.call_url(podcast_url)[:PAGE_BUFFER]

        # -------------------------------------------------------------
        # TEST 1 of 7: Compare Podcast API Type with HTML tag Type.
        # -------------------------------------------------------------
        print("   TEST 1 of 7: Podcast Type")
        type_test = runTagCheck(expected_type, page_data, "branch:deeplink:type")
        if type_test == False:
            failed_type += 1

        # -------------------------------------------------------------
        # TEST 2 of 7: Compare API title with HTML podcast name.
        # -------------------------------------------------------------
        print("   TEST 2 of 7: Title Check")
        title_test = runTagCheck(expected_title, page_data, "branch:deeplink:podcast_name")
        if title_test == False:
            failed_title += 1

        # -------------------------------------------------------------
        # TEST 3 of 7: Compare API ID with HTML Podcast ID.
        # -------------------------------------------------------------
        print("   TEST 3 of 7: ID Check")
        id_test = runTagCheck(str(expected_id), page_data, "branch:deeplink:podcast_id")
        if id_test == False:
            failed_id += 1

        # -------------------------------------------------------------
        # TEST 4 of 7: Compare API Partner ID with HTML Partner ID.
        # -------------------------------------------------------------
        print("   TEST 4 of 7: Partner ID Check")
        partner_id_test = runTagCheck(str(expected_partner_id), page_data, "branch:deeplink:partner_id")
        if partner_id_test == False:
            failed_partner_id += 1

        # -------------------------------------------------------------
        # TEST 5 of 7: Compare API Partner Name with HTML partner name.
        # -------------------------------------------------------------
        print("   TEST 5 of 7: Partner Name Check")
        partner_name_test = runTagCheck(expected_partner_name, page_data, "branch:deeplink:partner_name")
        if partner_name_test == False:
            failed_partner_name += 1

        # -------------------------------------------------------------
        # TEST 6 of 7: Compare API Category Name with HTML category.
        # -------------------------------------------------------------
        print("   TEST 6 of 7: Category Name Check")
        category_test = runTagCheck(expected_category_name, page_data, "branch:deeplink:podcast_category")
        if category_test == False:
            failed_category_name += 1

        # -------------------------------------------------------------
        # TEST 7 of 7: Compare API Image with HTML Podcast Logo.
        # -------------------------------------------------------------
        print("   TEST 7 of 7: Image Check")
        image_test = runTagCheck(expected_image, page_data, "branch:deeplink:podcast_logo")
        if image_test == False:
            failed_image += 1

        # -------------------------------------------------------------
        #  TEST RESULTS SECTION
        # -------------------------------------------------------------

        # Check if all the tests are truthy
        if type_test and title_test and id_test and partner_id_test \
                and partner_name_test and category_test and image_test:
            podcast_result = PASSED
            podcasts_passed += 1
        else:
            podcast_result = FAILED
            podcasts_failed += 1

        # Print and tally results before going to the next url for testing
        message = "Podcast Result = %s\n\n" % podcast_result
        functions.show_message(message)


# Outside the For loops - printing results
print("=======\nPODCAST BRANCH IO SHOW PAGE RESULTS\n=======")
print("Test 1 - Type:         %d of %d Failed" % (failed_type, total_calls))
print("Test 2 - Title:        %d of %d Failed" % (failed_title, total_calls))
print("Test 3 - ID:           %d of %d Failed" % (failed_id, total_calls))
print("Test 4 - Partner ID:   %d of %d Failed" % (failed_partner_id, total_calls))
print("Test 5 - Partner Name: %d of %d Failed" % (failed_partner_name, total_calls))
print("Test 6 - Category:     %d of %d Failed" % (failed_category_name, total_calls))
print("Test 7 - Image:        %d of %d Failed" % (failed_image, total_calls))
print("--------------------------------------------------")
print("Podcasts failed    = %d" % podcasts_failed)
print("Podcasts skipped   = %d" % skipped)
print("Total Calls PASSED = %d of %d " % (podcasts_passed, total_calls))
print("=====END PODCAST BRANCH IO SHOW PAGE RESULTS=====\n\n")

FillGoogleSheetWithTestResults.fillSheet(MY_FILENAME, podcasts_failed)

sys.exit(0)
