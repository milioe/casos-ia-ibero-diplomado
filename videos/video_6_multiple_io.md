way up north there's an island out in
the sea
and way out there they've got neural
networks and they're cool
statquest
hello i'm josh starmer and welcome to
statquest
today we're going to talk about neural
networks part 4
multiple inputs and outputs
note this stack quest was supported in
part by
ital also i thought i'd mention that the
inspiration for this stat quest came
from my friend
michael in svalbard lastly
this stat quest assumes that you already
understand the main ideas behind neural
networks
and the relu activation function if not
check out the quests the links are in
the description below
so far the neural networks that we've
looked at have been super simple
and only predict whether or not the
dosage of a drug
will be effective the neural networks
just have one input node
and one output node when there is only
one
input node then the data we are using to
make predictions
in this case dosages can all fit on the
x-axis
of this graph in other words the input
is one-dimensional
since it only needs one axis in the
graph
likewise a single dimension the y-axis
represents the output values combined
we get a two-dimensional graph with the
input dosage
on the x-axis and the output drug
effectiveness
on the y-axis because the input and
output combine to form a two-dimensional
graph
we can see how the weights and biases in
this neural network
slice flip and stretch the curved or
bent activation functions
into new shapes that are added together
to make a two-dimensional squiggle or
shape that fits the data
bam now let's look at a more complicated
network
that has more than one input node and
more than one output node
now this neural network may look really
fancy
but all it does is take two measurements
from an iris flower
the width of a petal which is this part
of the flower
and the width of a sepal which is this
part of the flower
and with that information it predicts
the species
either setosa versicolor or virginica
now raise your hand if you already knew
that this was a sepal and not a petal
not me i thought they were all petals
anyway to keep things simple at the
start let's begin with both
input nodes but just one output node for
setosa
later on we'll add the other two output
nodes but for now
let's keep things simple and just use
one output node
now let's see what happens when we plug
values for petal width
and sepal width into this simplified
neural network
since we have two inputs and one output
if we're going to draw a graph
of what's going on then we need a
three-dimensional graph
the inputs petal width and sepal width
each get an axis
in the output the prediction for setosa
gets the y-axis
note to keep the math simple i scaled
the inputs to be between 0
for the smallest value and one for the
largest value
so let's start in this corner where
petal and sepal width
equal zero and plug those values into
the neural network
first let's determine the x-axis
coordinate for the top node in the
hidden layer
we multiply the petal width by the
weight associated with the connection to
the top node in the hidden layer
negative 2.5 and we multiply the
sepal width by the weight associated
with its connection to the top node in
the hidden layer
0.6 then we add the two
terms together and add the bias 1.6
and that gives us the x-axis coordinate
for the activation function
which is 1.6 now we plug 1.6
into the relu activation function to get
the y-axis coordinate
1.6 because 1.6
is greater than 0 and 1.6
corresponds to this blue point on the
graph when petal and sepal widths are
both zero
now let's increase petal width to 0.2
but keep sepal width at 0.
now when we do the math we get 1.1 for
the x-axis coordinate
and 1.1 for the y-axis coordinate
and 1.1 corresponds to this blue point
on the graph likewise when we
increase pedal width to the maximum
value 1
but keep sepal width at 0 we get these
blue dots
now let's increase sepal width to 0.2
and run values for petal width from 0 to
1
through the neural network
likewise if we keep increasing sepal
width to 1
for different values of petal width we
get this blue bent
surface the bend corresponds to the
points where the relu
activation function set the y-axis
values to 0.
now we multiply the y-axis value for
each point by negative 0.1
for example the original y-axis value
for this point
when petal and sepal widths are both
zero is 1.6
and 1.6 times negative 0.1
equals negative 0.16 so the final point
is here
likewise when we multiply all of the
other y-axis coordinates by negative 0.1
we get this final blue bent surface
now we do the exact same thing for the
connections to the bottom node in the
hidden layer
and we end up with this orange bent
surface where the bend
occurs where the relu activation
function set the y-axis
values to zero then we multiply each
y-axis coordinate by 1.5 to get the
final
orange bent surface
now we add the y-axis coordinates on the
blue bent surface
to the y-axis coordinates on the
orange-bent surface
for example the y-axis coordinate for
this blue point
is negative 0.16
and we add the y-axis coordinate for
this orange point
1.05 to get 0.89 the y-axis coordinate
for this green point
anyways we do that for every single
point and
ultimately we end up with this green
crinkled surface
now the last thing we do is add the
final bias
0 to each y-axis coordinate
and since adding 0 doesn't change the
green crinkled surface
this is the output for setosa bam
looking at the green crinkled surface we
see that the value for setosa is highest
when the petal width is close to zero
and the value for setosa is lowest
when the petal width is close to one
note remember that we scaled the inputs
to be between zero
and one and thus pedal width equals zero
does not imply that the pedal is zero
centimeters wide
instead 0 refers to the smallest width
in the training data set
likewise 1 means the largest width in
the training data set
small bam now to review the concepts so
far
when we have two inputs the neural
network creates curved or bent surfaces
that are added together to make a new
crinkled surface
that in this case we can use to make
predictions about whether or not the
species of an iris is setosa
for example if we found this iris while
walking in the woods
and the scaled petal width was 0.5
and the scaled sepal width was 0.37
then we can look at the y-axis value on
the green crinkled surface that
corresponds to these measurements
and see that this particular iris is
probably not setosa
because the y-axis value is closer to
zero
than one and this is confirmed when we
run the numbers through the neural
network
and get 0.09
bam now that we have a green crinkled
surface for setosa
let's determine the output for the
second species fursy color
just like before we'll start with the
connections to the top node in the
hidden layer
and because the weights and biases are
the same as before
we start out with the same blue bent
surface
however because we will multiply the
y-axis coordinates by 2.4
let's change the range of the y-axis
from 0 to 2
to negative 6 to 6 bam
now multiplying the y-axis coordinates
by 2.4
gives us this final blue bent surface
now we create the orange pen surface
from the bottom node in the hidden layer
and multiply the y-axis coordinates on
the orange-bent surface by negative 5.2
now we add the y-axis coordinates from
the two bent surfaces together
to create this red crinkled surface
lastly we add the final bias 0
to the y-axis coordinates on the red
crinkled surface
and that gives us the final surface for
predicting if the iris species is
versicolor
now i'll admit it's hard to see
what values for petal or sepal widths
will give versicolor a high score
on this red crinkled surface but when we
change the y-axis scale
from negative 6 to 6 to negative 0.5
to 1 we see that when petal width
is close to 0.4 we will get a high value
for versicolor double bam
now just like we did for setosa and
versicolor
let's determine the crinkled surface for
virginica
just like before we start with the blue
bent surface from the top node in the
hidden layer
but now we multiply the y-axis
coordinates by negative 2.2
and just like before we create the
orange bent surface from the bottom node
in the hidden layer
but now we multiply the y-axis
coordinates by 3.7
now we add the y-axis coordinates from
the two bent surfaces
together and get this purple crinkled
surface
lastly we add the final bias one
to the y-axis coordinates on the purple
crinkled surface
and that gives us the final surface for
predicting if the iris species is
virginica
now so we can see what's going on let's
change the scale for the y-axis from
negative six
to six to zero to one
now we see that when petal width is
close to 1
then we will get a high score for
virginica
triple bam at long last
we have crinkled surfaces for setosa
versicolor
and virginica now we can plug in the
petal and sepal widths
from the iris we found and run the
numbers through the neural network
and predict that this iris is versicolor
because that output value
0.86 is closest to 1.
that said usually when there are two or
more
output nodes the output values are sent
to either something called
arg max arg or something called
softmax before a final decision is made
and we'll talk about argmax and softmax
in the next stat quest in this series
bam now it's time for some
shameless self-promotion if you want to
review statistics and machine learning
offline
check out the statquest study guides at
statquest.org
there's something for everyone hooray
we've made it to the end of another
exciting stat quest
if you like this stat quest and want to
see more please subscribe
and if you want to support statquest
consider contributing to my patreon
campaign
becoming a channel member buying one or
two of my original songs or a t-shirt or
a hoodie
or just donate the links are in the
description below
alright until next time quest on