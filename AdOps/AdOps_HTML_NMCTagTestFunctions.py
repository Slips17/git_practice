#! /tmp/python3

# -------------------------------------------------------------------------------------------------
# Purpose Statement: This is the script of test steps for NMC Tags that specific page scripts will
# call. Since the nmc tags are the same for all AdOps pages and only the expected value is different,
# each page will have a script with the expected value, and will call this script to run the tests.
# This allows for code reuse and removes duplication of effort. Tests are run against prod and
# pre-prod URLs at the same time.
#
# For example: to check the nmc tags on station section front pages...the section front page script
# will run and set the expected values. Then the script will call this script to run the test and
# compare expected with actual results.
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

MY_PATH     = os.path.dirname(os.path.realpath(__file__)) # Path for this file
LIBRARY_PATH    = os.path.join(MY_PATH, "../lib")

sys.path.append(LIBRARY_PATH)
import functions


# ----------------------------------------------------------------------------- test_nmc_tag()
def test_nmc_tag(prod_web_page_data, preprod_web_page_data, expected_tag):
    """ Takes prod_web_page_data, preprod_web_page_data, and an expected_tag.
        The function will find the nmc:tag for each of the prod and preprod web
        pages. Then it will compare that tag with the expected tag. This function
        returns two results: true/false for the prod page and true/false for the
        preprod page.
    """

    # Get the tag from the page. Function returns string in upper case.
    tag_from_html_prod = functions.get_meta_tag_content(prod_web_page_data, "", "nmc:tag")
    tag_from_html_preprod = functions.get_meta_tag_content(preprod_web_page_data, "", "nmc:tag")

    # Compares expected tag with the one found on the page. Response is true if it is a match; false if not.
    print("Checking HTML nmc:tag on PROD")
    isMatch1 = functions.compare(expected_tag, tag_from_html_prod)
    print("Checking HTML nmc:tag on PREPROD")
    isMatch2 = functions.compare(expected_tag, tag_from_html_preprod)

    return isMatch1, isMatch2


# ----------------------------------------------------------------------------- test_nmc_tag_single()
def test_nmc_tag_single(web_page_data, expected_tag):
    """ Takes web_page_data and an expected_tag. The function will find the nmc:tag
        for the web page. Then it will compare that tag with the expected tag.
        This function returns one result: true/false.
    """

    # Get the tag from the page. Function returns string in upper case.
    tag_from_html = functions.get_meta_tag_content(web_page_data, "", "nmc:tag")

    # Compares expected tag with the one found on the page. Response is true if it is a match; false if not.
    print("Checking HTML nmc:tag")
    isMatch = functions.compare(expected_tag, tag_from_html)

    return isMatch


# ----------------------------------------------------------------------------- test_nmc_pid()
def test_nmc_pid(prod_web_page_data, preprod_web_page_data, expected_pid):
    """ Takes prod_web_page_data, preprod_web_page_data, and an expected_pid.
        The function will find the nmc:pid for each of the prod and preprod web
        pages. Then it will compare that pid with the expected pid. This function
        returns two results: true/false for the prod page and true/false for the
        preprod page.
    """

    # Get the pid from the page. Function returns string in upper case.
    pid_from_html_prod = functions.get_meta_tag_content(prod_web_page_data, "", "nmc:pid")
    pid_from_html_preprod = functions.get_meta_tag_content(preprod_web_page_data, "", "nmc:pid")

    # Compares the expected pid with the one found on the page. Response is true if it is a match; false if not.
    print("Checking HTML nmc:pid on PROD")
    isMatch1 = functions.compare(expected_pid, pid_from_html_prod)
    print("Checking HTML nmc:pid on PREPROD")
    isMatch2 = functions.compare(expected_pid, pid_from_html_preprod)

    return isMatch1, isMatch2


# ----------------------------------------------------------------------------- test_nmc_pid_single()
def test_nmc_pid_single(web_page_data, expected_pid):
    """ Takes web_page_data and an expected_pid. The function will find the nmc:pid
        for the web page. Then it will compare that pid with the expected pid.
        This function returns one result: true/false.
    """

    # Get the pid from the page. Function returns string in upper case.
    pid_from_html = functions.get_meta_tag_content(web_page_data, "", "nmc:pid")

    # Compares the expected pid with the one found on the page. Response is true if it is a match; false if not.
    print("Checking HTML nmc:pid")
    isMatch = functions.compare(expected_pid, pid_from_html)

    return isMatch


# ----------------------------------------------------------------------------- do_they_match()
def do_they_match(prod_value, preprod_value):
    """ Takes two boolean values. Assumes the first value is from PROD
        and the second value is from PREPROD. Prints and logs a message
        depending on which is true and which is not. Returns True if both
        values are True. Returns False if either or both are not True.
    """

    # If both values are True, return True. If not, return False. Print and Log a message either way.
    if prod_value and preprod_value == True:
        functions.show_message("Yes! Prod and Preprod are True.")
        return True
    else:
        if prod_value == True:
            functions.show_message("Passed on Prod Only.")
        elif preprod_value == True:
            functions.show_message("Passed on PreProd Only.")
        else:
            functions.show_message("Both Prod and PreProd Failed.")
        return False
