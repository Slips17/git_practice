#! /tmp/python3

# -------------------------------------------------------------------------------------------------
# VERSION: 2.0
#
# Purpose Statement:
# JIRA Ticket Link (if applicable):
#
# Original Author: S Lehnert  Created: June 2020
# Updating Author: S Lehnert  Updated: July 2020
# Updating Author: S Lehnert  Updated: Oct 2020
# Updating Author:
# Last Updated:
# -------------------------------------------------------------------------------------------------
# Additional Information (Optional):
# This script is sharing json files with other scripts. Therefore, only specific information from
# those json files will be called out.
# This script is testing specific URLs. These are previously created pages.
# This script does NOT search and pull up existing pages to check them.
#
# Acceptance Criteria:
# 1) STATION Article and Gallery pages: Branch IO HTML meta tags should match the Station API
#
#    API                 | |    HTML
#    ---                 | |    ----
#    DISPLAY NAME        | |    MARKET
#    CATEGORY            | |    CATEGORY
#    GENRE NAME          | |    GENRE
#    ID                  | |    STATION ID
#    SQUARE LOGO SMALL   | |    STATION LOGO
#    NAME                | |    STATION NAME
#
# 2)  STATION Article and Gallery pages: Branch IO HTML meta tags for editorial_tags should match
#     ["QA", "SHANA", "TEST", "AUTOMATION", "BACKEND"] though not necessarily in that order
#
# 3) NATIONAL Article and Gallery pages:
#    A) Should definitely have the station_name Branch IO HTML meta tag
#    B) The value should be `sanitized`
#
# -------------------------------------------------------------------------------------------------

# Standard Library Imports
import json
import sys
import os
import logging
import StationBranchIOTest
import NationalBranchIOTest

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

# URLS - listed in a json file
with open(LIBRARY_PATH + "/StationBranchIOUrls.json") as file:
    station_urls = json.load(file)

with open(LIBRARY_PATH + "/NationalBranchIOUrls.json") as file2:
    national_page_urls = json.load(file2)


######################################
# Testing the Station URLs
######################################

#----------------------------------------------
# Tests 1 through 6 are handled in a function
# that all the Branch IO scripts call.
#----------------------------------------------

# Call the Base Branch IO Test to check Station Market, Logo, Name, ID,
# Genre Name, and Category API values. 6 Tests. Returns the total number of
# overall page failures. Does NOT return the number of failures per each test
# run, but DOES print that information to the log and console.

# We only want to test the article and gallery urls from the json file
failures = StationBranchIOTest.baseTest(station_urls, "article_url", "gallery_url")

#-------------------------------------------------------------
# TEST 7: Compare Editorial Tags with Known Tags.
# Expecting tags: QA, Shana, test, Automation, backend
# Because tags may be in a different order, we are not able
# to use the functions in the StationBranchIOTagCheck script.
#-------------------------------------------------------------

# Using the same json file - same urls - we used for the other 6 tests
for section in station_urls:
    # We only want to test the article and gallery urls from the json file
    html_url1 = section["article_url"]
    html_url2 = section["gallery_url"]

    # Call for the web page data once and use the data for the test
    url1_web_page_data = functions.call_url(html_url1)[:PAGE_BUFFER]
    url2_web_page_data = functions.call_url(html_url2)[:PAGE_BUFFER]
    expected_tags = ['AUTOMATION', 'BACKEND', 'TEST', 'QA', 'SHANA']

    print("   TEST: Editorial Tags Check")
    # Function returns string in upper case
    branch_io_tags_from_html_url1 = functions.get_meta_tag_content_list(url1_web_page_data, "", "branch:deeplink:editorial_tags")
    branch_io_tags_from_html_url2 = functions.get_meta_tag_content_list(url2_web_page_data, "", "branch:deeplink:editorial_tags")

    # Comparison time
    print("Comparing Expected Tags: %s" % expected_tags)
    print("With Article tags:       %s" % branch_io_tags_from_html_url1)
    print("And with Gallery tags:   %s" % branch_io_tags_from_html_url2)

    mismatch = 0

    # Expected tags and Actual tags may not be in the same order
    # So we need to loop through and check each one
    for item in expected_tags:
        print("Item is: %s" % item)
        # Compare if the tag is in the article
        if item in branch_io_tags_from_html_url1:
            match1 = True
        else: # <-- Need the else otherwise True persists if only one item is in expected tags
            match1 = False

        # Compare if the tag is in the gallery
        if item in branch_io_tags_from_html_url2:
            match2 = True
        else: # <-- Need the else otherwise True persists if only one item is in expected tags
            match2 = False

        # Count how many mismatches there are
        if match1 == False or match2 == False:
            mismatch += 1

    # If all the tags match, test passes
    if mismatch == 0:
        message = "   TEST: %s\n" % PASSED
    else:
        message = "   TEST: %s\n" % FAILED
        failures += 1 # <-- Add to the failures number recorded for the other station tests 1-6
    functions.show_message(message)


######################################
# Testing the National URLs
######################################

# Call the Base Branch IO Test to check Station Name. 1 Test. Returns total
# number of overall page failures. Expecting station_name = sanitized

# We only want to test the article and gallery urls from the json file
failed_national_calls = NationalBranchIOTest.NationalBaseTest(national_page_urls, "article_url", "gallery_url")


##############################################
# Print results and report to GoogleSheets
##############################################

print("\n-------ARTICLE/GALLERY TEST RESULTS----------")
print("Part 1 Station: %d of %d FAILED" % (failures, len(station_urls)))
print("Part 2 National: %d of %d FAILED" % (failed_national_calls, len(national_page_urls)))
print("-------ARTICLE/GALLERY TEST RESULTS----------\n\n")

total_failed = failures + failed_national_calls
FillGoogleSheetWithTestResults.fillSheet(MY_FILENAME, total_failed)

sys.exit(0)
