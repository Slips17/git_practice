#!/bin/bash

PNAME="/Users/slehnert/Desktop/backup_be_auto_scripts"
# LIST="$(ls $PNAME/SEO/*.py)"
# printf "RUNNING ALL THE FILES FOR THE SEO DIRECTORY.\n\n"
# for i in "$LIST"; do
# 	printf "Test running is: $i\n\n"
# 	python3 "$i"
# done
# printf "\n\nFINISHED RUNNING ALL THE FILES FOR THE SEO DIRECTORY.\n"

# PNAME="/Users/slehnert/Desktop/backup_be_auto_scripts"
# LIST="$(ls $PNAME/SEO/*.py)"
# printf "RUNNING ALL THE FILES FOR THE SEO DIRECTORY.\n\n"
# for i in $LIST; do
#     printf "Test running is: $i\n\n"
#     python3 "$i"
# done
# printf "\n\nFINISHED RUNNING ALL THE FILES FOR THE SEO DIRECTORY.\n"

for i in $PNAME/MiscFeatures/*.py; do
	printf "Test running is: $i\n\n"
	python3 $i
done