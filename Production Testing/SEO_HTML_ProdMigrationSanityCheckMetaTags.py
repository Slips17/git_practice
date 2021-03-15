#! /tmp/python3

# -------------------------------------------------------------------------------------------------
# VERSION: 1.2
#
# Purpose Statement:
# JIRA Ticket Link (if applicable):
#
# Original Author: S Lehnert  Created: July 2020
# Updating Author: S Lehnert  Updated: September 2020
# Updating Author: S Lehnert  Updated: November 2020
# Updating Author:
# Last Updated:
# -------------------------------------------------------------------------------------------------
# Additional Information (Optional):
#  This script is checking Station Home Pages (Station Fronts) on **PROD**
#
# Acceptance Criteria:
# 1) THESE SHOULD MATCH
#
#    API                 | |    HTML
#    ---                 | |    ----
#    TITLE               | |    TITLE
#    TITLE               | |    OG:TITLE
#    TITLE               | |    TWITTER:TITLE
#    DESCRIPTION         | |    DESCRIPTION
#    DESCRIPTION         | |    OG:DESCRIPTION
#    DESCRIPTION         | |    TWITTER:DESCRIPTION
#    DISPLAY NAME        | |    MARKET
#    CATEGORY            | |    CATEGORY
#    GENRE NAME          | |    GENRE
#    ID                  | |    STATION ID
#    SQUARE LOGO SMALL   | |    STATION LOGO
#    NAME                | |    STATION NAME
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

# ----- Here Be Functions! Arr! -----
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
        message = "   TEST: %s\n" % PASSED
    else:
        message = "   TEST: %s\n" % FAILED
    functions.show_message(message)

    return match


# ---- End Functions section -----

# Variables
pages_failed = 0
total_calls  = 0

failed_title       = 0
failed_description = 0
failed_market      = 0
failed_category    = 0
failed_genre       = 0
failed_id          = 0
failed_logo        = 0
failed_name        = 0

# URLS - listed in a json file
with open(LIBRARY_PATH + "/migratedStationUrls.json") as file:
    station_urls = json.load(file)

# Cycle through each of the Stations and run the tests
for url in station_urls:
    total_calls += 1
    tests_failed = 0

    api_url  = url["api_url"]
    html_url = url["prod_url"]
    # html_url = url["preprod_url"]

    # Get Station data from the API
    station_data_text = functions.call_url(api_url)
    station_data = json.loads(station_data_text)

    # ---------------------------
    # Variable setup section
    # ---------------------------

    # Separate out the information we want into variables
    station_dictionary   = station_data["data"]
    station_id           = station_dictionary["id"]
    station_description  = station_dictionary["attributes"]["description"]
    station_slogan       = station_dictionary["attributes"]["slogan"]
    station_market       = station_dictionary["attributes"]["market"]["display_name"]
    station_name         = station_dictionary["attributes"]["name"]
    station_logo         = station_dictionary["attributes"]["square_logo_small"]

    # Category is a LIST (of ONE dictionary) that is nested inside of "attributes"
    station_category     = station_dictionary["attributes"]["category"]

    # Genre is a LIST (of ONE dictionary) that is nested inside of "attributes"
    station_genre        = station_dictionary["attributes"]["genre"]

    # If there is more than 1 dictionary in the genre list...print a message
    # (there should be a tag for each genre)
    if len(station_genre) > 1:
        message = "Station has more than one genre dictionary in the list!"
        functions.show_message(message)
        list_of_genre_names = []
        for item_dict in station_genre:
            name = item_dict["name"]
            list_of_genre_names.append(name)
        station_genre_name = list_of_genre_names
    else:
        station_genre_name = station_genre[0]["name"]

    # Call for the web page data once and use the data for the tests
    page_data = functions.call_url(html_url)[:PAGE_BUFFER]

    # ------------------
    # Test section
    # ------------------
    # ------------------------------------------------------------------------
    # TEST 1 of 8: Compare Expected Title with HTML Title, OG Title, and
    # Twitter Title
    # ------------------------------------------------------------------------
    print("   TEST 1 of 8: Title Check")

    # Build the expected title
    if station_slogan == None or station_slogan == "":
        expected_title = 'sanitized' % station_name
    else:
        expected_title = 'sanitized' % (station_name, station_slogan)
    expected_title = expected_title.upper()

    # Get the actual values from the web page
    html_title    = functions.get_title(page_data)
    og_title      = functions.get_meta_tag_content(page_data, "og:title", "")
    twitter_title = functions.get_meta_tag_content(page_data, "", "twitter:title")

    # Comparison time - all titles should match
    print("      Looking for     : '%s'" % expected_title)
    print("      Title Tag Found : '%s'" % html_title)
    print("      OG Found        : '%s'" % og_title)
    print("      Twitter Found   : '%s'" % twitter_title)

    # Print Pass/Fail - Increment counters if actual/expected values don't match
    if expected_title == og_title and \
            expected_title == twitter_title and \
            expected_title == html_title:
        message = "   TEST: %s\n" % PASSED
    else:
        message = "   TEST: %s\n" % FAILED
        failed_title += 1
        tests_failed += 1
    functions.show_message(message)

    # ------------------------------------------------------------------------
    # TEST 2 of 8: Compare the API description with the HTML Description,
    # OG Description, and Twitter Description
    # ------------------------------------------------------------------------
    print("   TEST 2 of 8: Description Check")

    # If ${PARAMVALUE}, return empty string
    station_description = functions.check_for_empty(station_description)
    # If None/Empty, return empty string. Else return in uppercase.
    station_description = functions.isNoneOrEmpty(station_description, "Station API Description")

    # Get the actual values from the web page
    html_description    = functions.get_meta_tag_content(page_data, "", "description")
    og_description      = functions.get_meta_tag_content(page_data, "og:description")
    twitter_description = functions.get_meta_tag_content(page_data, "", "twitter:description")

    # Comparison time - all descriptions should match
    print("      Looking for        : '%s'" % station_description)
    print("      Desc Tag Found     : '%s'" % html_description)
    print("      OG Desc Found      : '%s'" % og_description)
    print("      Twitter Desc Found : '%s'" % twitter_description)

    # Print Pass/Fail - Increment counters if actual/expected values don't match
    if station_description == og_description and \
            station_description == twitter_description and \
            station_description == html_description:
        message = "   TEST: %s\n" % PASSED
    else:
        message = "   TEST: %s\n" % FAILED
        failed_description += 1
        tests_failed += 1
    functions.show_message(message)

    # ------------------------------------------------------------------------
    # TEST 3 of 8: Compare the API Station Market with the HTML Market
    # ------------------------------------------------------------------------
    print("   TEST 3 of 8: Market Check")

    # If None/Empty, return empty string. Else return in uppercase.
    station_market = functions.isNoneOrEmpty(station_market, "Station Market")
    # Get the actual value - compare with expected - return True/False
    market_test = runTagCheck(station_market, page_data, "branch:deeplink:market")
    # Increment counters if actual/expected values do not match
    if market_test == False:
        failed_market += 1
        tests_failed += 1

    # ------------------------------------------------------------------------
    # TEST 4 of 8: Compare the API Station Category with the HTML Category
    # ------------------------------------------------------------------------
    print("   TEST 4 of 8: Category Check")

    # If None/Empty, return empty string. Else return in uppercase.
    station_category = functions.isCategoryOrGenreEmpty(station_category, "Station Category")

    # Make expected value uppercase and get actual value in uppercase
    if type(station_category) is list:
        message = "   The API Category is a list."
        station_category = [item.upper() for item in station_category]
        html_category = functions.get_meta_tag_content_list(page_data, "", "branch:deeplink:category")
    else:
        message = "   The API Category is a single value."
        station_category = station_category.upper()
        html_category = functions.get_meta_tag_content(page_data, "", "branch:deeplink:category")
    functions.show_message(message)

    # Compare actual value with expected - return True/False
    match = compareAndPrint(station_category, html_category)
    # Increment counters if actual/expected values do not match
    if match == False:
        failed_category += 1
        tests_failed += 1

    # ------------------------------------------------------------------------
    # TEST 5 of 8: Compare the API Station genre name with the HTML genre
    # ------------------------------------------------------------------------
    print("   TEST 5 of 8: Genre Check")

    # If None/Empty, return empty string. Else return in uppercase.
    station_genre_name = functions.isCategoryOrGenreEmpty(station_genre_name, "Station Genre Name")

    # Make expected value uppercase and get actual value in uppercase
    if type(station_genre_name) is list:
        message = "   The API Genre is a list."
        station_genre_name = [item.upper() for item in station_genre_name]
        html_genre_name = functions.get_meta_tag_content_list(page_data, "", "branch:deeplink:genre")
    else:
        message = "   The API Genre is a single value."
        station_genre_name = station_genre_name.upper()
        html_genre_name = functions.get_meta_tag_content(page_data, "", "branch:deeplink:genre")
    functions.show_message(message)

    # Compare actual value with expected - return True/False
    match = compareAndPrint(station_genre_name, html_genre_name)
    # Increment counters if actual/expected values do not match
    if match == False:
        failed_genre += 1
        tests_failed += 1

    # ------------------------------------------------------------------------
    # TEST 6 of 8: Compare the API Station ID with the HTML Station ID
    # ------------------------------------------------------------------------
    print("   TEST 6 of 8: ID Check")

    # If None/Empty, return empty string.
    station_id = functions.isIDEmpty(station_id)
    # Get the actual value - compare with expected - return True/False
    id_test = runTagCheck(str(station_id), page_data, "branch:deeplink:station_id")
    # Increment counters if actual/expected values do not match
    if id_test == False:
        failed_id += 1
        tests_failed += 1

    # ------------------------------------------------------------------------
    # TEST 7 of 8: Compare the API Station logo with the HTML logo
    # ------------------------------------------------------------------------
    print("   TEST 7 of 8: Logo Check")

    # If None/Empty, return empty string. Else return in uppercase.
    station_logo = functions.isNoneOrEmpty(station_logo, "Station Logo")
    # Get the actual value - compare with expected - return True/False
    logo_test = runTagCheck(station_logo, page_data, "branch:deeplink:station_logo")
    # Increment counters if actual/expected values do not match
    if logo_test == False:
        failed_logo += 1
        tests_failed += 1

    # ------------------------------------------------------------------------
    # TEST 8 of 8: Compare the API Station name with the HTML Station name
    # ------------------------------------------------------------------------
    print("   TEST 8 of 8: Name Check")

    # If None/Empty, return empty string. Else return in uppercase.
    station_name = functions.isNoneOrEmpty(station_name, "Station Name")
    # Get the actual value - compare with expected - return True/False
    name_test = runTagCheck(station_name, page_data, "branch:deeplink:station_name")
    # Increment counters if actual/expected values do not match
    if name_test == False:
        failed_name += 1
        tests_failed += 1


    # -----------------------------
    # End of Loop tally
    # -----------------------------
    if tests_failed != 0:
        pages_failed += 1

# ------------------------------------------
# Outside the for loop, print the results
# ------------------------------------------
print("======PROD SANITY CHECK RESULTS======")
print("Stations FAILED    : %d of %d" % (pages_failed, total_calls))
print("-----------------------------")
print("Titles FAILED      : %d of %d" % (failed_title, total_calls))
print("Descriptions FAILED: %d of %d" % (failed_description, total_calls))
print("Markets FAILED     : %d of %d" % (failed_market, total_calls))
print("Categories FAILED  : %d of %d" % (failed_category, total_calls))
print("Genres FAILED      : %d of %d" % (failed_genre, total_calls))
print("IDs FAILED         : %d of %d" % (failed_id, total_calls))
print("Logos FAILED       : %d of %d" % (failed_logo, total_calls))
print("Names FAILED       : %d of %d" % (failed_name, total_calls))
print("====END PROD SANITY CHECK RESULTS====\n")

FillGoogleSheetWithTestResults.fillMigrationSheet(MY_FILENAME, pages_failed)

sys.exit(0)
