## Tagged with `todo`
```dataview
LIST
FROM #todo
WHERE type != "taglist"
SORT type ASC, file.title DESC
```



## Danging links

```dataview
TABLE
	WITHOUT ID
	key AS "Unresolved link",
	rows.file.link AS "Referencing file"
FROM ""
FLATTEN file.outlinks as outlinks
WHERE !(outlinks.file)
	AND startswith(meta(outlinks).path, "images") = false
GROUP BY outlinks
```
