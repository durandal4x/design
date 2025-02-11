---
role: 
discord_name: 
tags: 
type: person
pronouns: 
aliases: 
gh_name: 
game_id:
---
# <% tp.file.title %>
<% await tp.file.move("people/" + tp.file.title) %>


### Recent discussions
```dataview
TABLE
	without id
	link(file.link, title) as "Discussion",
	date as "Date"
FROM "discussions"
WHERE contains(participants, this.file.link)
SORT date desc
LIMIT 10
```

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

