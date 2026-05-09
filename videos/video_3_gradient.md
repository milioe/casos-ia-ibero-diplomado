Gradient Descent is decent at estimating parameters. StatQuest!
Hello!
I'm Josh Starmer and welcome to StatQuest.
Today we're going to learn about Gradient Descent and we're going to go through the algorithm step by step.
Note: this StatQuest assumes you already understand the basics of least squares and
linear regression, so if you're not already down with that, check out the Quest.
In statistics, machine learning, and other data science fields, we optimize a lot of stuff.
When we fit a line with linear regression, we optimize the intercept and the slope.
When we use logistic regression, we optimize a squiggle. And when we use t-SNE, we optimize clusters.
These are just a few examples of the stuff we optimize, there are tons more.
The cool thing is that Gradient Descent can optimize all these things, and much more.
So, if we learn how to optimize this line using Gradient Descent, then we'll have
learned the strategy that optimizes this squiggle, and these clusters, and many more
of the optimization problems we have in statistics, machine learning, and data science.
So let's start with a simple data set.
On the x-axis we have weight.
On the y-axis we have height.
If we fit a line to the data and someone tells us that they weigh 1.5, we can use
the line to predict that they will be 1.9 tall.
So let's learn how Gradient Descent can fit a line to data by finding the optimal values for the intercept and the slope.
Actually, we'll start by using Gradient Descent to find the intercept.
Then, once we understand how Gradient Descent works, we'll use it to solve for the intercept and the slope.
So, for now, let's just plug in the Least Squares estimate for the slope, 0.64, and
we'll use Gradient Descent to find the optimal value for the intercept.
The first thing we do is pick a random value for the intercept.
This is just an initial guess that gives Gradient Descent something to improve upon.
In this case, we'll use 0, but any number will do.
And that gives us the equation for this line.
In this example, we will evaluate how well this line fits the data with the sum of the squared residuals.
Note: in machine learning lingo, the sum of the squared residuals is a type of Loss Function.
We'll talk more about Loss Functions towards the end of the video.
We'll start by calculating this residual.
This data point represents a person with weight 0.5 and height 1.4. We get the predicted
height, the point on the line, by plugging weight equals 0.5 into the equation for the line.
And the predicted height is 0.32.
The residual is the difference between the observed height and the predicted height,
so we calculate the difference between 1.4 and 0.32, and that gives us 1.1 for the residual.
Here's the square of the first residual.
The second residual is 0.4. and the third residual is 1.3. In the end, 3.1 is the sum of the squared residuals.
Now, just for fun, we can plot that value on a graph.
This graph has the sum of squared residuals on the y-axis, and different values for the intercept on the x-axis.
This point represents the sum of the squared residuals when the intercept equals zero.
However, if the intercept equals 0.25, then we would get this point on the graph.
And if the intercept equals 0.5, then we would get this point.
And for increasing values for the intercept we get these points.
Of the points that we calculated for the graph, this one has the lowest sum of squared residuals.
But is it the best we can do?
What if the best value for the intercept is somewhere between these values?
A slow and painful method for finding the minimal sum of the squared residuals is
to plug and chug a bunch more values for the intercept.
Don't despair!
Gradient Descent is way more efficient.
Gradient Descent only does a few calculations far from the optimal solution, and increases
the number of calculations closer to the optimal value.
In other words, gradient descent identifies the optimal value by taking big steps
when it is far away, and baby steps when it is close.
So let's get back to using gradient ascent to find the optimal value for the intercept, starting from a random value.
In this case, the random value was zero.
When we calculated the sum of the squared residuals, the first residual was the difference
between the observed height, which was 1.4, and the predicted height, which came from the equation for this line.
So we replace predicted height with the equation for the line.
Since the individual weighs 0.5 we replace weight with 0.5. So, for this individual,
this is their observed height and this is their predicted height.
Note: we can now plug in any value for the intercept and get a new predicted height.
Now let's focus on the second data point.
Just like before, the residual is the difference between the observed height, which
is 1.9, and the predicted height, which comes from the equation for the line.
Snd since this individual weighs 2.3, we replace weight with 2.3.
Now let's focus on the last person.
Again, the residual is the difference between the observed height, which is 3.2, and
the predicted height, which comes from the equation for the line.
And since this person weighs 2.9, we'll replace weight with 2.9.
Now we can easily plug in any value for the intercept and get the sum of the squared residuals.
Thus, we now have an equation for this curve, and we can take the derivative of this
function and determine the slope at any value for the intercept.
So let's take the derivative of the sum of the squared residuals with respect to the intercept.
The derivative of the sum of the squared residuals with respect to the intercept equals
the derivative of the first part, plus the derivative of the second part, plus the derivative of the third part.
Let's start by taking the derivative of the first part.
First, we'll move this part of the equation up here, so that we have room to work.
To take the derivative of this we need to apply the chain rule.
So we start by moving the square to the front and multiply that by the derivative of the stuff inside the parentheses.
These parts don't contain a term for the intercept, so they go away.
Then we simplify by multiplying two by negative one.
And this is the derivative of the first part, so we plug it in.
Now we need to take the derivative of the next two parts.
I'll leave that as an exercise for the viewer.
Bam!
Let's move the derivative up here, so that it's not taking up half the screen.
Now that we have the derivative, Gradient Descent will use it to find where the sum of squared residuals is lowest.
Note: if we were using least squares to solve for the optimal value for the intercept,
we would simply find where the slope of the curve equals zero.
In contrast gradient descent finds the minimum value by taking steps from an initial guess until it reaches the best value.
This makes Gradient Descent very useful when it is not possible to solve for where
the derivative equals zero. And this is why Gradient Descent can be used in so many different situations.
Bam!
Remember, we started by setting the intercept to a random number.
In this case that was zero.
So we plug zero into the derivative and we get negative 5.7. So, when the intercept
equals 0, the slope of the curve equals negative 5.7. Note: the closer we get to
the optimal value for the intercept, the closer the slope of the curve gets to zero.
This means that when the slope of the curve is close to zero, then we should take
baby steps, because we are close to the optimal value.
And when the slope is far from zero, then we should take big steps because we are far from the optimal value.
However, if we take a super, huge step, then we would increase the sum of the squared residuals.
So the size of the step should be related to the slope, since it tells us if we should take a baby step or a big step.
But we need to make sure the big step is not too big.
Gradient Descent determines the step size by multiplying the slope by a small number called the learning rate.
Note: we'll talk more about learning rates later.
When the intercept equals 0, the step size equals negative 5.7. With the step size, we can calculate a new intercept.
The new intercept is the old intercept minus the step size.
So we plug in the numbers, and the new intercept equals 0.57.
Bam!
In one big step, we moved much closer to the optimal value for the intercept.
Going back to the original data and the original line, with the intercept equals 0,
we can see how much the residuals shrink when the intercept equals 0.57.
Now let's take another step closer to the optimal value for the intercept. To take
another step, we go back to the derivative and plug in the new intercept, and that
tells us the slope of the curve equals negative 2.3.
Now let's calculate the step size.
By plugging in negative 2.3 for the slope, and 0.1 for the learning rate, ultimately
the step size is negative 0.23. And the new intercept equals 0.8.
Now we can compare the residuals when the intercept equals 0.57 to when the intercept equals 0.8.
Overall the sum of the squared residuals is getting smaller.
Notice that the first step was relatively large, compared to the second step.
Now let's calculate the derivative at the new intercept: and we get negative 0.9.
The step size equals negative 0.09, and the new intercept equals 0.89.
Now we increase the intercept from 0.8 to 0.89, then we take another step and the
new intercept equals 0.92. And then we take another step, and the new intercept equals
0.94. And then we take another step, and the new intercept equals 0.95.
Notice how each step gets smaller and smaller the closer we get to the bottom of the curve.
After six steps, the gradient ascent estimate for the intercept is 0.95.
Note: the least squares estimate for the intercept is also 0.95.
so we know that gradient descent has done its job, but without comparing its solution
to a gold standard, how does gradient descent know to stop taking steps?
Gradient Descent stops when the step size is very close to zero.
The step size will be very close to zero when the slope is very close to zero.
In practice, the minimum step size equals 0.001 or smaller.
So if this slope equals 0.009, then we would plug in 0.009 for the slope and 0.1 for
the learning rate and get 0.0009, which is smaller than 0.001, so gradient descent would stop.
That said, gradient descent also includes a limit on the number of steps it will take before giving up.
In practice, the maximum number of steps equals 1000 or greater.
So, even if the step size is large, if there have been more than the maximum number of steps, gradient descent will stop.
Okay, let's review what we've learned so far.
The first thing we did is decide to use the sum of the squared residuals as the loss
function to evaluate how well a line fits the data.
Then, we took the derivative of the sum of the squared residuals. In other words,
we took the derivative of the loss function.
Then, we picked a random value for the intercept, in this case we set the intercept to be equal to zero.
Then, we calculated the derivative when the intercept equals zero, plugged that slope
into the step size calculation, and then calculated the new intercept, the difference
between the old intercept and the step size.
Lastly, we plugged the new intercept into the derivative and repeated everything until step size was close to zero.
Double bam!
Now that we understand how gradient descent can calculate the intercept, let's talk
about how to estimate the intercept and the slope.
Just like before, we'll use the sum of the squared residuals as the loss function.
This is a 3D graph of the loss function for the different values for the intercept and the slope.
This axis is the sum of the squared residuals, this axis represents different values
for the slope, and this axis represents different values for the intercept.
We want to find the values for the intercept and slope that give us the minimum sum of the squared residuals.
So, just like before, we need to take the derivative of this function.
And just like before, we'll take the derivative with respect to the intercept.
But, unlike before, we'll also take the derivative with respect to the slope.
We'll start by taking the derivative with respect to the intercept.
Just like before, we'll take the derivative of each part.
And, just like before, we'll use the chain rule and move the square to the front,
and multiply that by the derivative of the stuff inside the parentheses.
[Music] Since we are taking the derivative with respect to the intercept, we treat
the slope like a constant, and the derivative of a constant is zero.
So, we end up with negative one, just like before.
Then we simplify by multiplying two by negative one.
And this is the derivative of the first part.
So we plug it in.
Likewise, we replace these terms with their derivatives.
So this whole thing is the derivative of the sum of squared residuals with respect to the intercept.
Now let's take the derivative of the sum of the squared residuals with respect to the slope.
Just like before, we take the derivative of each part and, just like before, we'll
use the chain rule to move the square to the front and multiply that by the derivative of the stuff inside the parentheses.
Since we are taking the derivative with respect to the slope, we treat the intercept
like a constant and the derivative of a constant is zero.
So we end up with negative 0.5. Then we simplify by moving the negative 0.5 to the front.
Note: I left the 0.5 in bold instead of multiplying it by 2 to remind us that 0.5 is the weight for the first sample.
And this is the derivative of the first part.
So we plug it in.
Likewise, we replace these terms with their derivatives.
Again, 2.3 and 2.9 are in bold to remind us that they are the weights of the second and third samples.
Here's the derivative of the sum of the squared residuals with respect to the intercept,
and here's the derivative with respect to the slope.
Note: when you have two or more derivatives of the same function they are called a gradient.
We will use this gradient to descend to the lowest point in the loss function, which,
in this case, is the sum of the squared residuals.
Thus, this is why the algorithm is called Gradient Descent.
Bam!
Just like before, we'll start by picking a random number for the intercept. In this
case, we'll set the intercept to be equal to zero, and we'll pick a random number for the slope.
In this case we'll set the slope to be 1.
Thus, this line, with intercept equals 0 and slope equals 1, is where we will start.
Now, let's plug in 0 for the intercept and 1 for the slope.
And that gives us two slopes.
Now, we plug the slopes into the step size formulas, and multiply by the learning rate, which this time we set to 0.01.
Note: The larger learning rate that we used in the first example doesn't work this time.
Even after a bunch of steps, Gradient Descent doesn't arrive at the correct answer.
This means that Gradient Descent can be very sensitive to the learning rate.
The good news is that, in practice, a reasonable learning rate can be determined automatically
by starting large and getting smaller with each step.
So, in theory, you shouldn't have to worry too much about the learning rate.
Anyway, we do the math and get two step sizes.
Now we calculate the new intercept and new slope by plugging in the old intercept and the old slope, and the step sizes.
And we end up with a new intercept and a new slope.
This is the line we started with and this is the new line after the first step.
Now we just repeat what we did until all of the step sizes are very small, or we reach the maximum number of steps.
This is the best fitting line, with intercept equals 0.95 and slope equals 0.64,  the same values we get from least squares.
Double bam!
We now know how Gradient Descent optimizes two parameters, the slope and the intercept.
If we had more parameters then we just take more derivatives and everything else stays the same.
Triple bam!
Note: the sum of the squared residuals is just one type of Loss Function.
However, there are tons of other loss functions that work with other types of data.
Regardless of which Loss Function you use, Gradient Descent works the same way.
Step 1: take the derivative of the loss function for each parameter in it.
In fancy machine learning lingo, take the gradient of the loss function.
Step 2: pick random values for the parameters.
Step 3: plug the parameter values into the derivatives (ahem, the gradient).
Step 4: calculate the step sizes.
Step 5: calculate the new parameters.
Now go back to step 3 and repeat until step size is very small or you reach the maximum number of steps.
One last thing before we're done. In our example we only had three data points, so the math didn't take very long.
But when you have millions of data points it can take a long time.
So there is a thing called Stochastic Gradient Descent that uses a randomly selected
subset of the data at every step rather than the full data set.
This reduces the time spent calculating the derivatives of the loss function.
That's all.
Stochastic Gradient Descent sounds fancy, but it's no big deal.
Hooray!
We've made it to the end of another exciting StatQuest.
If you like this StatQuest and want to see more, please subscribe.
And if you want to support StatQuest, well, consider buying one or two of my original
songs, or buying a StatQuest t-shirt or hoodie.
The links are in the description below.
Alright, until next time.
Quest on!