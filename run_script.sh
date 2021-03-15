#!/bin/bash

# ---------------------------------------------------------------------------------
# Original Author: S Lehnert  Created: June 2020
# Updating Author:
# Last Updated:
# ---------------------------------------------------------------------------------

#----------------------------------------------------------------------------------
# ALL the Unity Backend Automation scripts are listed here.
# The for loops will run ALL the .py scripts in the corresponding folder.
# If you do NOT want to run ALL the scripts, 
#  1. Comment out the For loop
#  2. Uncomment the tests you want to run
#----------------------------------------------------------------------------------

#----------------------------------------------------------------------------------
# To run this script:
# 1. Open a terminal window.
# 2. CD to the rad-qa-test-automation/testcases/Unity folder.
# 3. LS -L to make sure this script has execution permissions.
#   3a. Should look like -rwxr--r--
#   3b. IF there are no X's, type: chmod u+x run_script.sh
# 4. To run the script, type: ./run_script.sh
#----------------------------------------------------------------------------------

# PNAME="/Users/slehnert/Desktop/backup_be_auto_scripts"

# ------------------
#    SEO Scripts
# ------------------

# printf "RUNNING ALL THE FILES FOR THE SEO DIRECTORY.\n\n"
# for i in $PNAME/SEO/*.py; do
# 	printf "Test running is: $i\n\n"
# 	python3 "$i"
# done
# printf "\n\nFINISHED RUNNING ALL THE FILES FOR THE SEO DIRECTORY.\n"

python3 /Users/slehnert/Desktop/backup_be_auto_scripts/SEO/SEO_HTML_BranchIOTagsForArticleGalleryPages.py
python3 /Users/slehnert/Desktop/backup_be_auto_scripts/SEO/SEO_HTML_BranchIOTagsForContentCollectionPages.py
python3 /Users/slehnert/Desktop/backup_be_auto_scripts/SEO/SEO_HTML_BranchIOTagsForContestPages.py
python3 /Users/slehnert/Desktop/backup_be_auto_scripts/SEO/SEO_HTML_BranchIOTagsForEventsPages.py
python3 /Users/slehnert/Desktop/backup_be_auto_scripts/SEO/SEO_HTML_BranchIOTagsForSectionFrontPages.py
python3 /Users/slehnert/Desktop/backup_be_auto_scripts/SEO/SEO_HTML_TitleAndDescriptionComparison.py
python3 /Users/slehnert/Desktop/backup_be_auto_scripts/SEO/SEO_HTML_TitleTagAndMetaTagComparison.py

# ----------------------
#    PODCASTS Scripts
# ----------------------

# printf "RUNNING ALL THE FILES FOR THE PODCAST DIRECTORY.\n\n"
# for i in $PNAME/Podcast/*.py; do
# 	printf "Test running is: $i\n\n"
# 	python3 $i
# done
# printf "\n\nFINISHED RUNNING ALL THE FILES FOR THE PODCAST DIRECTORY.\n"

python3 /Users/slehnert/Desktop/backup_be_auto_scripts/Podcast/Podcast_HTML_BranchIOTagsComparisonStationPages.py
python3 /Users/slehnert/Desktop/backup_be_auto_scripts/Podcast/Podcast_HTML_BranchIOTagsForPodcastEpisodePages.py
python3 /Users/slehnert/Desktop/backup_be_auto_scripts/Podcast/Podcast_HTML_TitleAndDescriptionAndImageComparison.py
python3 /Users/slehnert/Desktop/backup_be_auto_scripts/Podcast/Podcast_HTML_TitleAndDescriptionOnRDCPage.py
python3 /Users/slehnert/Desktop/backup_be_auto_scripts/Podcast/Podcast_HTML_VerifyEpisodesTitleDescriptionAndImage.py
python3 /Users/slehnert/Desktop/backup_be_auto_scripts/Podcast/Podcast_ShowDetailsPage_NationalAndStationPagesReturn200.py
python3 /Users/slehnert/Desktop/backup_be_auto_scripts/Podcast/Podcast_ShowDetailsPage_Verify20EpisodesForOneSpecificPodcast.py
python3 /Users/slehnert/Desktop/backup_be_auto_scripts/Podcast/Podcast_ShowDetailsPage_VerifyEpisodesHaveImageURLPubDateAndDurationSeconds.py
python3 /Users/slehnert/Desktop/backup_be_auto_scripts/Podcast/Podcast_ShowDetailsPage_DescriptionComparison.py

# ------------------------
#  MISC FEATURES Scripts
# ------------------------

# printf "RUNNING ALL THE FILES FOR THE MISC FEATURES DIRECTORY.\n\n"
# for i in $PNAME/MiscFeatures/*.py; do
# 	printf "Test running is: $i\n\n"
# 	python3 $i
# done
# printf "\n\nFINISHED RUNNING ALL THE FILES FOR THE MISC DIRECTORY.\n"

python3 /Users/slehnert/Desktop/backup_be_auto_scripts/MiscFeatures/EditorialGroup_VerifyDBChangesStick.py

# ------------------------
#  AD OPS Scripts
# ------------------------

python3 /Users/slehnert/Desktop/backup_be_auto_scripts/AdOps/AdOps_HTML_NMCTagsForArticlePages.py
python3 /Users/slehnert/Desktop/backup_be_auto_scripts/AdOps/AdOps_HTML_NMCTagsForAuthorPages.py
python3 /Users/slehnert/Desktop/backup_be_auto_scripts/AdOps/AdOps_HTML_NMCTagsForContestPages.py
python3 /Users/slehnert/Desktop/backup_be_auto_scripts/AdOps/AdOps_HTML_NMCTagsForEventPages.py
python3 /Users/slehnert/Desktop/backup_be_auto_scripts/AdOps/AdOps_HTML_NMCTagsForGalleryPages.py
python3 /Users/slehnert/Desktop/backup_be_auto_scripts/AdOps/AdOps_HTML_NMCTagsForSectionFrontPages.py
python3 /Users/slehnert/Desktop/backup_be_auto_scripts/AdOps/AdOps_HTML_NMCTagsForTopicPages.py

