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

## Normal resources
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

## Composite resources
Composite resources represent a resource with two or more components making up the actual content of the resource. For example, extracting ferrous ores will yield you iron but there will be other elements there too. These will be present and depending on equipment and resources can be identified (or possibly be known from the outset if surveys take place).

These compositions can vary in both content (one asteroid might have carbon and iron, another might have oxygen and iron) and in quantities (one is rich in iron, another poor). We will need a way to represent this.

### Composite types
```
	name: string
	contents: array of resource_type_id
```

#### Examples

| Name        | Contents                      |
| ----------- | ----------------------------- |
| Ferrous ore | Iron, Carbon, Boron           |
| Ferrous ore | Iron, Carbon, Boron, Titanium |
| Frozen ore  | Water, Hydrogen, Oxygen       |
| Frozen ore  | Water, Hydrogen, Helium       |
As we can see a composite type only tracks a list of resource types present in that composition.

### Composite instances
A composite instance represents the composite resource existing at a location in the game similar to a normal resource instance. The main difference is it has some combined properties based on the composition.

```
	type: composite_type_id
	ratios: array of integer
	quantity: integer
	combined_mass: integer
	combined_volume: integer
```

The ratios added together represent the whole allowing for more precise fractions without having to use floating point numbers.

Combined values represent cached calculations of the elements of the composition to prevent having to be re-calculated every time a common request needs to be made.

#### Examples
In these examples each type refers to the first of that name; within the database it would use an id value allowing for multiple composites of the same name but with different compositions to exist.

| Type        | Ratios       | Quantity | Combined mass | Combined volume |
| ----------- | ------------ | -------- | ------------- | --------------- |
| Ferrous Ore | 400, 100, 50 | 1000     | 1000          | 100             |
| Ferrous Ore | 800, 100, 50 | 1000     | 1300          | 100             |



# Things still unceratin
- Composites need to have the ability to have their contents hidden, e.g. you have muddy water but you don't know what the mud is. This strikes me as something we can do after implementing the resource system as opposed to being part of it. Gut feeling tells me it's the same pattern as an authorisation issue (permissions come from doing scans etc).
- Do we need both mass and volume?
