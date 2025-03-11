---
type: concept
tags: 
aliases:
---

# Description
[[Information]] that was accurate at one point in time but is now out of date; typically only possible when information is not transmitted instantaneously.

## Examples
- [[Honor Harrington Novella]] has no method of instant communication so a lot of information is out of date
- [[The Expanse]] information speed is limited by the speed of light
```dataview
TABLE
	without id
	link(file.link, title) as "Example",
	type as "Type"
FROM "examples"
Where contains(this.file.inlinks, file.link)
SORT title
```

