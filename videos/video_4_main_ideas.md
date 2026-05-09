Backpropagation is a really big word, but it's not a really big deal. StatQuest!
Hello!
I'm Josh Starmer and welcome to StatQuest!
Today we're going to talk about Neural Networks, Part 2: Backpropagation Main Ideas.
Note: this StatQuest assumes that you are already familiar with neural networks, the
chain rule, and gradient descent.  If not, check out the quests.  The links are in the description below.
In the StatQuest on Neural Networks Part 1, Inside the Black Box, we started with
a simple dataset that showed whether or not different drug dosages were effective against a virus.
The low and high dosages were not effective, but the medium dosage was effective.
Then we talked about how a neural network like this one fits a green squiggle to this data set.
Remember, the neural network starts with identical activation functions, but, using
different weights and biases on the connections, it flips and stretches the activation
functions into new shapes, which are then added together to get a squiggle that is shifted to fit the data.
However, we did not talk about how to estimate the weights and biases.
So let's talk about how backpropagation optimizes the weights and biases in this, and other, neural networks.
Note: backpropagation is relatively simple, but there are a ton of details, so I split it up into bite-sized pieces.
In this part we talk about the main ideas of backpropagation.
One: using the chain rule to calculate derivatives, and Two: plugging the derivatives
into gradient descent to optimize parameters. In the next part we'll talk about how
the chain rule and gradient descent apply to multiple parameters simultaneously, and introduce some fancy notation.
Then we will go completely bonkers with the chain rule and show how to optimize all
seven parameters simultaneously in this neural network.
Bam!
First, so we can be clear about which specific weights we are talking about, let's
give each one a name: we have w1, w2, w3, and w4.
And let's name each bias: b1, b2, and b3.
Note: conceptually, backpropagation starts with the last parameter and works its way
backwards to estimate all of the other parameters.
However, we can discuss all of the main ideas behind a backpropagation by just estimating the last bias, b3.
So, in order to start from the back, let's assume that we already have optimal values
for all of the parameters except for the last bias term, b3.
Note: throughout this, and the next StatQuests, I'll make the parameter values that
have already been optimized green, and unoptimized parameters will be red.
Also, note: to keep the math simple, let's assume dosages go from 0, for low, to 1, for high.
Now, if we run dosages from 0 to 1 through the connection to the top node in the hidden
layer, then we get the x-axis coordinates for the activation function, that are all
inside this red box and when we plug the x-axis coordinates into the activation function
which, in this example, is the soft plus activation function, we get the corresponding
y-axis coordinates, and this blue curve.
Then we multiply the y-axis coordinates on the blue curve by negative 1.22 and we get the final blue curve.
Bam!
Now, if we run dosages from zero to one through the connection to the bottom node
in the hidden layer, then we get x-axis coordinates inside this red box.
Now we plug those x-axis coordinates into the activation function to get the corresponding
y-axis coordinates for this orange curve.
Now we multiply the y-axis coordinates on the orange curve by negative 2.3 and we end up with this final orange curve.
Bam!
Now we add the blue and orange curves together to get this green squiggle.
Now we are ready to add the final bias, b3, to the green squiggle.
Because we don't yet know the optimal value for b3, we have to give it an initial
value, and because bias terms are frequently initialized to 0, we will set b3 equal to 0.
Now, adding zero to all of the y-axis coordinates on the green squiggle leaves it right where it is.
However, that means the green squiggle is pretty far from the data that we observed.
We can quantify how good the green squiggle fits the data by calculating the sum of the squared residuals.
A residual is the difference between the observed and predicted values.
For example, this residual is the observed value, zero, minus the predicted value
from the green squiggle, negative 2.6. This residual is the observed value, one,
minus the predicted value from the green squiggle, negative 1.61.
Lastly, this residual is the observed value, 0, minus the predicted value from the green squiggle, negative 2.61.
Now we square each residual and add them all together to get 20.4 for the sum of the squared residuals.
So when b3 equals 0, the sum of the squared residuals equals 20.4. And that corresponds
to this location on this graph that has the sum of the squared residuals on the y -axis and the bias, b3, on the x-axis.
Now, if we increase b3 to 1, then we would add one to the y-axis coordinates on the
green squiggle and shift the green squiggle up one.
And we end up with shorter residuals.
When we do the math, the sum of the squared residuals equals 7.8, and that corresponds to this point on our graph.
If we increase b3 to 2, then the sum of the squared residuals equals 1.11. And if
we increase b3 to 3, then the sum of the squared residuals equals 0.46. And if we
had time to plug in tons of values for b3, we would get this pink curve, and we could
find the lowest point, which corresponds to the value for b3 that results in the
lowest sum of the squared residuals, here.
However, instead of plugging in tons of values to find the lowest point in the pink
curve, we use gradient descent to find it relatively quickly.
And that means we need to find the derivative of the sum of the squared residuals with respect to b3.
Now, remember the sum of the squared residuals equals the first residual squared,
plus all of the other squared residuals.
Now, because this equation takes up a lot of space, we can make it smaller by using summation notation.
The greek symbol sigma tells us to sum things together, and 'i' is an index for the
observed and predicted values that starts at one.
And the index goes from one to the number of values, 'n', which in this case is set to 3.
So, when 'i' equals one, we're talking about the first residual.
When 'i' equals two, we're talking about the second residual.
And when 'i' equals three, we are talking about the third residual.
Now let's talk a little bit more about the predicted values.
Each predicted value comes from the green squiggle, and the green squiggle comes from the last part of the neural network.
In other words, the green squiggle is the sum of the blue and orange curves, plus b3.
Now remember, we want to use gradient descent to optimize b3, and that means we need
to take the derivative of the sum of the squared residuals with respect to b3.
And because the sum of the squared residuals are linked to b3 by the predicted values,
we can use the chain rule to solve for the derivative of the sum of the squared residuals with respect to b3.
The chain rule says that the derivative of the sum of the squared residuals with respect
to b3 is the derivative of the sum of the squared residuals with respect to the predicted
values, times the derivative of the predicted values with respect to b3.
Now, before we calculate the derivative of the sum of the squared residuals with respect
to the predicted values, let's clean up our workspace and move these equations out of the way.
Now we can solve for the derivative of the sum of the squared residuals with respect
to the predicted values by first substituting in the equation, and then use the chain
rule to move the square to the front, and then we multiply that by the derivative
of the stuff inside the parentheses with respect to the predicted values, negative one.
Now we simplify by multiplying two by negative 1, and we have the derivative of the
sum of the squared residuals with respect to the predicted values.
So let's move that up here, and now we are done with the first part.
Now let's solve for the second part: the derivative of the predicted values with respect to b3.
We start by plugging in the equation for the predicted values.
Remember, the blue and orange curves were created before we got to b3.
So the derivative of the blue curve with respect to b3 is 0, because the blue curve is independent of b3.
And the derivative of the orange curve with respect to b3 is also 0.
Lastly, the derivative of b3, with respect to b3, is 1.
Now we just add everything up, and the derivative of the predicted values with respect to b3, is one.
So we multiply the derivative of the sum of the squared residuals with respect to the predicted values by 1.
Note: this times 1 part in the equation doesn't do anything, but I'm leaving it in
to remind us that the derivative of the sum of the squared residuals with respect
to b3 consists of two parts: the derivative of the sum of the squared residuals with
respect to the predicted values, and the derivative of the predicted values with respect to b3.
Bam! And at long last we have the derivative of the sum of the squared residuals with respect to b3.
And that means we can plug this derivative into gradient descent to find the optimal value for b3.
So let's move this equation up and show how we can use this equation with gradient descent.
Note: if you're not familiar with gradient descent, check out the quest
the link is in the description below.
Anyway, first, we expand the summation.
Then, we plug in the observed values and the values predicted by the green squiggle.
Remember, we get the predicted values on the green squiggle by running the dosages through the neural network.
Now, we just do the math and get negative 15.7. And that corresponds to the slope for when b3 equals zero.
Now we plug the slope into the gradient descent equation for step size, and, in this
example, we'll set the learning rate to 0.1. And that means the step size is -1.57.
Now we use the step size to calculate the new value for b3 by plugging in the current
value for b3, zero, and the step size, -1.57. And the new value for b3 is 1.57.
Changing b3 to 1.57 shifts the green squiggle up, and that shrinks the residuals.
Now, plugging in the new predicted values and doing the math gives us -6.26, which
corresponds to the slope when b3 equals 1.57.
Then, we calculate the step size and the new value for b3, which is 2.19.
Changing b3 to 2.19 shifts the green squiggle up further, and that shrinks the residuals even more.
Now we just keep taking steps until the step size is close to zero. And because the
step size is close to 0 when b3 equals 2.61, we decide that 2.61 is the optimal value for b3.
Double bam!
So, the main ideas for backpropagation are that, when a parameter is unknown, like
b3, we use the chain rule to calculate the derivative of the sum of the squared residuals
with respect to the unknown parameter, which in this case was b3.
Then we initialize the unknown parameter with a number, and in this case we set b3
equal to zero, and used gradient descent to optimize the unknown parameter.
Triple bam!
In the next StatQuest we'll show how these ideas can be used to optimize all of the parameters in a neural network.
Now it's time for some shameless self-promotion.
If you want to review statistics and machine learning offline, check out the StatQuest study guides at statquest.org.
There's something for everyone.
Hooray!
We've made it to the end of another exciting StatQuest.
If you like this StatQuest and want to see more, please subscribe.  And if you want
to support StatQuest, consider contributing to my patreon campaign, becoming a channel
member, buying one or two of my original songs, or a t-shirt or a hoodie, or just
donate the links are in the description below.  Alright, until next time.  Quest on!