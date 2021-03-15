#! /tmp/python3

# -------------------------------------------------------------------------------------------------
# VERSION: 2.0
#
# Purpose Statement:
# JIRA Ticket Link (if applicable):
#
# Original Author: S Lehnert  Created: June 2020
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
# 1) STATION Primary Section Front and Secondary Section Front pages:
# Branch IO HTML meta tags should match the Station API
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
# 2) NATIONAL Section Front pages:
#    A) Should definitely have the station_name Branch IO HTML meta tag
#    B) The value should be `sanitized'
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
# that all Branch IO scripts call.
#----------------------------------------------

# Call the Base Branch IO Test to check Station Market, Logo, Name, ID,
# Genre Name, and Category API values. 6 Tests. Returns the total number of
# overall page failures. Does NOT return the number of failures per each test
# run, but DOES print that information to the log and console.

# We only want to test the primary and secondary section front urls from the json file
failures = StationBranchIOTest.baseTest(station_urls, "psf_url", "ssf_url")


######################################
# Testing the National URLs
######################################

# Call the Base Branch IO Test to check Station Name. 1 Test. Returns total
# number of overall page failures. Expecting station_name = sanitized

# We only want to test the primary and secondary section front urls from the json file
failed_national_calls = NationalBranchIOTest.NationalBaseTest(national_page_urls,"psf_url", "ssf_url")


##############################################
# Print results and report to GoogleSheets
##############################################

print("\n-------SECTION FRONT TEST RESULTS----------")
print("Part 1 Station: %d of %d FAILED" % (failures, len(station_urls)))
print("Part 2 National: %d of %d FAILED" % (failed_national_calls, len(national_page_urls)))
print("-------SECTION FRONT TEST RESULTS----------\n\n")

total_failed = failures + failed_national_calls
FillGoogleSheetWithTestResults.fillSheet(MY_FILENAME, total_failed)

sys.exit(0)
