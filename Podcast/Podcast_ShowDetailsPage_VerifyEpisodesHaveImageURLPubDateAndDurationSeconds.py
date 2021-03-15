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
# 1) Get a podcast URL page and loop through the episodes
# 2) Verify each of the podcast episodes has (is not empty):
#    a) Image URL
#    b) Publish Date
#    c) Duration_seconds
#    d) Podcast: Categories
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

# Set up for Podcast data
podcast_api_url = "sanitized"
# Get the Podcast API data
podcast_data_text = functions.call_url(podcast_api_url)
podcast_data = json.loads(podcast_data_text)

# Variables
podcast_title_count = 0
total_empty = 0
total_eps = 0

# Starting the loop to grab a Podcast
for podcast_dictionary in podcast_data["data"]:
    podcast_title_count += 1

    # Create a URL like this one:
    # sanitized
    podcast_site_slug = podcast_dictionary["attributes"]["site_slug"]
    base_url = "sanitized"
    podcast_filter = "sanitized" % podcast_site_slug

    # Set up for Podcast Episode data
    podcast_episodes_url = "sanitized" % (base_url, podcast_filter)
    # Get the Podcast Episode API data
    podcast_episode_data_text = functions.call_url(podcast_episodes_url)
    podcast_episode_data = json.loads(podcast_episode_data_text)

    # Message for troubleshooting
    message = "\nFound %d Podcast Episodes!" % len(podcast_episode_data["data"])
    functions.show_message(message)


    # ---- Podcast Episodes section -----

    # Podcast Episode variables
    episode_count    = 0
    empty_title      = 0
    empty_image      = 0
    empty_pub_date   = 0
    empty_duration   = 0
    empty_categories = 0

    # Loop for each Episode in the Podcast
    # Max 20 Episodes so script runtime is shorter
    for episode_dictionary in podcast_episode_data["data"][:20]:
        episode_count += 1
        message = "\nEpisode : %d" % episode_count
        functions.show_message(message)

        # Get the data values
        episode_site_slug = episode_dictionary["attributes"]["site_slug"]
        episode_title     = episode_dictionary["attributes"]["title"]
        episode_image     = episode_dictionary["attributes"]["image_url"]
        episode_pub_date  = episode_dictionary["attributes"]["published_date"]
        episode_duration  = episode_dictionary["attributes"]["duration_seconds"]

        # Categories is a list inside the podcast list inside attributes
        # Have to break it out
        episode_show_info = episode_dictionary["attributes"]["podcast"]

        if len(episode_show_info) > 1:
            message = "Episode has more than one podcast in the list!"
            functions.show_message(message)
            list_of_podcast_categories = []
            for item in episode_podcast_show_info:
                category = item["categories"]
                list_of_podcast_categories.append(category)
            episode_category = list_of_podcast_categories
            print("There is more than ONE!! API returns: %s" % episode_category)
        else:
            episode_category = episode_show_info[0]["categories"]

        # Check if the data values are "None" - if yes, increment counters
        ep_title_status = isNone(episode_title, "Podcast Episode Title")
        if ep_title_status == True:
            empty_title += 1

        ep_image_status = isNone(episode_image, "Podcast Episode Image URL")
        if ep_image_status == True:
            empty_image += 1

        ep_pub_date_status = isNone(episode_pub_date, "Podcast Episode Published Date")
        if ep_pub_date_status == True:
            empty_pub_date += 1

        ep_duration_status = isNone(episode_duration, "Podcast Episode Duration Seconds")
        if ep_duration_status == True:
            empty_duration += 1

        if episode_category is None:
            message = "%s -> Podcast Episode Categories is of type None" % FAILED
            empty_categories += 1
        elif episode_category is []:
            message = "%s -> Podcast Episode Categories is an empty list." % FAILED
            empty_categories += 1
        else:
            message = "%s -> Podcast Episode Categories is: %s" % (PASSED, episode_category)
        functions.show_message(message)


    # ---- Outside the Episodes section but inside the Podcast section -----

    # Adding for easier console readability
    message = "\n"
    functions.show_message(message)

    # Printing out the Episode results
    print("----------- EPISODE RESULTS ---------------")
    print("Empty 'Podcast Title'      : %s of %s" % (empty_title, episode_count))
    print("Empty 'Image URL'          : %s of %s" % (empty_image, episode_count))
    print("Empty 'Published Date'     : %s of %s" % (empty_pub_date, episode_count))
    print("Empty 'Duration Seconds'   : %s of %s" % (empty_duration, episode_count))
    print("Empty 'Podcast Categories' : %s of %s" % (empty_categories, episode_count))
    print("----------- EPISODE RESULTS ---------------\n")

    # Tally for End Script results
    total_empty = total_empty + empty_title + empty_image + empty_pub_date + \
                  empty_duration + empty_categories
    total_eps = total_eps + episode_count


# Printing out the script results
print("==========CHECK EPISODES PER PODCAST RESULTS==========")
print("Total Podcasts reviewed: %s" % podcast_title_count)
print("Total Episodes reviewed: %s" % total_eps)
print("Total Empty Episode Items (Failed Items) found: %s" % total_empty)
print("========END CHECK EPISODES PER PODCAST RESULTS========\n\n")

FillGoogleSheetWithTestResults.fillSheet(MY_FILENAME, total_empty)
