import json
import yaml
import sys
import subprocess
import os
import datetime

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
  result = subprocess.check_output(["gh", "api", f"/repos/durandal4x/design/issues/{issue_number}"])
  return json.loads(result)

def get_comments(issue_number):
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

        if properties["github-issue"] == issue_number:
          return (filename, properties)

# Given the string of an obsidian file, extract the properties from the front matter
def get_obsidian_properties_from_string(file_string):
  file_parts = file_string.split("---")
  property_string = file_parts[1]
  
  yaml_data = yaml.safe_load(property_string)
  return yaml_data

# Given a list of comments, create a new markdown file in the discussions directory
def create_comments_page(issue, comments, doc_name, doc_properties):
  gh_lookup = build_gh_person_lookup()
  
  document_path = f"design docs/{doc_name}".replace(".md", "")
  tags = doc_properties.get("tags")
  if tags is None:
    tags = []
  tags += ["design", "comments"]

  comments_text = []
  for c in comments:
    person = gh_lookup.get(c["user"]["login"])
    
    dt = datetime.datetime.strptime(c["updated_at"], "%Y-%m-%dT%H:%M:%SZ")
    formatted_date = dt.strftime("%Y-%m-%d %H:%M:%S")
    
    if person != None:
      text = f"""
**[[{person["filename"]}]]** - {formatted_date}
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
tags: {", ".join(tags)}
type: design-comments
github-issue: "{issue["number"]}"
design-doc: "[[{document_path}|{issue["title"]}]]"
---
[GitHub issue]({issue["html_url"]})

{comments_text}
  """
  
  name = f"{issue['title']} - Design comments"
  
  with open(f"discussions/{name}.md", "w") as file:
    file.write(text)

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
    
    create_comments_page(issue, comments, doc_name, doc_properties)

if __name__ == "__main__":
  main()
  
  