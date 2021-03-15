#! /tmp/python3

# -------------------------------------------------------------------------------------------------
# VERSION: 1.1
#
# Purpose Statement:
# JIRA Ticket Link (if applicable):
#
# Original Author: S Lehnert  Created: November 2020
# Updating Author: S Lehnert  Updated: March 2021
# Updating Author:
# Last Updated:
# -------------------------------------------------------------------------------------------------
# Additional Information (Optional):
# On National Podcasts Front Page ONLY: sanitized
# For Podcast Section Front page only. National page has no API so Product gave
# expected requirements for title and description of the page.
#
# Acceptance Criteria:
# 1) Match expected title with: HTML <title>, og:title, and twitter:title
# 2) Match expected description with: HTML <description>, twitter:description, and
#    og:description
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

page_url = "sanitized"
page_data = functions.call_url(page_url)[:PAGE_BUFFER]

# ------------------------
# Test section
# ------------------------
title_failed = 0
desc_failed = 0

# Title should exist and be exactly like this:
# sanitized
print("   TEST 1: Title Check")

expected_title = "sanitized"
expected_title = expected_title.upper()

# Function returns string in upper case
title         = functions.get_title(page_data)
og_title      = functions.get_meta_tag_content(page_data, "og:title")
twitter_title = functions.get_meta_tag_content(page_data, "", "twitter:title")
# Comparison time
match1 = functions.compare(expected_title, title)
match2 = functions.compare(expected_title, og_title)
match3 = functions.compare(expected_title, twitter_title)

if match1 and match2 and match3:
    message = "   Podcast title: %s\n" % PASSED
else:
    message = "   Podcast title: %s\n" % FAILED
    title_failed += 1
functions.show_message(message)


# Description should exist and be exactly like this:
# sanitized
print("   TEST 2: Description Check")

expected_description = "sanitized"
expected_description = expected_description.upper()

# Function returns string in upper case
description         = functions.get_meta_tag_content(page_data, "", "description")
og_description      = functions.get_meta_tag_content(page_data, "og:description")
twitter_description = functions.get_meta_tag_content(page_data, "", "twitter:description")
# Comparison time
match1 = functions.compare(expected_description, description)
match2 = functions.compare(expected_description, og_description)
match3 = functions.compare(expected_description, twitter_description)

if match1 and match2 and match3:
    message = "   Podcast description: %s\n" % PASSED
else:
    message = "   Podcast description: %s\n" % FAILED
    desc_failed += 1
functions.show_message(message)


# ------------------------
# Results section
# ------------------------

print("=======\nPODCAST SECTION FRONT PAGE RESULTS\n=======")
if title_failed == 0:
    print("Podcast Title Passed")
else:
    print("Podcast Title Failed")

if desc_failed == 0:
    print("Podcast Description Passed")
else:
    print("Podcast Description Failed")
print("=====END PODCAST SECTION FRONT PAGE RESULTS=====\n\n")

total_failed = title_failed + desc_failed
FillGoogleSheetWithTestResults.fillSheet(MY_FILENAME, total_failed)

sys.exit(0)
