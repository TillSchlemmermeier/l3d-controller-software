# l3d-controller-software

## Introduction

![Flowchart](/flowchart.png)

## Generators

Seven "Generators" are included at the moment. Generators return a new world when called. Each generator can be controlled with up to three knobs/parameters. *Cursive* written generators are untested.
The generators are called at each step by thier "generate" routine, which gets the current step and the world as input. The last is usually not used by the generators, but has to be passed to be consistent.

- *g_cube*
- *g_growing_sphere*
- *g_orbiter*
- *g_random*
- *g_randomlines*
- *g_shooting_star*
- *g_sphere*
- *g_snake*

Example in an effect class:

'''def generate(self, step, dumpworld):'''

Example for call, the generator is stored in the list self.CHA:

'''for i in self.CHA:
    self.world_CHA = i.generate(step, self.world_CHA)'''


## Effects

- *fade2blue*
- *rotate* (planned)
- *move* (planned)
- *oscillate* (planned, change brightness periodically)

## Mapping of Midi Keys

16 | 20 | 24 | 28 | 46 | 50 | 54 | 58		
17 | 21 | 25 | 29 | 47 | 51 | 55 | 59
18 | 22 | 26 | 30 | 48 | 52 | 56 | 60
19 | 23 | 27 | 31 | 49 | 53 | 57 | 61 | 62
