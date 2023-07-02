import sys

import requests

from tqdm import tqdm

global filename

filename = "gitcomito-logs.txt"




def log(text):

    print(text)

    f = open(filename,"a")

    if text != "":

        f.write("[+] "+text+"\n")

    else:

        f.write("\n")

    f.close()




org = sys.argv[1]




log("Start grathing repos from github\n")




email_set = set() # Set to store unique emails





repos_url = f"https://api.github.com/orgs/{org}/repos"

repos_response = requests.get(repos_url)

if ("API rate limit exceeded for" in repos_response.text):

    log("Error:\n"+repos_response.text)

else:

    repos_data = repos_response.json()

    log("Found "+str(len(repos_data))+" repos from "+org+"\n")

    repo_count = 1

    for repo in repos_data:

        repo_name = repo['name']

        commits_url = f"https://api.github.com/repos/{org}/{repo['name']}/commits"

        commits_response = requests.get(commits_url)

        commits_data = commits_response.json()

        log(str(repo_count) + " - Found "+str(len(commits_data))+" commits from "+org+"/"+repo_name+"\n")




        commit_count = 1

        for commit in commits_data:

            patch_url = f"https://github.com/{org}/{repo['name']}/commit/{commit['sha']}.patch"

            patch_response = requests.get(patch_url)

            patch_lines = patch_response.content.decode('utf-8').splitlines()




            if len(patch_lines) >= 2:

                second_line = patch_lines[1]

                email_start = second_line.find('<')

                email_end = second_line.find('>')

                if email_start != -1 and email_end != -1:

                    email = second_line[email_start+1:email_end]

                    if "@users.noreply.github.com" in email:

                        email = "hidden email address"

                    else:

                        name_start = second_line.find(':') + 2

                        name_end = email_start - 1

                        name = second_line[name_start:name_end]

                        email = f"{name} ({email})"

                    if email not in email_set:

                        log("\tRepo: "+repo_name+", Email: "+email)

                        email_set.add(email)

            commit_count += 1

        repo_count += 1

    log("Done, We collect "+str(len(email_set))+" email addresses. ("+filename+")")
