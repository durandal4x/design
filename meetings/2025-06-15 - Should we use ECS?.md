---
date: 2025-06-15
type: meeting
summary: 
tags: 
attendees:
  - "[[Teifion]]"
  - "[[Dormouse]]"
---


# Log
- First time Teifion and Dormouse have spoken via audio so general introductions and getting to know each other
- Teifion went over the general structure of the server so far
- Teifion explained the concern around Database usage and should we look at using an ECS?
	- Primarily is using the database the right pattern for what we're doing here?
	- For the purposes of the simulation should we use something other than a database
	- Questions from Dormouse on if we should use a relational database
		- Both agreed Postgres is the correct choice for data permanence
- Dormouse thinks ECS might be a good shout at this stage, it seems to be the right sort of tool for sure
- Dormouse asks about alternatives
	- Teifion suggested we could store stuff in memory in general without changing the overall structure
- Dormouse asked Teifion if he felt ECS was needed at this point and the right choice right now
	- Teifion said; since the start of the chat and the more he's thought about it the more he's thinking not yet
	- Dormouse pointed out much is likely to be dropped and replaced in the future and swapping to ECS now might be an example of premature optimisation

