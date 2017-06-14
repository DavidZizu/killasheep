---
layout: default
title:  Final
---

## Project Summary

The goal of our project, although changed a couple of times, may be summarized as exploring various ways in which an actor can kill a sheep in Minecraft. We have separated this task in two subtasks: the first was to make an agent kill all the sheeps as quick as possible with it knowing the locations of the sheeps and the other was to kill the sheeps (although possible not optimally) with the agent only seeing the world as the player would.

The first subtask was focused around q-learning. The agent lives in the world where it can choose a sheep and then choose which sheep to chase. Once the sheep is chosen, the agent deterministically moves toward the sheep by turning by 90 degrees left or right or moving forward. After doing the step, the agent can choose the sheep it wants to follow again (i.e. it can change the decision after each step). We were curious to see whether the agent using q-learning will learn to chase one sheep and stay on it (instead of changing its decision every time) and how scalable the model will be (how many sheeps it can handle). Moreover we were curious to see whether it will choose the closest sheep or adopt any more optimal algorithm.

The second subtask was to do the same, but with agent not seeing the entire field now, but instead having just a picture like a real human player would. This task has obviously to do with computer vision and how to train AI to recognize sheeps in the field of vision. We were curious as to whether we could train the model that would adequately recognize whether there is a sheep in the frame or not.



## Approaches

### First sub-problem

For our first sub-problem we have used q-learning. The state in q-table is a tuple, which length equals to the number of live sheep on the field. Each element is the distance between the agent and the sheep quantified in the three categories - very close, close and quite far. For example, if there were four sheeps on the field and one was close and the rest were quite far, the state would be (close, far, far, far). The actions available are choose_sheep_1, choose_sheep_2, choose_sheep_3, ..., choose_sheep_n for n sheeps. Once the agent has picked a sheep, he deterministically (or without any machine learning) moves towards it, depending on the angle between agent's current direction and the sheep and the distance or hits it. After this action is completed, the agent gets rewarded (+100) if one sheep was killed in a previous action and punished (-2) if the action was performed and the sheep was not killed. This reward system is supposed to reinforce killing the sheep and punish switching the target all the time and just wandering around as the result.

That is quite an improvement from the version that we have submitted for our report, which had way to many states (27^n, where n is a number of sheeps) and thus never actually learned. Moreover, our previous version had (move, hit, turn 45 degrees, turn 90 degrees, turn 125 degrees, ...) as a set of action, which created way to many possible scenarios and made it impossible for an agent to "figure out" what it needs to do.

### Second sub-problem

For our second sub-problem we indented to divide the image that is displayed on the screen by Minecraft and cut it into 9 equal squares (in a 3x3 grid) (from now on I am going to call each of these squares a "little square"). Then, we would use a bag of models (several predictors) to estimate where there is a sheep in this square. We used supervised training and trained our model on 200 little squares that contained the part of the sheep and 200 little squares that did not. We then have tested the precision of the model on the total of 25 little squares with a sheep and 25 without one and estimated the precision of each of our trained model.

We have tried multiple classifiers, including various configurations of the neural networks. Out best configuration of the neural network (stochastic gradient descent, 7 internal layers) and gave the precision of 78% and this neural network was eventually included in the bag. We have also included support vector machine (which had a precision of 83% in out dataset) and a Gaussian Process classifier, which had the precision of 91%. We also considered some other classifier, including K-nearest-neighbor, the precision of which was sad (about 50%).

We have used scikit-learn in order to get off-the-shelf classifier in order not to write it ourselves. Moreover, images has been processed - transfered to greyscale and reduced to size 28x28 for (obviously) both training and prediction. The bag I referred to above works using a vote: if all three models decide that there is a sheep in a little square, it is considered to be very credible. If there two predictors say that there is a sheep, it is considered quite credible, but less credible nonetheless. Depending on which square we have found the sheep in, our agent moves forward or turns deterministically.



## Evaluation

### First sub-problem

We have used q-learning in order to train our agent perform well in the conditions described above. The obvious measure of the performance is the time it took to kill all the sheeps on the field. The following graph represents the average time it took to kill 2 sheeps on a field over 5 consequent attempts (i.e. f(x=1) = average time of attempts 1 to 5, f(x=2) = average time of attempts 5-10, etc.)



The following graph represents the same for three sheeps spawned on the field (it obviously takes longer to learn the optimal strategy, but that still happens):


There is an obvious trend toward reducing the time it took to kill a sheep in a second graph. We have compared the time with the same agent, but which chose random sheep and it took it about 40 seconds to kill two sheeps and about 5 minutes to kill three sheeps. On the video, we can clearly see that an agents tends to choose the closest sheep (and that is kind of cool that it has learned this tactic all by itself!)

### Second sub-problem

The only reasonable measure of success we can think of is the rate of our system being correct on some sample test (we have used 100 test pictures, 50 positive and 50 negative). The total bag was correct on 90% of our testing pictures. However, we could not properly estimate the sheep location so that we know when to hit; thus on the video it is not possible to see the agent actually hit the sheep, but it is clearly possible to see it follow one (although not as closely as we wish it did, which may be because of insufficient size of training set and human bias towards what constitutes a presence of the sheep in a little square (is part of the sheep good enough?)).

## Video

<iframe width="560" height="315" src="https://www.youtube.com/embed/1QiUOO8TrLw?ecver=1" frameborder="0" allowfullscreen></iframe>

## Images
<img src="https://files.torba.me/1.png"/>


<img src="https://files.torba.me/2.png"/>


## References

We have used multiple on-line resources to learn about models and to figure out whether our models were appropriate for the task. Here are the resources we used:

https://en.wikipedia.org/wiki/Q-learning

http://scikit-learn.org/stable/auto_examples/classification/plot_classifier_comparison.html

http://scikit-learn.org/stable/modules/generated/sklearn.gaussian_process.GaussianProcessClassifier.html#sklearn.gaussian_process.GaussianProcessClassifier

http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html#sklearn.neighbors.KNeighborsClassifier

http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html#sklearn.svm.SVC

http://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html#sklearn.neural_network.MLPClassifier

http://proceedings.mlr.press/v48/oh16.pdf