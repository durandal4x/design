import json
import yaml
import sys
import subprocess
import os
import datetime

# If you're testing this and don't want to hit the GitHub API
# set this to True
local_only = False

def build_gh_person_lookup():
  result = {}
  
  for _root, _dirs, filenames in os.walk("people"):
    for filename in filenames:
      with open(f"people/{filename}", "r") as file:
        contents = file.read()
        properties = get_obsidian_properties_from_string(contents)
        properties["filename"] = filename.replace(".md", "")

        if "gh_name" in properties:
          result[properties["gh_name"]] = properties

  return result

def get_issue(issue_number):
  if local_only:
    return dummy_issue

  result = subprocess.check_output(["gh", "api", f"/repos/durandal4x/design/issues/{issue_number}"])
  return json.loads(result)

def get_comments(issue_number):
  if local_only:
    return dummy_comments
  
  result = subprocess.check_output(["gh", "api", f"/repos/durandal4x/design/issues/{issue_number}/comments"])
  return json.loads(result)

# Given an issue number, return a the filename and properties of the relevant
# design doc in the vault
def get_document(issue_number):
  # List all files in the directory
  for _root, _dirs, filenames in os.walk("design docs"):
    for filename in filenames:
      with open(f"design docs/{filename}", "r") as file:
        contents = file.read()
        properties = get_obsidian_properties_from_string(contents)

        if properties["issue_number"] == issue_number:
          return (filename, properties)

# Given the string of an obsidian file, extract the properties from the front matter
def get_obsidian_properties_from_string(file_string):
  file_parts = file_string.split("---")
  property_string = file_parts[1]
  
  yaml_data = yaml.safe_load(property_string)
  return yaml_data

def update_design_page_properties(issue, doc_name, comments_path):
  document_path = f"design docs/{doc_name}"
  with open(document_path, "r") as file:
    contents = file.read()
    properties = get_obsidian_properties_from_string(contents)
  
  properties["tags"] = list(set(properties["tags"] + ["design"]))
  properties["github_issue"] = issue["html_url"]
  properties["comments"] = f"[[{comments_path}|Comments]]"
  
  file_parts = contents.split("---")[2:]
  file_parts = "---".join(file_parts).strip()
  property_string = yaml.dump(properties)
  
  text = f"""---
{property_string}
---
{file_parts}
"""
  
  with open(document_path, "w") as file:
    file.write(text)

def create_comment_page_properties(issue, comments, doc_name, doc_properties):
  gh_lookup = build_gh_person_lookup()
  
  person_set = set()
  for c in comments:
    person = gh_lookup.get(c["user"]["login"])
    if person != None:
      person_set.add(person["filename"])
  
  tags = set(doc_properties["tags"] + ["comments"])
  tags.remove("design")
  
  properties = {
    "tags": list(tags),
    "type": "design-comments",
    "issue_number": str(issue["number"]),
    "github_issue": issue["html_url"],
    "document": f"[[{doc_name}|{issue['title']}]]",
    "participants": [f'[[{p}]]' for p in list(person_set)]
  }
  return yaml.dump(properties)

# Given a list of comments, create a new markdown file in the discussions directory
def create_comments_page(issue, comments, doc_name, doc_properties):
  properties = create_comment_page_properties(issue, comments, doc_name, doc_properties)
  
  gh_lookup = build_gh_person_lookup()
  
  tags = doc_properties.get("tags")
  if tags is None:
    tags = []
  tags += ["design", "comments"]

  comments_text = []
  for c in comments:
    person = gh_lookup.get(c["user"]["login"])
    
    dt = datetime.datetime.strptime(c["updated_at"], "%Y-%m-%dT%H:%M:%SZ")
    formatted_date = dt.strftime("%Y-%m-%d %H:%M:%S")
    formatted_date = f'[{formatted_date}]({c["html_url"]})'

    if person != None:
      if person["discord_name"] != c["user"]["login"]:
        comment_name = f'{c["user"]["login"]} - ({person["filename"]})'
      else:
        comment_name = person["filename"]

      text = f"""
**{comment_name}** - {formatted_date}
{c["body"].replace(" (edited)", "")}
"""
      
    else:
      text = f"""
**{c["user"]["login"]}** - {formatted_date}
{c["body"].replace(" (edited)", "")}
"""
    comments_text.append(text)

  comments_text = "".join(comments_text)

  text = f"""---
{properties}
---
{comments_text}"""
  
  file_path = f"discussions/{issue['title']} - Design comments.md"
  
  with open(file_path, "w") as file:
    file.write(text)
  
  return file_path

def main():
  if len(sys.argv) == 1:
    print("Usage: python3 scripts/get_comments.py [issue_number]")
    
  elif len(sys.argv) > 2:
    print("Usage: python3 scripts/get_comments.py [issue_number]")
  
  else:
    [_ignore, issue_number] = sys.argv

    issue = get_issue(issue_number)
    comments = get_comments(issue_number)
    (doc_name, doc_properties) = get_document(issue_number)
    
    comments_path = create_comments_page(issue, comments, doc_name, doc_properties)
    update_design_page_properties(issue, doc_name, comments_path)


dummy_issue = {'url': 'https://api.github.com/repos/durandal4x/design/issues/1', 'repository_url': 'https://api.github.com/repos/durandal4x/design', 'labels_url': 'https://api.github.com/repos/durandal4x/design/issues/1/labels{/name}', 'comments_url': 'https://api.github.com/repos/durandal4x/design/issues/1/comments', 'events_url': 'https://api.github.com/repos/durandal4x/design/issues/1/events', 'html_url': 'https://github.com/durandal4x/design/issues/1', 'id': 2843764785, 'node_id': 'I_kwDON3XpS86pgGgx', 'number': 1, 'title': 'Surface gravity', 'user': {'login': 'Avaristimo', 'id': 73989722, 'node_id': 'MDQ6VXNlcjczOTg5NzIy', 'avatar_url': 'https://avatars.githubusercontent.com/u/73989722?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/Avaristimo', 'html_url': 'https://github.com/Avaristimo', 'followers_url': 'https://api.github.com/users/Avaristimo/followers', 'following_url': 'https://api.github.com/users/Avaristimo/following{/other_user}', 'gists_url': 'https://api.github.com/users/Avaristimo/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/Avaristimo/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/Avaristimo/subscriptions', 'organizations_url': 'https://api.github.com/users/Avaristimo/orgs', 'repos_url': 'https://api.github.com/users/Avaristimo/repos', 'events_url': 'https://api.github.com/users/Avaristimo/events{/privacy}', 'received_events_url': 'https://api.github.com/users/Avaristimo/received_events', 'type': 'User', 'user_view_type': 'public', 'site_admin': False}, 'labels': [], 'state': 'open', 'locked': False, 'assignee': None, 'assignees': [], 'milestone': None, 'comments': 2, 'created_at': '2025-02-10T21:53:47Z', 'updated_at': '2025-02-11T00:01:37Z', 'closed_at': None, 'author_association': 'MEMBER', 'sub_issues_summary': {'total': 0, 'completed': 0, 'percent_completed': 0}, 'active_lock_reason': None, 'body': None, 'closed_by': None, 'reactions': {'url': 'https://api.github.com/repos/durandal4x/design/issues/1/reactions', 'total_count': 0, '+1': 0, '-1': 0, 'laugh': 0, 'hooray': 0, 'confused': 0, 'heart': 0, 'rocket': 0, 'eyes': 0}, 'timeline_url': 'https://api.github.com/repos/durandal4x/design/issues/1/timeline', 'performed_via_github_app': None, 'state_reason': None}

dummy_comments = [{'url': 'https://api.github.com/repos/durandal4x/design/issues/comments/2649328727', 'html_url': 'https://github.com/durandal4x/design/issues/1#issuecomment-2649328727', 'issue_url': 'https://api.github.com/repos/durandal4x/design/issues/1', 'id': 2649328727, 'node_id': 'IC_kwDON3XpS86d6YxX', 'user': {'login': 'Avaristimo', 'id': 73989722, 'node_id': 'MDQ6VXNlcjczOTg5NzIy', 'avatar_url': 'https://avatars.githubusercontent.com/u/73989722?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/Avaristimo', 'html_url': 'https://github.com/Avaristimo', 'followers_url': 'https://api.github.com/users/Avaristimo/followers', 'following_url': 'https://api.github.com/users/Avaristimo/following{/other_user}', 'gists_url': 'https://api.github.com/users/Avaristimo/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/Avaristimo/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/Avaristimo/subscriptions', 'organizations_url': 'https://api.github.com/users/Avaristimo/orgs', 'repos_url': 'https://api.github.com/users/Avaristimo/repos', 'events_url': 'https://api.github.com/users/Avaristimo/events{/privacy}', 'received_events_url': 'https://api.github.com/users/Avaristimo/received_events', 'type': 'User', 'user_view_type': 'public', 'site_admin': False}, 'created_at': '2025-02-10T21:54:33Z', 'updated_at': '2025-02-10T21:56:12Z', 'author_association': 'MEMBER', 'body': 'The surface gravity of a planet determines the fuel costs for resources and ships to be transported out of the planet. (edited)', 'reactions': {'url': 'https://api.github.com/repos/durandal4x/design/issues/comments/2649328727/reactions', 'total_count': 0, '+1': 0, '-1': 0, 'laugh': 0, 'hooray': 0, 'confused': 0, 'heart': 0, 'rocket': 0, 'eyes': 0}, 'performed_via_github_app': None}, {'url': 'https://api.github.com/repos/durandal4x/design/issues/comments/2649332227', 'html_url': 'https://github.com/durandal4x/design/issues/1#issuecomment-2649332227', 'issue_url': 'https://api.github.com/repos/durandal4x/design/issues/1', 'id': 2649332227, 'node_id': 'IC_kwDON3XpS86d6ZoD', 'user': {'login': 'Teifion', 'id': 167068, 'node_id': 'MDQ6VXNlcjE2NzA2OA==', 'avatar_url': 'https://avatars.githubusercontent.com/u/167068?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/Teifion', 'html_url': 'https://github.com/Teifion', 'followers_url': 'https://api.github.com/users/Teifion/followers', 'following_url': 'https://api.github.com/users/Teifion/following{/other_user}', 'gists_url': 'https://api.github.com/users/Teifion/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/Teifion/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/Teifion/subscriptions', 'organizations_url': 'https://api.github.com/users/Teifion/orgs', 'repos_url': 'https://api.github.com/users/Teifion/repos', 'events_url': 'https://api.github.com/users/Teifion/events{/privacy}', 'received_events_url': 'https://api.github.com/users/Teifion/received_events', 'type': 'User', 'user_view_type': 'public', 'site_admin': False}, 'created_at': '2025-02-10T21:56:18Z', 'updated_at': '2025-02-11T00:01:37Z', 'author_association': 'MEMBER', 'body': "It could also have an impact on combat near it, if you're fighting with the gravity well to your back you are potentially less manoeuvrable, like fighting up hill.\n\nAdditional questions:\n- Should gravity affect resource extraction?\n- What effects will gravity have on resource production/refinement?\n- What effects will gravity have on the population of a planet?", 'reactions': {'url': 'https://api.github.com/repos/durandal4x/design/issues/comments/2649332227/reactions', 'total_count': 0, '+1': 0, '-1': 0, 'laugh': 0, 'hooray': 0, 'confused': 0, 'heart': 0, 'rocket': 0, 'eyes': 0}, 'performed_via_github_app': None}]

if __name__ == "__main__":
  main()