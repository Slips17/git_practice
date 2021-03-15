#! /tmp/python3

# -------------------------------------------------------------------------------------------------
# VERSION: 1.0.0
#
# Purpose Statement: This script contains the base testing for all the SEO Branch IO
# Scripts regaring the National URLs under test. For the moment (Oct 2020),
# only the station_name is being checked. This script will grow as other HTML tags
# require verifications in the future.
#
# Original Author: S Lehnert  Created: October 2020
# Updating Author:
# Last Updated:
# -------------------------------------------------------------------------------------------------
# Additional Information (Optional):
#
# Acceptance Criteria:
# station_name = "sanitized-url"
#
# -------------------------------------------------------------------------------------------------

# Standard Library Imports
import os
import sys
import json
import StationBranchIOTagCheck as test

# Variables
MY_PATH     = os.path.dirname(os.path.realpath(__file__)) # Path for this file
LIBRARY_PATH    = os.path.join(MY_PATH, "../lib")
PAGE_BUFFER = 8192

# Custom library imports
sys.path.append(LIBRARY_PATH)
import functions

# ----------------------------------------------------------------------------- baseTest()
def NationalBaseTest(page_urls, html, html2 = ""):
    """ All the Branch IO Test scripts have the same base test set for National.
        This function tests the Station Name for a given list of page urls. This
        function accepts 3 arguments:
        1) The list of page_urls to test
        2) The HTML page under test (example: the article_url or the contest_url)
        3) A second HTML page under test which is optional (example: the script
        for section fronts tests both the primary section front url and the secondary
        section front url at the same time).
    """
    # Expected Station Name (National pages do not have an API to pull this from)
    station_name = "sanitized-url"

    # Counters for tallying test results
    total_calls = 0
    failed_national_calls = 0

    # Start a loop to go through the given page_urls list
    for url in page_urls:
        total_calls += 1

        html_url1 = url[html] # <-- URL is given to us in the page_urls list
        url1_page_data = functions.call_url(html_url1)[:PAGE_BUFFER]

        # Some scripts have 2 HTML URLs to verify against. Some have only one.
        if html2 != "":
            html_url2 = url[html2]
            url2_page_data = functions.call_url(html_url2)[:PAGE_BUFFER]
            status = test.runTagCheckDouble(station_name, url1_page_data, url2_page_data, "branch:deeplink:station_name")
        else:
            status = test.runTagCheck(station_name, url1_page_data, "branch:deeplink:station_name")

        if status == False:
            failed_national_calls += 1

    # Printing test results
    print("\n-------NATIONAL BASE TEST RESULTS----------")
    print("Total National Calls Failed: %d of %d" % (failed_national_calls, total_calls))

    # Return how many total URL failures there were
    return failed_national_calls
