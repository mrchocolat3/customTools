#!/bin/bash

echo -e "
========================================================
Name: Github Data Puller
Author: MrChocolat3. https://www.github.com/mrchocolat3
Created At: 7/9/2021 
Updated At: 27/10/2021

========================================================

"

# GLOBAL VARIABLES
TEMPDIR="$TMP/temporaryClonedDirectory"
MAIN_DIR="$(dirname $(readlink -f $0))"
USAGE="
Usage: 
\n    ./updater.sh <userName> <projectName> <branchName> <remoteName> <timeToWait>(optional)
\ne.x: 
\n    ./updater.sh username project origin main jhon@doe.com 5
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
  echo "[x] -> Remote Name is missing!"
  echo -e $USAGE 
  exit 1
else
  REMOTE_NAME=$4
fi


if [ -z "$5" ]
then 
    echo "[!] -> Since you did not specified waiting time, setting interval time to 1s!"
    echo -e $USAGE
    WAITING_TIME=1
else 
    echo "[!] -> Set wait time to $5s"
    WAITING_TIME=$5
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


# SET USERNAME AND PASSWORD 
echo -e "
\nSome times there are clonflicts in Git repositories. For that, It has to 
\nStash your local files so it doesn't get overwritten or removed. So please
\nGive your email address and username for this repository. It will show as a
\nContributor.
"
echo -ne "Email: "
read email 
EMAI_ADDR="$email"

echo -ne "Username: "
read userName
REPO_USER="$userName"

echo "[!] -> SETTING EMAIL: $EMAI_ADDR for this repository"
git config user.email $EMAI_ADDR
echo -e "\n[!] -> SETTING USERNAME: $REPO_USER for this repository"
git config user.name $REPO_USER


# MAIN LOOP
while true
do
    echo -e "\n[!] -> Fetching from $REMOTE_NAME: $BRANCH_NAME..."
    git fetch $REMOTE_NAME $BRANCH_NAME

    if git status | grep "git push"
    then
        echo -e "\n[!] -> Pulling data... "
        cd $MAIN_DIR
        git pull $REMOTE_NAME $BRANCH_NAME
    elif git status | grep "modified"
    then
      clear 
      git stash
      echo -e "\n[!] -> Pulling data..."
      git pull $REMOTE_NAME $BRANCH_NAME
      echo -e "\n[!] -> Poping Stash"
      git stash pop 
    else
        echo -e "\n[!] -> No updates yet..."
    fi
    
    echo -e "\n[!] -> Retrying in $WAITING_TIME s..."
    sleep $WAITING_TIME
done
