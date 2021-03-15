#! /tmp/python3

# -------------------------------------------------------------------------------------------------
# Purpose Statement:
# JIRA Ticket Link (if applicable):
#
# Original Author: S Lehnert  Created: September 2020
# Updating Author:
# Last Updated:
# -------------------------------------------------------------------------------------------------
# Additional Information (Optional):
#  This script is checking Event Pages
#
# Acceptance Criteria:
# 1) nmc:pid should be content=”events_<headline>"
# 2) nmc:tag should be content=”events”
#
# -------------------------------------------------------------------------------------------------

# Imports
import json
import os
import sys
import logging
import AdOps_HTML_NMCTagTest as NMCTest

# Variables
ME          = os.path.basename(__file__)      # Name of this file
MY_PATH     = os.path.dirname(os.path.realpath(__file__)) # Path for this file
MY_FILENAME = ME.split(".")[0]
LIBRARY_PATH    = os.path.join(MY_PATH, "../lib")
LOG_PATH    = os.path.join(MY_PATH)
LOG_FILE    = ME.replace(".py", ".log")  # filename.log
LOG_FORMAT  = "%(asctime)s, %(levelname)s, %(message)s"

# Custom Import
sys.path.append(LIBRARY_PATH)
import functions, FillGoogleSheetWithTestResults

# Initialize the logger
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=LOG_FORMAT, filemode="w")
logger = logging.getLogger()
logger.info("Logging Started =================================================")

# URLS - listed in a json file
with open(LIBRARY_PATH + "/eventURLs.json") as file:
    event_urls = json.load(file)

# Run the test with the URLs - get the number of pages failed.
pages_failed = NMCTest.singleTest(event_urls)
print("Pages failed: " + str(pages_failed))

# Put pass/fail in the google sheet
FillGoogleSheetWithTestResults.fillSheet(MY_FILENAME, pages_failed)

# Exit gracefully
sys.exit(0)
