---
layout: default
title:  Status
---

The goal of our project is to implement an agent that kills ships in as little time as possible (initial goal was to add skeletons that would do so, but we changed that idea). The agent sees the whole field and knows where the ships are. One might think that there is a algorithmic solution to this problem that does not require machine learning, but that would be wrong because our problem is essentially equivalent to traveling salesman problem that says:

  Given a list of cities and the distance between each pair of cities, what is the shortest possible route to visit all the cities and return to the original location.

That problem is NP-hard, which essentially means there is no fast algorithm to solve it. Thus, we weer curious if we can come up with AI agent that solves similar problem in our environment.

The agent in our implementation can see the whole field, on which there are n ships. We use reinforcement learning (Q-learning) to stimulate the agent to kill ships (and give positive reward for doing so). One strike is enough for an agent to kill a ship. 

For n ships, there are $\frac{((3 * 3 + 1)^n}{n!)}$ states. For each ship we recognize four steps - ship is close to us, ship is in mid-range, the ship is far, far away and the ship is dead. For the ship that is alive we also take the angle of the ship as related to our vision: either directly in front of us (from -45 to 45 degrees), to the left (from 180 to 45) or to the right (from -180 to -45). Because as far as our agent is concerned the ships are identical, we sort the array of ships from closest to farthest, which is why it is divided by n!. For each steps there are 4 steps our agent chooses from - move straight, turn 45, 90, 135, 180, 225, 270 and 315 degrees or strike. We reinforce killing of the ship so that the agent attempts to do that.

As for performance, our goal was to minimize time. The learning speed of our algorithm is rather slow, which is understandable considering that it needs to find and kill a ship in order to at least start understanding of what is happening. We have tried training it for 12 hours and the average speed at which the agent kills all the sheeps dropped 30%. We have tried several optimizations, including:

	-First training it to kill only one sheep, then two, then three, etc...
		That did not work well because he needs to figure out how to deal with every new number of sheeps from scratch
	-Give agent some reward for reducing the average distance between him and all the sheeps
		That actually was a fairly stupid idea because he ended up just standing in the center
	-Giving agent some reward for approaching the nearest sheep
		That actually worked, but our algorithm started to always get to the closes sheep, which is not that interesting (it is not always the best strategy and one do not require machine learning to do that)

In the future, we want to try a different strategy - instead of having an agent choose an action, we will want to try it choosing a sheep and then following the shortest path to it. That might be a lot better in terms of the speed of learning.