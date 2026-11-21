<!-- layout: stage | where: app -->
<p class="kicker">Part 2 · Measure</p>

# The menu

| Measure | It asks | It can't tell you |
|---|---|---|
| `park_sun` | How much of the park's sun does the tower take? | Any day but 21 March · where people sit |
| `neighbours_sun` | How much sun do the buildings around it lose? | Which neighbour · where the windows are |
| `river_view` | How much of the tower do people on the river see? | Whether they notice it |
| `terraces` | How much open roof do the floors leave? | Whether a terrace is usable |

<!-- notes -->
Each measure is a Grasshopper tool in the `measures` kit, with a contract in the same folder. The contract lists its inputs, the rule, its outputs, its test cases, and a row to paste into your skill with a starting limit.

- **`park_sun`** (Ladybug): sun lost on the park on 21 March, in %.
- **`neighbours_sun`** (Ladybug): the same for the walls and roofs of the five neighbouring blocks. It averages all five, so a big loss on one wall can hide behind four untouched buildings: look at its sun map.
- **`river_view`** (Ladybug): the area of the tower, in m², that a person at an average river viewpoint can see, with the neighbours in the way. Seeing works both ways, so this is also how much of the tower looks out at the river.
- **`terraces`** (plain Grasshopper): the open roof each floor leaves where the floor above steps back, shifts or turns, in m², and the largest single piece.

The terraces measure shows how a measure can reward the wrong thing. A tower that tapers from 20 m to 10 m wide over 30 floors leaves 300 m² of terraces. A tower twisted 90° leaves almost as much, 298 m². Neither has a terrace you could stand on: the taper narrows each floor by 17 cm a side, so its terraces are rings 17 cm deep, and the twist leaves 116 corner slivers. `largest_terrace_m2` tells the twist (2.6 m²) from the taper (13.7 m²), but a 13.7 m² ring 17 cm deep is no more usable. What would catch it is the depth of a terrace, which this measure doesn't report. A tower that leans 40 m over 20 floors shifts each floor 2.1 m, and leaves strips 2.1 m deep: those you could use.
