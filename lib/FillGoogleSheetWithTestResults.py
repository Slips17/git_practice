#! /tmp/python3

# -------------------------------------------------------------------------------------------------
# Purpose Statement: This script is called by all the Podcast scripts to report number of errors.
# This script will take the results and put Pass/Fail status into the worksheet of the
# Google Sheet for the specific test that was executed.
#
# Original Author: S Lehnert  Created: May 2020
# Updating Author: S Lehnert  Updated: March 2021
# Updating Author:
# Last Updated:
# -------------------------------------------------------------------------------------------------
# Additional Information (Optional):
# The credentials json file is specific to the local machine running the tests. Be sure to modify
# that filename as appropriate.
# To make the code "callable" for other scripts, the code must be inside functions.
# -------------------------------------------------------------------------------------------------

#---------------
# Boiler Plate
#---------------
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Need all 4 of these or it gives errors
scope = ["sanitized",
         "sanitized"]

# Make sure to add the correct name for your key file (.json file).
# This is a locally stored credentials file.
MY_PATH     = os.path.dirname(os.path.realpath(__file__))
jsonFile = os.path.join(MY_PATH, "BEAutomation.json")
creds = ServiceAccountCredentials.from_json_keyfile_name(jsonFile, scope)
client = gspread.authorize(creds)

#-------------------
# End Boiler Plate
#-------------------

def fillSheet(name, error):
    # Open the Google Sheet file by name
    # Specify the file's worksheet by name
    sheet = client.open("sanitized")
    worksheet = sheet.worksheet("sanitized")

    # This is the dictionary of test names and what row of the sheet they correspond to
    row_dict = {"Podcast_HTML_BranchIOTagsComparisonStationPages": 3,
                "Podcast_HTML_BranchIOTagsForPodcastEpisodePages": 4,
                "Podcast_HTML_TitleAndDescriptionAndImageComparison": 5,
                "Podcast_HTML_TitleAndDescriptionOnRDCPage": 6,
                "Podcast_HTML_VerifyEpisodesTitleDescriptionAndImage": 7,
                "Podcast_ShowDetailsPage_NationalAndStationPagesReturn200": 8,
                "Podcast_ShowDetailsPage_Verify20EpisodesForOneSpecificPodcast": 9,
                "Podcast_ShowDetailsPage_VerifyEpisodesHaveImageURLPubDateAndDurationSeconds": 10,
                "Podcast_ShowDetailsPage_DescriptionComparison": 11,
                "SEO_HTML_TitleAndDescriptionComparison": 13,
                "SEO_HTML_TitleTagAndMetaTagComparison": 14,
                "SEO_HTML_BranchIOTagsForContestPages": 15,
                "SEO_HTML_BranchIOTagsForArticleGalleryPages": 16,
                "SEO_HTML_BranchIOTagsForSectionFrontPages": 17,
                "SEO_HTML_BranchIOTagsForContentCollectionPages": 18,
                "SEO_HTML_BranchIOTagsForEventsPages": 19,
                "EditorialGroup_VerifyDBChangesStick": 21,
                "AdOps_HTML_NMCTagsForArticlePages": 23,
                "AdOps_HTML_NMCTagsForAuthorPages": 24,
                "AdOps_HTML_NMCTagsForContestPages": 25,
                "AdOps_HTML_NMCTagsForEventPages": 26,
                "AdOps_HTML_NMCTagsForGalleryPages": 27,
                "AdOps_HTML_NMCTagsForSectionFrontPages": 28,
                "AdOps_HTML_NMCTagsForTopicPages": 29
                }

    row = row_dict[name] # figure out what row to use based on the name of the test calling this script's function
    column = 12  # currently all Pass/Fail results are recorded in column 12

    # figure out the Pass/Fail rating
    if error == 0:
        worksheet.update_cell(row, column, "Passed")
    else:
        worksheet.update_cell(row, column, "Failed")


def fillMigrationSheet(name, error):
    # Open the Google Sheet file by name
    # Specify the file's worksheet by name
    sheet = client.open("sanitized")
    worksheet = sheet.worksheet("sanitized")

    # This is the dictionary of test names and what row of the sheet they correspond to
    row_dict = {"SEO_HTML_ProdMigrationSanityCheckMetaTags": 2,
                "AdOps_HTML_ProdAndPreProdNMCTagsForStationFrontPages": 3
                }

    row = row_dict[name] # figure out what row to use based on the name of the test calling this script's function
    column = 6  # currently all Pass/Fail results are recorded in column 12

    # figure out the Pass/Fail rating
    if error == 0:
        worksheet.update_cell(row, column, "Passed")
    else:
        worksheet.update_cell(row, column, "Failed")
