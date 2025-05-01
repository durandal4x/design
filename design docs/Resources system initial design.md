---
tags:
  - economy
  - resources
type: design-doc
issue_number: 
github_issue: 
comments:
---
# Goal
A resource system underpins almost every aspect of an economic system and several more to boot. We want to have a flexible resource system allowing for complexity and depth without requiring either. Summarised as bullet points we want:
- Resources to have a physical storage location
- Resources need to be transported between locations to be consumed
- Resources need to have varying storage requirements (e.g. mass and volume)
- Resources need to be able to have things affect them over time (e.g. spoilage)

# Data
### Resource types
These represent information regarding a given resource which is then referenced by instances of the resource.
```
	name: string
	mass: integer (kilograms per unit)
	volume: integer (cubic meters per unit)
	quality?: boolean (manufactured and refined goods can have a quality)
	tags: array of string (things like `liquid` and `combustable` along with additional behaviours/restrictions we want to add later)
```

#### Examples

| Name        | Mass | Volume | Quality? | Tags                       |
| ----------- | ---- | ------ | -------- | -------------------------- |
| Water       | 1000 | 1      | False    | liquid                     |
| Dynamite    | 2000 | 4      | True     | explosive, combust-in-heat |
| Metal sheet | 1000 | 10     | True     |                            |
| Plants      | 1000 | 5      | True     | needs-atmosphere, delicate |

### Resource instances
Representing a specific instance of a resource existing. If two instances are combined then one would be deleted. It is expected within the database the instances will be further broken down by location type (e.g. ship or station).
```
	type: resource_type
	quantity: integer
	quality: Enum of strings
```

#### Examples

| Type        | Quantity | Quality |
| ----------- | -------- | ------- |
| Water       | 1000     |         |
| Metal sheet | 1000     | Normal  |


# More to add
- Composite resources, how do we handle things like "muddy water" which we'd want to be able to filter.
	- Composites need to be able to have different compositions, different harvests will have different quantities of minerals
	- Composites need to have the ability to have their contents hidden, e.g. you have muddy water but you don't know what the mud is
