#! /tmp/python3

# -------------------------------------------------------------------------------------------------
# VERSION: 1.0.0
#
# Purpose Statement: This script checks for matching API and HTML content values for
# given tags on given pages. There are 4 functions:
# 1) Comparing single property values using a single html web page data source
# 2) Comparing single property values using two html web page data sources
# 3) Comparing a list of property values using a single html web page data source
# 4) Comparing a list of property values using two html web page data sources
# If the API property value matches the HTML property value(s), the function returns
# True. Else the function returns false.
#
# Original Author: S Lehnert  Created: October 2020
# Updating Author:
# Last Updated:
# -------------------------------------------------------------------------------------------------
# Additional Information (Optional):
# These functions do not check for <meta property= in the html source. They only check
# the <meta name= values at this time (Oct 2020).
#
# -------------------------------------------------------------------------------------------------

# Standard Library Imports
import os
import sys

# Variables
MY_PATH     = os.path.dirname(os.path.realpath(__file__)) # Path for this file
LIBRARY_PATH    = os.path.join(MY_PATH, "../lib")
PASSED      = "\033[32mPASSED\033[0m"  #\
WARNING     = "\033[33mWARNING\033[0m" # \___ Linux-specific colorization
FAILED      = "\033[31mFAILED\033[0m"  # /
ERROR       = "\033[31mERROR\033[0m"   #/

# Custom library imports
sys.path.append(LIBRARY_PATH)
import functions


# ----------------------------------------------------------------------------- runTagCheck()
def runTagCheck(api_value, web_page_data, tag):
    """ Using the provided web page data source, find the content for the tag.
        Then compare that content value with the expected api value. Return True
        or False. This function expects a single content value and a single web
        page data source. Use runTagListCheck if expecting multiple content
        values (in a list). Use runTagCheckDouble if there are two web page data
        sources but only one content value. Use runTagListCheckDouble if there
        are two web page data sources AND content values are in a list.
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


# ----------------------------------------------------------------------------- runTagListCheck()
def runTagListCheck(api_value, web_page_data, tag):
    """ Using the provided web page data source, find the listed content for the
        tag. Then compare that listed value with the expected api listed value.
        Return True or False. This function expects a list of content values and
        a single web page data source. Use runTagCheck if expecting only one
        content value and one web page data source. Use runTagCheckDouble if
        there are two web page data sources but only one content value. Use
        runTagListCheckDouble if there are two web page data sources AND content
        values are in a list.
    """

    # Function returns string in upper case
    branch_io_tag_from_html_url = functions.get_meta_tag_content_list(web_page_data, "", tag)

    # Comparison time
    match = functions.compare(api_value, branch_io_tag_from_html_url)

    if match == True:
        message = "   TEST for %s: %s\n" % (tag, PASSED)
    else:
        message = "   TEST for %s: %s\n" % (tag, FAILED)
    functions.show_message(message)

    return match


# ----------------------------------------------------------------------------- runTagCheckDouble()
def runTagCheckDouble(api_value, web_page_data1, web_page_data2, tag):
    """ Using the provided web page data sources, find the content for the tag.
        Then compare the content values with the expected api value. Return True
        or False. This function expects a content value and a two web page data
        sources. Use runTagCheck if expecting only one content value and one web
        page data source. Use runTagListCheck if expecting multiple content
        values (in a list). Use runTagListCheckDouble if there are two web page
        data sources AND content values are in a list.
    """

    # Function returns string in upper case
    branch_io_tag_from_html_url1 = functions.get_meta_tag_content(web_page_data1, "", tag)
    branch_io_tag_from_html_url2 = functions.get_meta_tag_content(web_page_data2, "", tag)

    # Comparison time
    match1 = functions.compare(api_value, branch_io_tag_from_html_url1)
    match2 = functions.compare(api_value, branch_io_tag_from_html_url2)

    if match1 == True and match2 == True:
        message = "   TEST for %s: %s\n" % (tag, PASSED)
        functions.show_message(message)
        return True
    else:
        message = "   TEST for %s: %s\n" % (tag, FAILED)
        functions.show_message(message)
        return False


# ----------------------------------------------------------------------------- runTagListCheckDouble()
def runTagListCheckDouble(api_value, web_page_data1, web_page_data2, tag):
    """ Using the provided web page data sources, find the listed content for
        the tag. Then compare the listed values with the expected api value.
        Return True or False. This function expects a list of content values and
        a two web page data sources. Use runTagCheck if expecting only one
        content value and one web page data source. Use runTagListCheck if
        expecting multiple content values (in a list). Use runTagCheckDouble if
        there are two web page data sources but only one content value.
    """

    # Function returns string in upper case
    branch_io_tag_from_html_url1 = functions.get_meta_tag_content_list(web_page_data1, "", tag)
    branch_io_tag_from_html_url2 = functions.get_meta_tag_content_list(web_page_data2, "", tag)

    # Comparison time
    match1 = functions.compare(api_value, branch_io_tag_from_html_url1)
    match2 = functions.compare(api_value, branch_io_tag_from_html_url2)

    if match1 == True and match2 == True:
        message = "   TEST for %s: %s\n" % (tag, PASSED)
        functions.show_message(message)
        return True
    else:
        message = "   TEST for %s: %s\n" % (tag, FAILED)
        functions.show_message(message)
        return False
