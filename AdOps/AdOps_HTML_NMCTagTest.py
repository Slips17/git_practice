#! /tmp/python3

# -------------------------------------------------------------------------------------------------
# Purpose Statement: This is the script that all the Stage Env AdOps scripts use
# for the body of their testing. It loops through the specific test set of URLs (json file)
# and compares the expected nmc:pid and nmc:tag with the ones on the page.
#
# Original Author: S Lehnert  Created: September 2020
# Updating Author:
# Last Updated:
# -------------------------------------------------------------------------------------------------
# Additional Information (Optional):
#
# -------------------------------------------------------------------------------------------------

import os
import sys
import AdOps_HTML_NMCTagTestFunctions as runTest

MY_PATH     = os.path.dirname(os.path.realpath(__file__)) # Path for this file
LIBRARY_PATH    = os.path.join(MY_PATH, "../lib")
PASSED      = "\033[32mPASSED\033[0m"  #\
WARNING     = "\033[33mWARNING\033[0m" # \___ Linux-specific colorization
FAILED      = "\033[31mFAILED\033[0m"  # /
ERROR       = "\033[31mERROR\033[0m"   #/
PAGE_BUFFER = 8192

sys.path.append(LIBRARY_PATH)
import functions

# ----------------------------------------------------------------------------- singleTest()
def singleTest(page_urls):
    """ This is the test for all the Stage only AdOps NMC Tag verification scripts.
        This function accepts 1 argument: page_urls. This function returns the
        number of pages failed so that the main test script can report to Google Sheets.
    """

    failed_pid_test = 0
    failed_tag_test = 0

    pages_passed = 0
    pages_failed = 0
    total_calls = 0

    for url in page_urls:
        tests_passed_for_this_page = 0
        total_calls += 1

        stg_url = url["url"]
        expected_pid = url["expected_pid"].upper()
        expected_tag = url["expected_tag"].upper()

        # Call for the web page data once and use the data for the tests
        web_page_data = functions.call_url(stg_url)[:PAGE_BUFFER]

        ###################################################
        # TEST 1 of 2: Compare HTML nmc:pid with expected
        ###################################################

        # Send web page data to AdOps_HTML_NMCTagTest
        # Check to see if it matches the expected value
        # Get back true/false
        status = runTest.test_nmc_pid_single(web_page_data, expected_pid)

        if status == True:
            message = "   TEST 1 of 2: %s\n" % PASSED
            tests_passed_for_this_page += 1
        else:
            message = "   TEST 1 of 2: %s\n" % FAILED
            failed_pid_test += 1
        functions.show_message(message)

        ###################################################
        # TEST 2 of 2: Compare HTML nmc:tag with expected
        ###################################################

        # Send web page data to AdOps_HTML_NMCTagTest
        # Check to see if it matches the expected value
        # Get back true/false
        status = runTest.test_nmc_tag_single(web_page_data, expected_tag)

        if status == True:
            message = "   TEST 2 of 2: %s\n" % PASSED
            tests_passed_for_this_page += 1
        else:
            message = "   TEST 2 of 2: %s\n" % FAILED
            failed_tag_test += 1
        functions.show_message(message)

        # Print and tally results before going to the next url for testing
        print("\n****\nThis page Passed = %d of 2\n****\n" % tests_passed_for_this_page)
        if tests_passed_for_this_page == 2:
            pages_passed += 1
        else:
            pages_failed += 1

    # Printing test results
    print("\n\n-------RESULTS----------")
    print("%d of %d pages PASSED" % (pages_passed, total_calls))
    print("----------------------------")
    print("%d of %d NMC:PID Tests FAILED" % (failed_pid_test, total_calls))
    print("%d of %d NMC:TAG Tests FAILED" % (failed_tag_test, total_calls))

    return(pages_failed)
