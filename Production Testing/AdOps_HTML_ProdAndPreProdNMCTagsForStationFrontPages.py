#! /tmp/python3

# -------------------------------------------------------------------------------------------------
# VERSION: 1.1
#
# Purpose Statement:
# JIRA Ticket Link (if applicable):
#
# Original Author: S Lehnert  Created: July 2020
# Updating Author: S Lehnert  Updated: August 2020
# Updating Author: S Lehnert  Updated: November 2020
# Updating Author:
# Last Updated:
# -------------------------------------------------------------------------------------------------
# Additional Information (Optional):
#  This script is checking Station Home Pages (Station Fronts)
#  on Production and Pre-Production environments!!!
#
# Acceptance Criteria:
# 1) nmc:pid should be content=”homepage”
# 2) nmc:tag should be content=”sectionfront/homepage”
#
# -------------------------------------------------------------------------------------------------

# Imports
import json
import os
import sys
import logging

# Variables
ME          = os.path.basename(__file__)      # Name of this file
MY_PATH     = os.path.dirname(os.path.realpath(__file__)) # Path for this file
MY_FILENAME = ME.split(".")[0]
LIBRARY_PATH    = os.path.join(MY_PATH, "../lib")
ADOPS_PATH  = os.path.join(MY_PATH, "../AdOps")
LOG_PATH    = os.path.join(MY_PATH)
LOG_FILE    = ME.replace(".py", ".log")  # filename.log
LOG_FORMAT  = "%(asctime)s, %(levelname)s, %(message)s"
PASSED      = "\033[32mPASSED\033[0m"  #\
WARNING     = "\033[33mWARNING\033[0m" # \___ Linux-specific colorization
FAILED      = "\033[31mFAILED\033[0m"  # /
ERROR       = "\033[31mERROR\033[0m"   #/
PAGE_BUFFER = 8192

# Custom Import
sys.path.append(LIBRARY_PATH)
import functions, FillGoogleSheetWithTestResults
sys.path.append(ADOPS_PATH)
import AdOps_HTML_NMCTagTestFunctions as runTest

# Initialize the logger
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=LOG_FORMAT, filemode="w")
logger = logging.getLogger()
logger.info("Logging Started =================================================")

# Script Specific Variables
expected_pid = "HOMEPAGE"
expected_tag = "SECTIONFRONT,HOMEPAGE"

failed_pid_test = 0
failed_tag_test = 0

pages_passed = 0
pages_failed = 0
total_calls = 0

# URLS - listed in a json file
with open(LIBRARY_PATH + "/migratedStationUrls.json") as file:
    station_urls = json.load(file)

# Body of Script
for url in station_urls:
    tests_passed_for_this_page = 0
    total_calls += 1

    prod_url = url["prod_url"]
    preprod_url = url["preprod_url"]

    # Call for the web page data once and use the data for the tests
    prod_web_page_data = functions.call_url(prod_url)[:PAGE_BUFFER]
    preprod_web_page_data = functions.call_url(preprod_url)[:PAGE_BUFFER]

    ###################################################
    # TEST 1 of 2: Compare HTML nmc:pid with expected
    # nmc:pid should be content=”homepage”
    ###################################################

    # Send web page data to AdOps_HTML_NMCTagTest
    # Check to see if they match the expected value
    # Get back true/false for prod and preprod
    prod_match, preprod_match = runTest.test_nmc_pid(prod_web_page_data, preprod_web_page_data, expected_pid)

    # Check to see if prod and preprod are both true
    status = runTest.do_they_match(prod_match, preprod_match)

    if status == True:
        message = "   TEST 1 of 2: %s\n" % PASSED
        tests_passed_for_this_page += 1
    else:
        message = "   TEST 1 of 2: %s\n" % FAILED
        failed_pid_test += 1
    functions.show_message(message)

    ###################################################
    # TEST 2 of 2: Compare HTML nmc:tag with expected
    # nmc:tag should be content=”sectionfront,homepage”
    ###################################################

    # Send web page data to AdOps_HTML_NMCTagTest
    # Check to see if they match the expected value
    # Get back true/false for prod and preprod
    match1, match2 = runTest.test_nmc_tag(prod_web_page_data, preprod_web_page_data, expected_tag)

    # Check to see if prod and preprod are both true
    status = runTest.do_they_match(match1, match2)
    if status == True:
        message = "   TEST 2 of 2: %s\n" % PASSED
        tests_passed_for_this_page += 1
    else:
        message = "   TEST 2 of 2: %s\n" % FAILED
        failed_tag_test += 1
    functions.show_message(message)

    # Print and tally results before going to the next pair of urls for testing
    print("\n****\nThis station page Passed = %d of 2\n****\n" % tests_passed_for_this_page)
    if tests_passed_for_this_page == 2:
        pages_passed += 1
    else:
        pages_failed += 1

# Printing test results
print("\n\n-------RESULTS----------")
print("%d of %d Stations PASSED" % (pages_passed, total_calls))
print("----------------------------")
print("%d of %d NMC:PID Tests FAILED" % (failed_pid_test, total_calls))
print("%d of %d NMC:TAG Tests FAILED" % (failed_tag_test, total_calls))

# Put pass/fail in the google sheet
FillGoogleSheetWithTestResults.fillMigrationSheet(MY_FILENAME, pages_failed)

# Exit gracefully
sys.exit(0)
