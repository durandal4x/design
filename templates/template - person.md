---
role: 
discord_name: 
tags: 
type: person
pronouns: 
aliases: 
gh_name:
---
# <% tp.file.title %>
<% await tp.file.move("people/" + tp.file.title) %>

### Recent meetings
```dataview
TABLE
	without id
	link(file.link, title) as "Meeting",
	date as "Date"
FROM "meetings"
WHERE contains(attendees, this.file.link)
SORT date desc
LIMIT 10
```

