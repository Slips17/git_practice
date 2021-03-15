#! /tmp/python3

# -------------------------------------------------------------------------------------------------
# VERSION: 2.0
#
# Purpose Statement:
# JIRA Ticket Link (if applicable):
#
# Original Author: S Lehnert  Created: July 2020
# Updating Author: S Lehnert  Updated: October 2020
# Updating Author:
# Last Updated:
# -------------------------------------------------------------------------------------------------
# Additional Information (Optional):
# GRAB SOME PODCASTS AND VERIFY
# For station urls - different script checks national urls
#
# Acceptance Criteria:
# 1) Match the Podcast API information with the HTML meta tags
#    API               | |    HTML
#    ---               | |    ----
#    EPISODE TYPE      | |    PODCAST TYPE
#    PODCAST TITLE     | |    PODCAST NAME
#    PODCAST ID        | |    PODCAST ID
#    EPISODE ID        | |    EPISODE ID
#    EPISODE TITLE     | |    EPISODE TITLE
#    CATEGORY NAME     | |    PODCAST CATEGORY
#    PODCAST IMAGE     | |    PODCAST LOGO
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


# ----- Here Be Functions! Arr! -----
# ----------------------------------------------------------------------------- get_station_site_slug()
def get_station_site_slug(station_call_sign):
    """ Call the station api with the callsign and get the corresponding station
        site slug.
    """
    for station_dictionary in station_data["data"]:
        callsign = station_dictionary["attributes"]["callsign"]
        if callsign == station_call_sign:
            return_value = station_dictionary["attributes"]["site_slug"]
            return return_value


# ----------------------------------------------------------------------------- runTagCheck()
def runTagCheck(api_value, web_page_data, tag):
    """ Using the provided web page data source, find the content for the tag.
        Then compare that content value with the expected api value. Return True
        or False. This function expects a single content value and a single web
        page data source. Use runTagListCheck if expecting multiple content
        values (in a list).
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
        content value and one web page data source.
    """
    # Function returns list in upper case
    branch_io_tag_from_html_url = functions.get_meta_tag_content_list(web_page_data, "", tag)
    # Comparison time
    match = functions.compare(api_value, branch_io_tag_from_html_url)

    if match == True:
        message = "   TEST for %s: %s\n" % (tag, PASSED)
    else:
        message = "   TEST for %s: %s\n" % (tag, FAILED)
    functions.show_message(message)

    return match


# ----------------------------------------------------------------------------- checkEpisodePodcastList()
def checkEpisodePodcastList(list):
    """ If the Episode Podcast List has more than 1 dictionary, this function
        will iterate through and create a list for podcast_title,podcast_id, and
        categories_list. If it has only 1 dictionary, this function will get the
        single value for podcast_title, podcast_id, and categories_list. This
        function returns podcast_title, podcast_id, and categories_list.
    """
    # If there is more than 1 dictionary in this list...
    if len(list) > 1:
        message = "Podcast has more than one dictionary in the list!"
        functions.show_message(message)
        list_of_podcast_titles = []
        list_of_podcast_ids = []
        list_of_categories = []
        for item_dict in episode_podcast_list: # <-- iterate through
            title    = item_dict["title"]
            id       = item_dict["id"]
            category = item_dict["categories"]
            list_of_podcast_titles.append(title)
            list_of_podcast_ids.append(id)
            list_of_categories.append(category)
        podcast_title   = list_of_podcast_titles
        podcast_id      = list_of_podcast_ids
        categories_list = list_of_categories
    else:
        podcast_title   = episode_podcast_list[0]["title"]
        podcast_id      = episode_podcast_list[0]["id"]
        categories_list = episode_podcast_list[0]["categories"]

    return podcast_title, podcast_id, categories_list


# ----------------------------------------------------------------------------- checkCategoryName()
def checkCategoryList(list):
    """ If there is more than 1 dictionary in the categories_list, this function
        will iterate through and put all the category names into a new list. if
        there is only 1 dictionary, this function will get the category name out
        of it. This function returns category_name.
    """
    # **********************************************************************
    # This will be used in test 6 - if code is ever adjusted to handle more
    # than one category
    # **********************************************************************
    if len(list) > 1:
        message = "Categories has more than one dictionary in the list!"
        functions.show_message(message)
        list_of_category_names = []
        for item_dict in categories_list: # <-- iterate through
            name = item_dict["name"].upper()
            list_of_category_names.append(name)
        category_name = list_of_category_names # <-- FYI variable not in use yet
    else:
        category_name = categories_list[0]["name"].upper() # <-- FYI not in use yet

    return category_name



# URLs
with open(LIBRARY_PATH + "/podcast_episode_urls.json") as file:
    podcast_urls = json.load(file)

# Variables
failed_type = 0
failed_podcast_title = 0
failed_podcast_id = 0
failed_episode_id = 0
failed_episode_title = 0
failed_category_name = 0
failed_podcast_logo = 0

podcasts_passed = 0
podcasts_failed = 0
total_calls = 0

# Loop through each set of URL's in the JSON file
for url in podcast_urls:
    total_calls += 1
    tests_passed_for_this_page = 0

    podcast_api_url = url["podcast_api_url"]
    episode_api_url = url["episode_api_url"]
    html_url        = url["html_url"]

    # Get all of the Podcast Episode page and Show page data
    episode_data_text = functions.call_url(episode_api_url)
    episode_data      = json.loads(episode_data_text)
    podcast_data_text = functions.call_url(podcast_api_url)
    podcast_data      = json.loads(podcast_data_text)

    # ------------------
    # Variables Section
    # ------------------

    # Episode Page Variables
    episode_dictionary = episode_data["data"]
    episode_type         = episode_dictionary["type"]
    episode_id           = episode_dictionary["id"]
    episode_title        = episode_dictionary["attributes"]["title"]
    episode_podcast_list = episode_dictionary["attributes"]["podcast"] # <-- this is a list of dictionaries

    podcast_title, podcast_id, categories_list = checkEpisodePodcastList(episode_podcast_list)

    # Podcast Show Page Variables
    podcast_dictionary    = podcast_data["data"]
    podcast_logo          = podcast_dictionary["attributes"]["image"]
    podcast_category_list = podcast_dictionary["attributes"]["category"]
    podcast_category_name = podcast_category_list[0]["name"] # TODO fix this after category issue is addressed

    # Call Podcast Episode Page
    page_data = functions.call_url(html_url)[:PAGE_BUFFER]

    # -------------------------------------------------------------
    # Check if the variables are null/None/empty
    # Set them to empty strings for comparison if they are
    # -------------------------------------------------------------
    podcast_id            = functions.isIDEmpty(podcast_id)
    episode_id            = functions.isIDEmpty(episode_id)
    episode_type          = functions.isNoneOrEmpty(episode_type, "Episode Type")
    podcast_title         = functions.isNoneOrEmpty(podcast_title, "Podcast Title")
    episode_title         = functions.isNoneOrEmpty(episode_title, "Episode Title")
    podcast_logo          = functions.isNoneOrEmpty(podcast_logo, "Podcast Logo")
    podcast_category_name = functions.isNoneOrEmpty(podcast_category_name, "Podcast Category Name")

    # -------------
    # Test Section
    # -------------

    # -------------------------------------------------------------
    # Test 1 of 7: Compare API Type with HTML Type
    # -------------------------------------------------------------
    print("   TEST 1 of 7: Type Check")
    episode_type_test = runTagCheck(episode_type, page_data, "branch:deeplink:podcast_type")
    if episode_type_test == False:
        failed_type += 1

    # -------------------------------------------------------------
    # Test 2 of 7: Compare API Podcast Title with HTML Podcast Title
    # -------------------------------------------------------------
    print("   TEST 2 of 7: Podcast Title Check")
    # If there is a list of categories to compare against
    if type(podcast_title) is list:
        podcast_title_test = runTagListCheck(podcast_title, page_data, "branch:deeplink:podcast_name")
    else:
        podcast_title_test = runTagCheck(podcast_title, page_data, "branch:deeplink:podcast_name")

    if podcast_title_test == False:
        failed_podcast_title += 1

    # -------------------------------------------------------------
    # Test 3 of 7: Compare API Podcast ID with HTML Podcast ID
    # -------------------------------------------------------------
    print("   TEST 3 of 7: Podcast ID Check")
    if type(podcast_id) is list:
        podcast_id_test = runTagListCheck(podcast_id, page_data, "branch:deeplink:podcast_id")
    else:
        podcast_id_test = runTagCheck(str(podcast_id), page_data, "branch:deeplink:podcast_id")

    if podcast_id_test == False:
        failed_podcast_id += 1

    # -------------------------------------------------------------
    # Test 4 of 7: Compare API Episode ID with HTML Episode ID
    # -------------------------------------------------------------
    print("   TEST 4 of 7: Episode ID Check")
    epidsode_id_test = runTagCheck(str(episode_id), page_data, "branch:deeplink:episode_id")
    if epidsode_id_test == False:
        failed_episode_id += 1

    # -------------------------------------------------------------
    # Test 5 of 7: Compare API Episode Title with HTML Episode Title
    # -------------------------------------------------------------
    print("   TEST 5 of 7: Episode Title Check")
    episode_title_test = runTagCheck(episode_title, page_data, "branch:deeplink:episode_title")
    if episode_title_test == False:
        failed_episode_title += 1

    # -------------------------------------------------------------
    # Test 6 of 7: Compare API Podcast Category with HTML Podcast Category
    # -------------------------------------------------------------

    #-------------------------------------------------------------------------------------------
    # Note: This section is a bit complicated.
    # Categories is a list of dictionaries within the podcast list of dictionaries
    # The HTML branch io tag is not pulling from the episodes api call but
    # are actually pulling from the podcasts api call.
    # The HTML branch io tag only reports the first category_name, ignoring others in the list.
    # So we need to verify that the FIRST category_name in the podcast api call
    # matches the HTML branch io tag until a list of categories is added to the HTML.
    # Once this is addressed in a new ticket...this code will have to be adjusted accordingly.
    # TODO change the test to point to "category_name" after category issue is addressed.
    # Don't forget to add the if/else check for a list!
    #--------------------------------------------------------------------------------------------
    print("   TEST 6 of 7: Podcast Category Check")
    # For now we're using the Podcast Category Name
    # category_name = checkCategoryList(categories_list)

    # the "?" is because there currently isn't a tag to look up for this
    # if type(category_name) is list:
    #     category_name_test = runTagListCheck(category_name, page_data, "?")
    # else:
    #     category_name_test = runTagCheck(category_name, page_data, "?")

    category_name_test = runTagCheck(podcast_category_name, page_data, "branch:deeplink:podcast_category")
    if category_name_test == False:
        failed_category_name += 1

    # -------------------------------------------------------------
    # Test 7 of 7: Compare API Podcast Image with HTML Podcast Logo
    # -------------------------------------------------------------
    print("   TEST 7 of 7: Podcast Image Check")
    podcast_logo_test = runTagCheck(podcast_logo, page_data, "branch:deeplink:podcast_logo")
    if podcast_logo_test == False:
        failed_podcast_logo += 1


    # ----------------------
    #  TEST RESULTS SECTION
    # ----------------------

    # Check if all the tests are truthy
    if episode_type_test and podcast_title_test and podcast_id_test and \
            epidsode_id_test and episode_title_test and category_name_test \
            and podcast_logo_test:
        podcast_result = PASSED
        podcasts_passed += 1
    else:
        podcast_result = FAILED
        podcasts_failed += 1

    # Print and tally results before going to the next url for testing
    message = "Podcast Result = %s\n\n" % podcast_result
    functions.show_message(message)


print("=======\nPODCAST BRANCH IO EPISODE PAGE RESULTS\n=======")
print("Podcast Titles failed   = %d" % failed_podcast_title)
print("Episode Titles failed   = %d" % failed_episode_title)
print("Podcast ID failed       = %d" % failed_podcast_id)
print("Episode ID failed       = %d" % failed_episode_id)
print("Podcast Logo failed     = %d" % failed_podcast_logo)
print("Podcast Category failed = %d" % failed_category_name)
print("-----------------------------------------------")
print("Podcasts failed = %d of %d" % (podcasts_failed, total_calls))
print("=====END PODCAST BRANCH IO EPISODE PAGE RESULTS=====\n\n")

FillGoogleSheetWithTestResults.fillSheet(MY_FILENAME, podcasts_failed)

sys.exit(0)
