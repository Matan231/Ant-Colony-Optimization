# Ant Colony Optimization
using the ACO method in two use cases.
1. a good solution for the traveling sales man problem (TSP)
2. using the ACO to order a Playlist of songs s.t the transitions between songs will be as smooth as possible
## ACO method
Initially proposed by Marco Dorigo in 1992 in his Ph.D. thesis.
the first algorithm was aiming to search for an optimal path in a graph.

The ACO algorithm is an optimization algorithm, recognized for being very efficient in
problems of finding routes and planning paths in roads. In terms of the problem of the
traveling salesman, ACO algorithm has been able to find optimal solutions to the problem.
### the general algorithem
```
procedure ACO_MetaHeuristic is
    while not terminated do
      generateSolutions()
      Local_search()
      pheromoneUpdate()
    repeat
end procedure
```

**the algorithem has 3 main parts:**
1. a group of ants generates feasible solutions by traversing the graph
2. Localsearch() - usually a local search to generate better solutions also known as deamon action
3. update the pheromones on the edges of the graph increasing the amount at the good solutions path
   and evaporate pheromones by some rate from all the edges.
   
### generate solutions
single ant next node local selection
To select the next node in its tour, an ant will consider the length of each edge
available from its current position, as well as the corresponding pheromone level
**each ant k computes a set Ak(x) of feasible expansions to its current
state in each iteration, and moves to one of these in probability.**
![image](https://user-images.githubusercontent.com/25345730/154714640-c743e88a-c5ad-419b-b8ec-2023420f3565.png)

- **tau** is the amount of pheromone deposited for transition from state x to y (xy).
- **alpha** is a parameter to control the influence of tau at xy.
- **eta** is the desirability of state transition xy (a priori knowledge, typically 1/d at xy, where d is the distance).
- **beta** is a parameter to control the influence of eta at xy.

### ants full path solution
1. an ant will keep touring the graph until no more feasible nodes
can be visited.
while choosing the next node by its probability
2. iterate this process for m ants (usually 10 - 20 ants)

### local search (Deamon action)
local search is a heuristic method for solving optimization problems.
Local search algorithms move from solution to solution in the space of candidate solutions (the search space) by applying local changes

the 2-opt algorithm is a simple local search algorithm for solving the traveling salesman problem.

The main idea behind it is to take a route that crosses over itself and reorder it so that it does not.

A complete 2-opt local search will compare every possible valid combination of the swapping mechanism.

![image](https://user-images.githubusercontent.com/25345730/154715565-47f985d0-beb7-41ac-8ccd-2e5682000478.png)
### update pheromones
Trails are usually updated when all ants have completed their solution,
increasing or decreasing the level of trails corresponding to moves that were
part of "good" or "bad" solutions

* ρ is the evaporation rate
![image](https://user-images.githubusercontent.com/25345730/154715913-690eaca9-7d02-4b6f-ab2f-b4aabeceede7.png)
![image](https://user-images.githubusercontent.com/25345730/154715945-adab97e0-13a4-44bb-9974-b21b35845600.png)

## Ant Colony System (ASC)

**In the ant colony system algorithm, the original ant system was modified in three aspects:**

1. the edge selection is biased towards exploitation (favoring the
selection of the shortest edges with a large amount of pheromone)

2. while building a solution, ants change the pheromone level of the
edges they are selecting by applying a local pheromone updating
rule.

3. at the end of each iteration, only the best ant is allowed to update
the trails by applying a modified global pheromone updating rule.

### (1.) State transition rule
**In the ACS the state transition rule is as follows:**
an ant positioned on a node chooses the city to move to
by applying the rule given by:
![image](https://user-images.githubusercontent.com/25345730/154716976-c695e425-abc7-418e-ac56-3cee150829ac.png)

where q0 is a parameter s.t 0 < q0 < 1 and q is choosen from a uniform distribution between 0 to 1.
**The parameter determines the relative importance of exploitation versus exploration**:
every time an ant in a city has to choose a city to move to, it samples a random number.

If q<=q0 the best edge is chosen (exploitation),
otherwise an edge is chosen according to AS previews function (biased exploration).

### (2.) ocal pheromone update
The most interesting contribution of ACS is probably the introduction of a local pheromone update in addition to the
pheromone update performed at the end of the construction process.

The local pheromone update is performed by all the ants after each construction step by the rules:
![image](https://user-images.githubusercontent.com/25345730/154717421-d3339085-45b9-45b5-a84d-e644641b6a8f.png)
![image](https://user-images.githubusercontent.com/25345730/154717452-0fdfdc8a-d96d-426a-9d16-e1af1de5d559.png)

where n is the number of nodes and Lnn is the total distance of a greedy TSP algorithm.

The main goal of the local update is to diversify the search performed by subsequent
ants during an iteration by decreasing the pheromone concentration on the traversed edges.
### (3.) ACS Global Updating Rule
**only the globally best ant (i.e., the ant which constructed the shortest tour from the beginning of the trial) is allowed to deposit pheromone.**
This choice, together with the use of the first rule, is intended to make the search more directed:
ants search in a neighborhood of the best tour found
**The pheromone level is updated by applying the global updating rule of:**
![image](https://user-images.githubusercontent.com/25345730/154718108-52700688-f276-4098-ad9b-1d9b367caee9.png)
![image](https://user-images.githubusercontent.com/25345730/154718162-a1319f8f-f82a-479c-b3c2-732a9f30058e.png)




## TSP
### results compersion

**A known set of real coordinantes in real cities**
link to the dataset of the coordinantes: http://elib.zib.de/pub/mp-testdata/tsp/tsplib/tsp/


**Berlin52 my result's**
![image](https://user-images.githubusercontent.com/25345730/154718389-a008ca0a-818a-46d1-ac89-5ea42767fe1d.png)
![image](https://user-images.githubusercontent.com/25345730/154718437-43727b2a-f6e9-4703-ae97-dd1d514a0867.png)
**berlin52 real optimal**
![image](https://user-images.githubusercontent.com/25345730/154718471-c7cf5525-092d-429f-b304-601626c9fedf.png)

**chn144 my result**
![image](https://user-images.githubusercontent.com/25345730/154718729-566ec860-4757-420b-a992-1855b815a374.png)
![image](https://user-images.githubusercontent.com/25345730/154718740-b7b72dde-f539-445c-8190-597372d60df6.png)

**chn144 real optimal**
![image](https://user-images.githubusercontent.com/25345730/154718760-285069f2-996c-4bbc-bf26-857f150d0fa2.png)

**A280 my result**
![image](https://user-images.githubusercontent.com/25345730/154718972-2a2498f5-0fef-4865-b451-1ebf99e74e6f.png)
![image](https://user-images.githubusercontent.com/25345730/154718994-21483b58-00fc-49a5-9216-c680c62df3f3.png)
**A280 optimal**
![image](https://user-images.githubusercontent.com/25345730/154719053-e1e986b0-e43a-4ac8-b7e0-ed6d4655e8c7.png)



## Playlist ordering (smart Random)
Spotify smoothest playlist playing order
### The main idea:
to generate a good smooth playing order of the songs in a given playlist.
we can do so by measuring how similar two songs are and give this property a scaler number.
in other words, we can measure the distance between any 2 songs, so we can come back to the TSP problem.

in this case, we will minimize the changes between songs that sounds different, and by that make our playing order sound smooth and with less abrupt changes.
### The songs features
Spotify uses some features from the audio tracks to analyze the songs
with this data, we can measure the distance between each of the songs.

**Python can be used to acquire the data using the library Spotipy**

### the songs features
**some of the features:**
- **bpm**: beat per minutes the tempo of the song
- **Instrumentalness**: This value represents a measure of the vocals in the song. The closer it is to 1.0, the more instrumental the song is.
- **Acousticness**: This value describes how acoustic a song is. A score of 1.0 means the song is most likely to be an acoustic one.
- **Liveness**: This value describes the probability that the song was recorded with a live audience.
  According to the official documentation “a value above 0.8 provides strong likelihood that the track is live”.
- **Speechiness:** “Speechiness detects the presence of spoken words in a track”. If the speechiness of a song is above 0.66, it is probably made of spoken words, 
  a score between 0.33 and 0.66 is a song that may contain both music and words, and a score below 0.33 means the song does not have any speech.
- **Danceability**: “Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability,
  beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable”.

![image](https://user-images.githubusercontent.com/25345730/154721633-5c8a7980-4392-4a1c-929f-95fdcaab861a.png)



