#! /tmp/python3

# -------------------------------------------------------------------------------------------------
# VERSION: 2.0
#
# Purpose Statement: Verify podcast show detail page description values
# JIRA Ticket Link:
#
# Original Author: S Lehnert  Created: July 2020
# Updating Author: S Lehnert  Updated: November 2020
# Updating Author: S Lehnert  Updated: March 2021
# Updating Author:
# Last Updated:
# -------------------------------------------------------------------------------------------------
# Additional Information (Optional):
# Testing STATION Show Detail pages ONLY! 3 are currently specified.
#
# Acceptance Criteria:
# Match expected API description with: HTML <description>, twitter:description,
# and og:description
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

# Variables
total_calls = 0
failed_test = 0

# URLs
# No JSON file needed - this is the only script using these URLs
podcast_urls = [
    {
        # Station: sanitized  callsign:  sanitized
        "api_url" : "sanitized",
        "html_url" : "sanitized",
    },
    {
        # Station: sanitized  callsign:  sanitized
        "api_url" : "sanitized",
        "html_url" : "sanitized",
    },
    {
        # Station: sanitized callsign: sanitized
        "api_url": "sanitized",
        "html_url": "sanitized",
    }
]

# Check each of the URLs above and test
for url in podcast_urls:
    total_calls += 1

    api_url = url["api_url"]
    html_url = url["html_url"]

    # Get the API data
    podcast_data_text = functions.call_url(api_url)
    podcast_data = json.loads(podcast_data_text)
    # Get the web page data
    page_data = functions.call_url(html_url)[:PAGE_BUFFER]

    # API description is the expected description for the test
    expected_description = podcast_data["data"]["attributes"]["description"]

    # If the API doesn't have a description - log it
    expected_description = functions.isNoneOrEmpty(expected_description, "Podcast API Description")

    # Get the tag content values from the HTML page
    description         = functions.get_meta_tag_content(page_data, "", "description")
    og_description      = functions.get_meta_tag_content(page_data, "og:description")
    twitter_description = functions.get_meta_tag_content(page_data, "", "twitter:description")

    # Set value to empty string if value is ${PARAMVALUE}
    og_description      = functions.check_for_empty(og_description)
    twitter_description = functions.check_for_empty(twitter_description)
    description         = functions.check_for_empty(description)

    # Print something easy to see in the console
    print("      Looking for     : '%s'" % expected_description)
    print("      OG Found        : '%s'" % og_description)
    print("      Twitter Found   : '%s'" % twitter_description)
    print("      HTML Desc Found : '%s'" % description)

    # If all match, then Pass. Else fail.
    if expected_description == og_description and \
            expected_description == twitter_description and \
            expected_description == description:
        message = "   Station Podcast Show Detail description: %s\n" % PASSED
    else:
        message = "   Station Podcast Show Detail description: %s\n" % FAILED
        failed_test += 1

    functions.show_message(message)

print("=======STATION PODCAST SHOW DETAIL PAGE RESULTS=======")
print("%d of %d Descriptions FAILED" % (failed_test, total_calls))
print("=====END STATION PODCAST SHOW DETAIL PAGE RESULTS=====\n\n")

FillGoogleSheetWithTestResults.fillSheet(MY_FILENAME, failed_test)

sys.exit(0)
