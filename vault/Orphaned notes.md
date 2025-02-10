Files with no links to or from them.
```dataview
LIST FROM -"templates"
WHERE length(file.inlinks) = 0
	AND length(file.outlinks) = 0
	AND type != "home"
	AND startswith(file.path, "vault") = false
```
