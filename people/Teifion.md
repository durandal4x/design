---
title: 
email: 
discord_name: Teifion
tags: 
type: person
pronouns: 
aliases:
---
# Teifion


### Recent meetings
```dataview
TABLE
	without id
	link(file.link, title) as "Meeting",
	date as "Date"
FROM "Durandal/meetings"
WHERE contains(attendees, this.file.link)
SORT date desc
LIMIT 10
```

