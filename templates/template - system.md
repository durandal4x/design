---
type: system
tags: 
aliases:
---
<% await tp.file.move("systems/" + tp.file.title) %>

```dataview
TABLE
	without id
	link(file.link, title) as "Item",
	type as "Type"
FROM "design docs"
Where contains(this.file.inlinks, file.link)
SORT title
```
