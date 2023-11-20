#!/bin/bash
ORG_URL="https://api.github.com/orgs/$ORGNAMECHANGEME/repos?per_page=200";

ALL_REPOS=$(curl -s ${ORG_URL} | grep html_url | awk 'NR%2 == 0' \
        | cut -d ':' -f 2-3 | tr -d '",');

for ORG_REPO in ${ALL_REPOS}; do
        git clone ${ORG_REPO}.git;
        sleep 2
done
