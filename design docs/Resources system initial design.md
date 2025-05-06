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
A [[Resources system]] underpins almost every aspect of an economic system and several more to boot. We want to have a flexible resource system allowing for complexity and depth without requiring either. A list of functional behaviour we want to enable is:
- Presence in a physical location (e.g. station, ship etc)
- Transfer resources from one storage to another at the same location (e.g. ship docked at a station)
- Transport resources between locations by having the container (e.g. ship) travel
- Varying storage requirements such as mass, volume and specialised containers (though not limited to just these)
- Affecting of resources over time (e.g. [[spoilage]])
- Some resources in theory be the same but actually contain different parts (e.g. ores mined from two different locations)

# Proposed data

## Normal resources
The bread and butter of the resource system, tracking the resources possessed by every entity.

### Resource types
These represent information regarding a given resource which is then referenced by instances of the resource.
- **name**: `string`
- **mass**: `integer`
- **volume**: `integer`
- **tags**: `array of string` (things like "liquid" and "combustible" along with additional behaviours/restrictions we want to add later), see [[#Tagged behaviours]] for more info

#### Examples

| Name       | Mass | Volume | Tags                       |
| ---------- | ---- | ------ | -------------------------- |
| Water      | 1    | 1      | liquid                     |
| Iron ore   | 3    | 1      |                            |
| Dynamite   | 100  | 20     | explosive, combust-in-heat |
| Iron sheet | 400  | 10     |                            |
| Plants     | 400  | 100    | needs-atmosphere, delicate |

### Resource instances
Representing a specific instance of a resource existing. If two instances are combined then one would be deleted. It is expected within the database the instances will be further broken down by location type (e.g. ship or station).

- **type**: `resource_type`
- **quantity**: `integer`

#### Examples

| Type       | Quantity |
| ---------- | -------- |
| Water      | 1000     |
| Iron sheet | 1000     |

## Composite resources
Composite resources represent a resource with two or more components making up the actual content of the resource. For example, extracting ferrous ores will yield you iron but there will be other elements there too. These will be present and depending on equipment and resources can be identified (or possibly be known from the outset if surveys take place).

These compositions can vary in both content (one asteroid might have carbon and iron, another might have oxygen and iron) and in quantities (one is rich in iron, another poor). We will need a way to represent this.

### Composite types
- **name**: `string`
- **contents**: `array of resource_type_id`

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

- **type**: `composite_type_id`
- **ratios**: `array of integer`
- **quantity**: `integer`
- **combined_mass**: `integer`
- **combined_volume**: `integer`

The ratios added together represent the whole allowing for more precise fractions without having to use floating point numbers.

Combined values represent cached calculations of the elements of the composition to prevent having to be re-calculated every time a common request needs to be made.

#### Examples
In these examples each type refers to the first of that name; within the database it would use an id value allowing for multiple composites of the same name but with different compositions to exist.

| Type        | Ratios       | Quantity | Combined mass | Combined volume |
| ----------- | ------------ | -------- | ------------- | --------------- |
| Ferrous Ore | 400, 100, 50 | 1000     | 1000          | 100             |
| Ferrous Ore | 800, 100, 50 | 1000     | 1300          | 100             |

## Tagged behaviours
The purpose of the tags is to allow overlapping behaviours to be defined for different resource types. It is intended new behaviours can be added without overhauling the entire system without needing to plan out it completely at this stage.

#### Examples
- `liquid` - Liquids require different containers for both storage and transfer.
- `combust-in-heat` - If exposed to heat this resource will explode, how we track the amount of damage it does is not certain at this stage
- `explosive` - If part of an explosion this will increase the explosion, as with the combust in heat I'm not sure how we'd want to handle the contributions being made
- `needs-atmosphere` - Must be stored in a container with an atmosphere
- `delicate` - Slow to transfer, maybe must be stored in a specifically designed container

It is possible we could use tags with numbers such as `explosive1`, `explosive2` etc to denote levels of a tag and how it should be used within the relevant functions.

#### Examples of other tags we might use
- [Hazard types](https://hsewatch.com/types-of-hazards/)

# Future additions
We currently want to have the following things as components of the resources system but without a better understanding of how other systems will work we will not define them fully at this stage. Instead we will outline a current ambition for them and revisit them later.

### Hidden contents
We want to allow players to be able to mine raw materials without knowing their exact composition, indeed we will likely want to have varying degrees of understanding of the contents of a resource, e.g.
- Asteroid
- Iron/Nickel asteroid
- Iron/Nickel asteroid with small amounts of Titanium and Cobalt
- Iron 40%, Nickel 30% asteroid with small amounts of Titanium and Cobalt
- A full breakdown of the resources in the asteroid

That is just one example, another would be where a spy has information on a "metal ore" being transported but without knowing the actual composition of the ore.

This means we will need to have the fully information stored in the entity (so regardless of what you know, you're getting the same result, we don't roll for discovery when you observe it) but with different levels of understanding about it.

To my mind this is the same pattern as a permissions system where different groups have access to differing amounts of information about it. By combining that access level and the composition data the game is able to generate textual information for the player.

### Spoilage
Spoilage is the function of transforming a resource from one type to another given time and conditions. Some examples include:
- Food spoiling if not refrigerated or frozen
- Radioactive materials decaying over time
- Delicate materials breaking if shaken or not stored correctly
- Pressurised resources leaking if stored in a poor quality container

This will likely entail storing additional information about resources and should be approached carefully.

#### Example spoilage systems
- [[Factorio]] - https://wiki.factorio.com/Spoilage
- [[Rimworld]] - https://rimworldwiki.com/wiki/Food#Degradation and https://rimworldwiki.com/wiki/Deterioration

### Quality
We have already said we would like to have a quality system in place but designing one at this stage would likely result in something not quite fit for purpose. The intent of adding a quality system is to reward specialisation (you make higher quality goods if you're a specialist) while still allowing players to produce many things.

#### Example quality systems
- [[Factorio]] - https://wiki.factorio.com/Quality
- [[Rimworld]] - https://rimworldwiki.com/wiki/Quality
