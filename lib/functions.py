#! /tmp/python3

# -------------------------------------------------------------------------------------------------
# VERSION: 1.1
#
# Purpose Statement: This script is called by other scripts to limit copy/paste of regularly
# used functions.
#
# Original Author: S Lehnert  Created: August 2020
# Updating Author: S Lehnert  Updated: October 2020
# Updating Author:
# Last Updated:
#
# -------------------------------------------------------------------------------------------------


# Standard Library Imports
import logging
import requests
from bs4 import BeautifulSoup


# === Regularly Used Functions - in Alphabetical order ===============
# ----------------------------------------------------------------------------- adjust_api_carriage_returns()
def adjust_api_carriage_returns(data_string):
    """ If the API string contains \r\n, HTML only recognizes them as \n. So the
        tests fail. This function adjusts the API strings that contain \r\n so
        that they only have \n for better HTML comparisons.
    """
    if "\r\n" in data_string:
        data_string = data_string.replace("\r\n", "\n")
    return data_string


# ----------------------------------------------------------------------------- call_url()
def call_url(url):
    """ Call a url and return the text response from the call.
        If there are any problems, then return an error.
    """
    show_message("   Calling: %s" % url)
    response_object = requests.get(url, timeout=30) #time out if 30 seconds passes with no response
    code = response_object.status_code

    if code != 200:
        show_message("   Failed. Call returned %d" % code)
    else:
        show_message("   Success, Call returned 200")
    # Return the text response from the call
    return response_object.text


# ----------------------------------------------------------------------------- checkBSValue()
def checkBSValue(item):
    """ If Beautiful Soup's find() is unable to find anything, it returns a None
        value. If the result is not a None or empty string, this function will
        capitalize the resulting value. If the result is None or an empty string,
        this function will just return an empty string.
    """

    if item is None or item == "":
        value = ""
    else:
        value = item["content"].upper()
    return value


# ----------------------------------------------------------------------------- check_for_empty()
def check_for_empty(parm):
    """ Returns empty string if value is ${PARAMVALUE}
    """
    if parm == "${PARAMVALUE}":
        parm = ""
        print("      ${PARAMVALUE} is being converted to empty")
    return parm


# ----------------------------------------------------------------------------- compare()
def compare(api, html):
    """ This function prints out the expected vs actual results, compares the
        two, and returns True if they match. Returns False if they do not match.
    """

    print("      API - Expected    : '%s'" % api)
    print("      Tag - Found       : '%s'" % html)

    if api == html:
        return True
    else:
        return False


# ----------------------------------------------------------------------------- get_meta_tag_content()
def get_meta_tag_content(page_data, property="", name=""):
    """ Parse out the HTML text or content values and return the search results.
        This function only returns results for the FIRST value found on the page.
        This function takes in arguments for page_data, the property search value,
        and the name search value in that order. Use function
        get_meta_tag_content_list if your results should be a list of values.
    """

    # Take the data, parse it, save it to variable
    soup = BeautifulSoup(page_data, "html.parser")

    if property != "":
        property_item = soup.find(attrs={"property" : property})
        value = checkBSValue(property_item)
    else:
        name_item = soup.find(attrs={"name": name})
        value = checkBSValue(name_item)

    return value


# ----------------------------------------------------------------------------- get_meta_tag_content_list()
# TODO: Coming soon - probably - nothing to test this against right now
def get_meta_tag_content_list(page_data, property="", name=""):
    """ Parse out HTML text or content values and return search results.
        This returns a LIST of values found on the page. Use function
        get_meta_tag_content if your results should be a single value.
    """

    # Take the data, parse it, save it to variable
    soup = BeautifulSoup(page_data, "html.parser")
    list_of_content_values = []

    # Search for all meta tags with desired property
    if property != "":
        list_of_properties = soup.find_all(attrs={"property" : property})
        for item in list_of_properties:
            value = item["content"].upper()
            list_of_content_values.append(value)
    # Search for all meta tags with desired name
    else:
        list_of_names = soup.find_all(attrs={"name" : name})
        for item in list_of_names:
            value = item["content"].upper()
            list_of_content_values.append(value)

    return list_of_content_values


# ----------------------------------------------------------------------------- get_title()
def get_title(page_data):
    """ Use Beautiful Soup to parse HTML data and find the title text.
    """

    # Take the page data, parse it, save it to variable
    soup = BeautifulSoup(page_data, "html.parser")
    # Find the first (should be "only") title tag in the HTML and get the text inside the tag
    title = soup.find("title").get_text()
    title = title.upper()
    return title


# ----------------------------------------------------------------------------- isCategoryOrGenreEmpty()
def isCategoryOrGenreEmpty(value, descriptor):
    """ If the Station Category API value or the Genre Name API value is None
        or an empty string, log an info message and return an empty string. Else;
        return the original value.
    """
    if value is None:
        message = "API %s is of type None." % descriptor
        show_message(message)
        value = ""
    elif value == "":
        message = "The API %s is an empty string." % descriptor
        show_message(message)
    else:
        value = adjust_api_carriage_returns(value)

    return value


# ----------------------------------------------------------------------------- isIDEmpty()
def isIDEmpty(IDValue):
    """ If the Station ID API value is None or an empty string, log an
        info message and return an empty string. Else; return the original value.
    """
    if IDValue is None:
        message = "API Station ID is of type None"
        show_message(message)
        IDValue = ""
    elif IDValue == "":
        message = "The API Station ID is an empty string."
        show_message(message)

    return IDValue


# ----------------------------------------------------------------------------- isNoneOrEmpty()
def isNoneOrEmpty(param, descriptor):
    """ If parameter is None or an empty string, log an info message and return
        an empty string. Else; return the original param value.
    """

    if param is None:  # <---  some API data is returning None
        message = "API %s is of type None" % descriptor
        show_message(message)
        return ""
    elif param == "":
        message = "The API %s is an empty string." % descriptor
        show_message(message)
        return ""
    else:
        param = adjust_api_carriage_returns(param)
        param = param.upper()
        return param


# ----------------------------------------------------------------------------- show_message()
def show_message(message):
    """ Log a message and print it to the console output
    """
    logging.getLogger().info(message)
    print(message)
