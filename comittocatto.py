import sys
import requests

org = sys.argv[1]

email_set = set() # Set to store unique emails

repos_url = f"https://api.github.com/orgs/{org}/repos"
repos_response = requests.get(repos_url)
repos_data = repos_response.json()

for repo in repos_data:
    commits_url = f"https://api.github.com/repos/{org}/{repo['name']}/commits"
    commits_response = requests.get(commits_url)
    commits_data = commits_response.json()

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
                    print(f"Repo: {repo['name']}, Email: {email}")
                    email_set.add(email)
