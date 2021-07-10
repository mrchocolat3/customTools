#!/bin/bash

echo -e "
========================================================
Name: Github Data Puller
Author: MrChocolat3. https://www.github.com/mrchocolat3
Created At: 7/9/2021 
========================================================

"

# GLOBAL VARIABLES
TEMPDIR="$TMP/temporaryClonedDirectory"
MAIN_DIR="$(dirname $(readlink -f $0))"
USAGE="
Usage: 
\n    ./updater.sh <userName> <projectName> <timeToWait>(optional)
\ne.x: 
\n    ./updater.sh username project main 5
\n
\nIt will pull data from branch main in https://github.com/username/project.git 
\nevery 5 seconds if modified by other collaborators!
"

# CHECK AND SET INPUTES
if [ -z "$1" ] 
then 
    echo "[x] -> User name is missing!"
    echo -e $USAGE
    exit 1
else
    USERNAME=$1
fi

if [ -z "$2" ]
then 
    echo "[x] -> Project name is missing!"
    echo -e $USAGE
    exit 1
else 
    PROJECT_NAME=$2
fi

if [ -z "$3" ]
then 
    echo "[x] -> Branch name is missing!"
    echo -e $USAGE
    exit 1
else 
    BRANCH_NAME=$3
fi 

if [ -z "$4" ]
then 
    echo "[!] -> Since you did not specified waiting time, setting interval time to 1s!"
    echo -e $USAGE
    WAITING_TIME=$4
else 
    echo "[!] -> Set wait time to $4s"
    WAITING_TIME=$4
fi 

# CLEAR CACHE ON FIRST RUN AND CLONE THE PROJECT
echo -e "[!] -> Clearing cache..."
if [ -d "$TEMPDIR" ]
then 
    rm -Rf $TEMPDIR
    echo "[!] -> Cleared Succesfully!" 
    mkdir $TEMPDIR
    cd $TEMPDIR
    git clone https://www.github.com/$USERNAME/$PROJECT_NAME.git .
fi

# MAIN LOOP
while true
do
    echo -e "\n[!] -> Fetching from $BRANCH_NAME..."
    git fetch origin $BRANCH_NAME

    if git status | grep "git pull"
    then 
        echo -e "\n[!] -> Pulling data... "
        cd $MAIN_DIR
        git pull 
    else
        echo -e "\n[!] -> No updates yet..."
    fi
    
    echo -e "\n[!] -> Retrying in $WAITING_TIME s..."
    sleep $WAITING_TIME
done
