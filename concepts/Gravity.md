---
type: concept
tags: 
aliases:
---

# Description
The concept where objects are pulled towards a specific point (typically the [[Ground (Terrain type)|Ground]])


## Ideas
- 

## Examples
- 
```dataview
TABLE
	without id
	link(file.link, title) as "Example",
	type as "Type"
FROM "examples"
Where contains(this.file.inlinks, file.link)
SORT title
```

