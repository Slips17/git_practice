#! /tmp/python3

# -------------------------------------------------------------------------------------------------
# VERSION: 2.0
#
# Purpose Statement: For testing Podcast Episode pages - NOT Show pages
#
# JIRA Ticket Link (if applicable):
#
# Original Author: S Lehnert  Created: August 2020
# Updating Author: S Lehnert  Updated: October 2020
# Updating Author: S Lehnert  Updated: March 2021
# Updating Author:
# Last Updated:
# -------------------------------------------------------------------------------------------------
# Additional Information (Optional):
# The Podcast Episode pages pull the images from the Podcast Show API data, but
# the rest of the data under test is from the Podcast Episode API data.
#
# Acceptance Criteria:
# 1) Match api title with: HTML <title>, og:title, and twitter:title
# 2) Match api description with: HTML <description>, twitter:description, and
#    og:description
# 3) Match api image with: HTML twitter:image and og:image
#
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

# Pull URLS from a file
with open(LIBRARY_PATH + "/podcast_episode_urls.json") as file:
    podcast_urls = json.load(file)


# ----------------------------------------------------------------------------- compare()
def compare(api, html):
    """This function compares two items and returns True if they match.
        Returns False if they do not match.
    """
    if api == html:
        return True
    else:
        return False


# Variables
failed_episode_title_calls = 0
failed_episode_description_calls = 0
failed_podcast_logo_calls = 0
pages_failed = 0
total_calls = 0

# Using the data from the json file
for url in podcast_urls:
    total_calls += 1
    tests_passed_for_this_page = 0

    podcast_api_url = url["podcast_api_url"]
    episode_api_url = url["episode_api_url"]
    html_url        = url["html_url"]

    # Get all of the podcast data as a list of dictionaries
    episode_data_text = functions.call_url(episode_api_url)
    episode_data      = json.loads(episode_data_text)  # <-- List of dictionaries
    podcast_data_text = functions.call_url(podcast_api_url)
    podcast_data      = json.loads(podcast_data_text)  # <-- List of dictionaries

    # Episode API Variables
    episode_dictionary  = episode_data["data"]
    episode_title       = episode_dictionary["attributes"]["title"]
    episode_description = episode_dictionary["attributes"]["description"]

    # Podcast API Variables
    podcast_dictionary = podcast_data["data"]
    podcast_logo       = podcast_dictionary["attributes"]["image"]

    # Call for the web page data
    page_data = functions.call_url(html_url)[:PAGE_BUFFER]

    # If getting a 404 "not found" in the url results,
    # break the loop and report failed to the Google Sheet
    if "not found" in page_data:
        pages_failed = 1
        break

    # ------------------------------------------------------------------------
    # Test 1 of 3: Compare API Episode Title with HTML Episode Title, og:title,
    # and twitter:title. All 4 should match
    # ------------------------------------------------------------------------
    print("   TEST 1 of 3: Episode Title Check")

    # If None/Empty, return empty string. Else return in uppercase.
    episode_title = functions.isNoneOrEmpty(episode_title, "Episode Title")

    # Function returns string in upper case
    html_title    = functions.get_title(page_data)
    og_title      = functions.get_meta_tag_content(page_data, "og:title")
    twitter_title = functions.get_meta_tag_content(page_data, "", "twitter:title")

    # Comparison time - all titles should match
    print("      Looking for     : '%s'" % episode_title)
    print("      Title Tag Found : '%s'" % html_title)
    print("      OG Found        : '%s'" % og_title)
    print("      Twitter Found   : '%s'" % twitter_title)

    match1 = compare(episode_title, html_title)
    match2 = compare(episode_title, og_title)
    match3 = compare(episode_title, twitter_title)

    # If they all match, test passes. Else, test fails.
    if match1 and match2 and match3 == True:
        message = "   TEST 1 of 3: %s\n" % PASSED
        tests_passed_for_this_page += 1
    else:
        message = "   TEST 1 of 3: %s\n" % FAILED
        failed_episode_title_calls += 1
    functions.show_message(message)


    # --------------------------------------------------------------
    # TEST 2 of 3: Compare API description with HTML description,
    # twitter:description, and og:description. All 4 should match.
    # --------------------------------------------------------------
    print("   TEST 2 of 3: Description Check")

    # If None/Empty, return empty string. Else return in uppercase.
    episode_description = functions.isNoneOrEmpty(episode_description, "Episode Description")

    # Function returns string in upper case
    html_description    = functions.get_meta_tag_content(page_data, "", "description")
    og_description      = functions.get_meta_tag_content(page_data, "og:description")
    twitter_description = functions.get_meta_tag_content(page_data, "", "twitter:description")

    # Sometimes descriptions have ${PARAMVALUE} and we want an empty string
    # if that happens.
    html_description    = functions.check_for_empty(html_description)
    og_description      = functions.check_for_empty(og_description)
    twitter_description = functions.check_for_empty(twitter_description)

    # Comparison time - all four descriptions should match
    print("      Looking for     : '%s'" % episode_description)
    print("      HTML Desc Found : '%s'" % html_description)
    print("      OG Found        : '%s'" % og_description)
    print("      Twitter Found   : '%s'" % twitter_description)

    match1 = compare(episode_description, html_description)
    match2 = compare(episode_description, og_description)
    match3 = compare(episode_description, twitter_description)

    # If they all match, test passes. Else, test fails.
    if match1 and match2 and match3 == True:
        message = "   TEST 2 of 3: %s\n" % PASSED
        tests_passed_for_this_page += 1
    else:
        message = "   TEST 2 of 3: %s\n" % FAILED
        failed_episode_description_calls += 1
    functions.show_message(message)


    # ---------------------------------------------------------------------
    # TEST 3 of 3: Compare API image with HTML twitter:image and og:image.
    # All three should match.
    # ---------------------------------------------------------------------
    print("   TEST 3 of 3: Images Check")

    # If None/Empty, return empty string. Else return in uppercase.
    podcast_logo = functions.isNoneOrEmpty(podcast_logo, "Podcast Logo")

    # Function returns string in upper case
    og_image      = functions.get_meta_tag_content(page_data, "og:image")
    twitter_image = functions.get_meta_tag_content(page_data, "", "twitter:image")

    # Comparison time - all three image urls should match
    print("      Looking for     : '%s'" % podcast_logo)
    print("      OG Found        : '%s'" % og_image)
    print("      Twitter Found   : '%s'" % twitter_image)

    # Comparison time
    match1 = compare(podcast_logo, og_image)
    match2 = compare(podcast_logo, twitter_image)

    # If they all match, test passes. Else, test fails.
    if match1 and match2 == True:
        message = "   TEST 3 of 3: %s\n" % PASSED
        tests_passed_for_this_page += 1
    else:
        message = "   TEST 3 of 3: %s\n" % FAILED
        failed_podcast_logo_calls += 1
    functions.show_message(message)


    # -----------------------------
    # End of Loop tally
    # -----------------------------

    # If a test failed, the podcast fails.
    if tests_passed_for_this_page != 3:
        pages_failed += 1

    # Makes the console printout easier to read
    message = "\n"
    functions.show_message(message)


# ------------------------------------------
# Outside the for loop, print the results
# ------------------------------------------
print("=======\nRESULTS\n=======")
print("Titles failed       = %d of %d" % (failed_episode_title_calls, total_calls))
print("Descriptions failed = %d of %d" % (failed_episode_description_calls, total_calls))
print("Images failed       = %d of %d" % (failed_podcast_logo_calls, total_calls))
print("------------------------------")
print("Episodes failed     = %d of %d" % (pages_failed, total_calls))

FillGoogleSheetWithTestResults.fillSheet(MY_FILENAME, pages_failed)

sys.exit(0)
