#! /tmp/python3

# -------------------------------------------------------------------------------------------------
# VERSION: 2.0
#
# Purpose Statement:
# JIRA Ticket Link (if applicable):
#
# Original Author: S Lehnert  Created: April 2020
# Updating Author: S Lehnert  Updated: November 2020
# Updating Author:
# Last Updated:
# -------------------------------------------------------------------------------------------------
# Additional Information (Optional):
#
# Acceptance Criteria:
# 1) Go to a podcast URL page (currently one specific page) and Verify it loads 200 OK
# 2) Verify each of the 20 podcasts has (is not empty):
#    a) Image URL
#    b) Publish Date
#    c) Duration_seconds
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
# ----------------------------------------------------------------------------- isNone()
def isNone(param, descriptor):
    """ Checks if the param value is None. If yes, prints a message using the
        descriptor and returns True. If not, prints a message and returns
        False.
    """
    if param is None:
        message = "%s -> %s is of type None" % (FAILED, descriptor)
        functions.show_message(message)
        return True
    else:
        message = "%s -> %s is: %s" % (PASSED, descriptor, param)
        functions.show_message(message)
        return False


# ---- End Functions section -----

# Go here and verify 200 OK
# sanitized
episode_url_base = "sanitized"
podcast_filter = "sanitized"
podcast_api_url = "sanitized" % (episode_url_base, podcast_filter)

# Get the podcast data
podcast_data_text = functions.call_url(podcast_api_url)
podcast_data = json.loads(podcast_data_text)

# Message for troubleshooting
message = "Found %d Podcast Episodes in the API.\n" % len(podcast_data["data"])
functions.show_message(message)

# Variables
title_count = 0
empty_title = 0
empty_image = 0
empty_pub_date = 0
empty_duration = 0

# Starting the for loop to check each podcast episode
for podcast_dictionary in podcast_data["data"]:
    # Get the data values
    title            = podcast_dictionary["attributes"]["title"]
    image_url        = podcast_dictionary["attributes"]["image_url"]
    pub_date         = podcast_dictionary["attributes"]["published_date"]
    duration_seconds = podcast_dictionary["attributes"]["duration_seconds"]

    # Check if the data values are "None" - if yes, increment counters
    title_status = isNone(title, "Podcast Title")
    if title_status == True:
        empty_title += 1
    else:
        title_count += 1

    image_status = isNone(image_url, "Podcast Image URL")
    if image_status == True:
        empty_image += 1

    pub_date_status = isNone(pub_date, "Podcast Published Date")
    if pub_date_status == True:
        empty_pub_date += 1

    duration_status = isNone(duration_seconds, "Podcast Duration Seconds")
    if duration_status == True:
        empty_duration += 1

    # Adding this for easier console readability
    message = "\n"
    functions.show_message(message)

# Printing out the results
print("=======20 EPISODES FOR ONE PODCAST RESULTS=======")
print("Total non-empty 'Podcast Title' : %s" % title_count)
print("Total empty 'Podcast Title'     : %s" % empty_title)
print("Total empty 'Image URL'         : %s" % empty_image)
print("Total empty 'Published Date'    : %s" % empty_pub_date)
print("Total empty 'Duration Seconds'  : %s" % empty_duration)
print("=====END 20 EPISODES FOR ONE PODCAST RESULTS=====\n\n")

total_empty = empty_title + empty_image + empty_pub_date + empty_duration
FillGoogleSheetWithTestResults.fillSheet(MY_FILENAME, total_empty)
