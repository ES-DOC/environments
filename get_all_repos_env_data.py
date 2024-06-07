"""
TODO 

"""

import json
from pprint import pprint

from github import Github
from github import Auth

# WARNING: do not commit personal tokens!
MY_TOKEN = "<ADD TOKEN HERE>"

ORG_NAME = "ES-DOC"


auth = Auth.Token(MY_TOKEN)
# Public Web Github
g = Github(auth=auth)
# Get the ES-DOC org
o = g.get_organization(ORG_NAME)

# Get all repositories
repos = o.get_repos()

# Create a mapping to store per-repo content
repo_env_content = {}
for repo in repos:
    # Get env-related content:

    # TODO: how to handle lack of files
    # 'github.GithubException.UnknownObjectException' raising? (see try/except)
    filenames = {
        "REQS": "requirements.txt",
        "SETUP": "setup.py",
        "PIPFILE": "Pipfile",
        "PIPFILE LOCK": "Pipfile.lock",
    }
    repo_env_content[repo.full_name] = {}
    for f_key, f_name in filenames.items():
        try:
            f_exists = repo.get_contents(f_name)
        except:
            f_exists = False
        if f_exists:
            f_url = f_exists.html_url
            # Add to registry of env content, else don't add is doesn't exist
            repo_env_content[repo.full_name][f_name] = f_url

# Report
print("Repo names are:")
pprint([r.full_name for r in repos])
print("Repo env-related content found at:")
pprint(repo_env_content)

# Must close connections after use
g.close()

# Save details to a file for reference, as JSON
with open("repo-report.json", "w") as f:
    json.dump(repo_env_content, f)
