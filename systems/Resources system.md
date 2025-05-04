---
type: system
tags: 
aliases:
---

```dataview
TABLE
	without id
	link(file.link, title) as "Item",
	type as "Type"
FROM "design docs"
Where contains(this.file.inlinks, file.link)
SORT title
```
