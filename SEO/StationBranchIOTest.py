#! /tmp/python3

# -------------------------------------------------------------------------------------------------
# VERSION: 1.0.0
#
# Purpose Statement: This script contains the base testing for all the SEO Branch IO
# Scripts regaring Station URLs under test. This script checks Station Market, Logo,
# Name, ID,Genre Name, and Category API values. 6 Tests. Returns the total number of
# overall page failures. Does NOT return the number of failures per each test
# run, but DOES print that information to the log and console.
#
# Original Author: S Lehnert  Created: October 2020
# Updating Author:
# Last Updated:
# -------------------------------------------------------------------------------------------------
# Additional Information (Optional):
#
# Acceptance Criteria:
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
# -------------------------------------------------------------------------------------------------

# Standard Library Imports
import os
import sys
import json
import StationBranchIOTagCheck as test

# Variables
MY_PATH     = os.path.dirname(os.path.realpath(__file__)) # Path for this file
LIBRARY_PATH    = os.path.join(MY_PATH, "../lib")
PAGE_BUFFER = 8192 # <-- So we don't waste time loading unimportant data

# Custom library imports
sys.path.append(LIBRARY_PATH)
import functions

# ----------------------------------------------------------------------------- baseTest()
def baseTest(page_urls, html, html2 = ""):
    """ All the Branch IO Test scripts have the same base test set for Station URLs.
        This function tests the Station Market, Logo, Name, ID, Category, and Genre
        Name for a given list of page urls. This function accepts 3 arguments:
        1) The list of page_urls to test
        2) The HTML page under test (example: the article_url or the contest_url)
        3) A second HTML page under test which is optional (example: the script
        for section fronts tests both the primary section front url and the secondary
        section front url at the same time).
    """
    # Counters for tallying test results
    total_calls = 0
    pages_passed = 0
    pages_failed = 0

    marketFail = 0
    logoFail = 0
    nameFail = 0
    idFail = 0
    categoryFail = 0
    genreFail = 0

    # Start a loop to go through the given page_urls list
    for url in page_urls:
        total_calls += 1

        #####################################
        #  API Variable SECTION
        #####################################

        api_url = url["api_url"] # <-- URL is given to us in the page_urls list

        # Get all of the station data from the core API as a list of dictionaries
        station_data_text = functions.call_url(api_url)
        station_data = json.loads(station_data_text)  # <-- List of dictionaries
        station_dictionary = station_data["data"] # <-- We ALWAYS want variables from the data section

        # Set variables for API comparison testing later
        station_id = station_dictionary["id"]
        station_market = station_dictionary["attributes"]["market"]["display_name"]
        station_name = station_dictionary["attributes"]["name"]
        station_logo = station_dictionary["attributes"]["square_logo_small"]

        # Category is a LIST (of ONLY ONE dictionary) that is nested inside of "attributes"
        station_category = station_dictionary["attributes"]["category"]

        # Genre is a LIST (of AT LEAST ONE dictionary) that is nested inside of "attributes"
        station_genre = station_dictionary["attributes"]["genre"]

        # Check if there is more than one dictionary in this list
        # Separate out the genre names from the other dictionary values
        if len(station_genre) > 1:
            message = "Station has more than one genre dictionary in the list!"
            functions.show_message(message)
            list_of_genre_names = []
            for item_dict in station_genre:
                name = item_dict["name"]
                list_of_genre_names.append(name)
            station_genre_name = list_of_genre_names
            print("There is more than one genre name!! API returns: %s" % station_genre_name)
        else:
            station_genre_name = station_genre[0]["name"]

        # If any variables are empty, log them
        station_market = functions.isNoneOrEmpty(station_market, "Station Market")
        station_logo = functions.isNoneOrEmpty(station_logo, "Station Logo")
        station_name = functions.isNoneOrEmpty(station_name, "Station Name")
        station_category = functions.isCategoryOrGenreEmpty(station_category, "Station Category")
        station_genre = functions.isCategoryOrGenreEmpty(station_genre, "Station Genre")
        station_id = functions.isIDEmpty(station_id)

        # Check if Genre Name is a list (the list we made earlier or just a single value)
        # Make uppercase for comparison testing
        if type(station_genre_name) is list:
            message = "The API Genre is a list."
            station_genre_name = [item.upper() for item in station_genre_name]
        else:
            message = "The API Genre is a single value."
            station_genre_name = station_genre_name.upper()
        functions.show_message(message)

        # Check if category (the value not the section) is a list
        # Make uppercase for comparison testing
        if type(station_category) is list:
            message = "The API Category is a list."
            station_category = [item.upper() for item in station_category]
        else:
            message = "The API Category is a single value."
            station_category = station_category.upper()
        functions.show_message(message)


        #####################################
        #  HTML Variable SECTION
        #####################################

        html_url1 = url[html] # <-- URL is given to us in the page_urls list
        url1_web_page_data = functions.call_url(html_url1)[:PAGE_BUFFER]

        # Some scripts have 2 HTML URLs to verify against. Some have only one.
        if html2 != "":
            html_url2 = url[html2]
            url2_web_page_data = functions.call_url(html_url2)[:PAGE_BUFFER]
        else:
            url2_web_page_data = ""


        #####################################
        #  TEST SECTION
        #####################################

        # Tests with 1 HTML URL
        if url2_web_page_data == "":
            market_test = test.runTagCheck(station_market, url1_web_page_data, "branch:deeplink:market")
            logo_test = test.runTagCheck(station_logo, url1_web_page_data, "branch:deeplink:station_logo")
            name_test = test.runTagCheck(station_name, url1_web_page_data, "branch:deeplink:station_name")
            id_test = test.runTagCheck(str(station_id), url1_web_page_data, "branch:deeplink:station_id")
            # If there is a list of categories to compare against
            if type(station_category) is list:
                category_test = test.runTagListCheck(station_category, url1_web_page_data, "branch:deeplink:category")
            elif type(station_category) is str:
                category_test = test.runTagCheck(station_category, url1_web_page_data, "branch:deeplink:category")
            # If there is a list of genre names to compare against
            if type(station_genre_name) is list:
                genre_test = test.runTagListCheck(station_genre_name, url1_web_page_data, "branch:deeplink:genre")
            elif type(station_genre_name) is str:
                genre_test = test.runTagCheck(station_genre_name, url1_web_page_data, "branch:deeplink:genre")

        # Tests with 2 HTML URLs
        else:
            market_test = test.runTagCheckDouble(station_market, url1_web_page_data, url2_web_page_data, "branch:deeplink:market")
            logo_test = test.runTagCheckDouble(station_logo, url1_web_page_data, url2_web_page_data, "branch:deeplink:station_logo")
            name_test = test.runTagCheckDouble(station_name, url1_web_page_data, url2_web_page_data, "branch:deeplink:station_name")
            id_test = test.runTagCheckDouble(str(station_id), url1_web_page_data, url2_web_page_data, "branch:deeplink:station_id")
            # If there is a list of genre names to compare against
            if type(station_category) is list:
                category_test = test.runTagListCheckDouble(station_category, url1_web_page_data, url2_web_page_data, "branch:deeplink:category")
            elif type(station_category) is str:
                category_test = test.runTagCheckDouble(station_category, url1_web_page_data, url2_web_page_data, "branch:deeplink:category")
            # If there is a list of genre names to compare against
            if type(station_genre_name) is list:
                genre_test = test.runTagListCheckDouble(station_genre_name, url1_web_page_data, url2_web_page_data, "branch:deeplink:genre")
            elif type(station_genre_name) is str:
                genre_test = test.runTagCheckDouble(station_genre_name, url1_web_page_data, url2_web_page_data, "branch:deeplink:genre")

        #####################################
        #  TEST RESULTS SECTION
        #####################################

        # Counter for how many of the 6 tests that this set of urls failed
        urlFailCount = 0

        # Check if all are truthy
        if market_test and logo_test and name_test and id_test and category_test and genre_test:
            message = "\nAll tests passed for this URL set.\n\n"
            pages_passed += 1
        # If at least one is not True, gotta count what failed and how many of them
        else:
            pages_failed += 1  # <-- Increment the overall/total URL Failure count
            if market_test == False:
                urlFailCount += 1
                marketFail += 1
            if logo_test == False:
                urlFailCount += 1
                logoFail += 1
            if name_test == False:
                urlFailCount += 1
                nameFail += 1
            if id_test == False:
                urlFailCount += 1
                idFail += 1
            if category_test == False:
                urlFailCount += 1
                categoryFail += 1
            if genre_test == False:
                urlFailCount += 1
                genreFail += 1

        # Print and tally results before going to the next url for testing
        message = "\n%d of 6 Tests Failed!!\n\n" % urlFailCount
        functions.show_message(message)

    # Finally outside the for loop
    # Printing test results
    print("\n-------STATION BASE TEST RESULTS----------")
    print("%d of %d Total Calls PASSED" % (pages_passed, total_calls))
    print("----------------------------")
    print("%d of %d Market Tests FAILED" % (marketFail, total_calls))
    print("%d of %d Logo Tests FAILED" % (logoFail, total_calls))
    print("%d of %d Name Tests FAILED" % (nameFail, total_calls))
    print("%d of %d ID Tests FAILED" % (idFail, total_calls))
    print("%d of %d Category Tests FAILED" % (categoryFail, total_calls))
    print("%d of %d Genre Name Tests FAILED" % (genreFail, total_calls))
    print("-------STATION BASE TEST RESULTS----------\n\n")

    # Return how many total URL failures there were
    return pages_failed
