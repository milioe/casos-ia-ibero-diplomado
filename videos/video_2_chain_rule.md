the chain rule is cool
stat quest yeah
[Music]
hello i'm josh starmer and welcome to
statquest
today we're going to talk about the
chain rule
and it's going to be clearly explained
note this stat quest assumes that you
are already familiar with the basic
idea of a derivative and just want a
deeper understanding of
the chain rule
that said let's do a super quick review
imagine we collected these measurements
from a bunch of people
on the x-axis we measured how much they
liked statquest
and on the y-axis we measured
awesomeness
we can then fit this orange parabola to
the data
the equation for the parabola is
awesomeness
equals likes statquest squared
the derivative of this equation tells us
the slope of the tangent line at any
point along the curve
the slope of the tangent line tells us
how quickly
awesomeness is changing with respect to
like's stat quest
we can calculate the derivative of
awesomeness with respect to like's
stat quest by using the power rule
the power rule tells us to multiply
like's stat quest
by the power which is 2 and raise stat
quest by the power
2 -1 and since
minus one equals one and raising
something by one
is the same as omitting the power we end
up with
two times like's statquest
okay bam that's the review
now let's dive into the
chain rule
with a super simple example
imagine we collected weight and height
measurements from three people
and then we fit a line to the data
now if someone tells us they weigh this
much
we can use the green line to predict
that they are this
tall bam now imagine we collected height
and shoe size measurements and we fit a
line to the data
now if someone tells us that they are
this tall
we can use the orange line to predict
that this
is their shoe size bam
now if someone tells us that they weigh
this much
then we can predict their height and we
can use the predicted height
to predict shoe size and if we change
the value for weight
we see a change in shoe size
bam
now let's focus on this green line that
represents the relationship between
weight
and height we see that for every one
unit increase in weight
there's a two unit increase in height
in other words the slope of the line is
2 divided by 1 which equals 2
and since the slope is 2 the derivative
the change in height with respect to a
change in weight
is two now since the slope of the green
line
is the same as its derivative two
the equation for height is height
equals the derivative of height with
respect to weight
times weight which equals two
times weight note
the equation for height has no intercept
because the green line goes through the
origin
now let's focus on the orange line that
represents the relationship between
height and shoe size in this case
we see that for every one unit increase
in height
there is a one-quarter unit increase in
shoe size
and i admit that it's hard to see the
one-quarter unit increase in shoe size
so just trust me anyway
because we go up one quarter unit for
every one unit we go
over the slope is one quarter
divided by one which equals one quarter
and since the slope is one quarter the
derivative
or the change in shoe size with respect
to a change in
height is one quarter
now since the slope of the orange line
is the same as its derivative
the equation for shoe size is
shoe size equals the derivative of shoe
size with respect to height
times height which equals one-quarter
times height and again
because the orange line goes through the
origin the equation for shoe size has no
intercept now because
weight can predict height
and height can predict shoe size
we can plug the equation for height into
the equation for shoe size
now if we want to determine exactly how
shoe size
changes with respect to changes in
weight
we can take the derivative of shoe size
with respect to weight and the
derivative
of the equation for shoe size with
respect to weight
is just the product of the two
derivatives
in other words because height connects
weight
to shoe size the derivative of shoe size
with respect to weight
is the derivative of shoe size with
respect to height
times the derivative of height with
respect to weight
this relationship is the essence of the
chain rule
plugging in numbers gives us one half
and that means for every one unit
increase in weight
beep boop beep there is a one-half
unit increase in shoe size bam
now let's look at a slightly more
complicated example
imagine we measured how hungry a bunch
of people were
and how long it had been since they last
had a snack
as time since the last snack increases
on the x-axis
people got hungrier and hungrier at a
faster rate
so we fit an exponential line with
intercept one-half
to the measurements to reflect the
increasing rate of hunger
then we measured how much people craved
ice cream and how hungry they
were the hungrier someone was
the more they craved ice cream
but after a certain amount of hunger the
craving did not continue to increase
very much
so we fit a square root function to the
data to reflect how the increase in
craving
tapers off now if we want to see how the
rate of
craving ice cream changes with respect
to the time
since the last snack plugging the
equation for hunger
into the equation for craves ice cream
gives us an equation without an obvious
derivative
to convince yourself that taking the
derivative of this
is no fun at all pause the video and
give it a try
however because hunger links time since
last snack
to craves ice cream we can use
the chain rule to solve for this
derivative
first the power rule tells us that the
derivative of hunger
with respect to the time since the last
snack is
two times time
likewise the power rule tells us that
the derivative of craves ice cream with
respect to hunger is
one divided by two times the square root
of hunger
so with these two derivatives
the chain rule tells us that the
derivative of craves ice cream
with respect to time is
the derivative of craves ice cream with
respect to hunger
times the derivative of hunger with
respect to time since last snack
so we plug in the derivatives
and plug in the equation for hunger
and cancel out the twos
and we get the derivative of craves ice
cream with respect to time
since last snack this derivative
tells us how quickly or slowly our
craving for ice cream
changes with respect to time
double bam
in this last example it was obvious that
hunger was the link between time since
last snack and craves ice cream
and we had an equation for hunger in
terms of time
and an equation for craves ice cream in
terms of hunger
however usually these relationships are
not so obvious
instead of having two separate equations
we usually get the first equation jammed
into the second
and when all you have is this it's not
so
obvious how the chain rule applies
so we can talk about how to apply the
chain rule
in this situation let us scooch the
equation to the left so we have room to
work
now one thing we can do in this
situation is look for things in the
equation that can be put
in parentheses for example
the square root symbol can be replaced
with parentheses
now we can say that the stuff inside the
parentheses
is time squared plus
one half and craves ice cream
can be rewritten as the square root of
the stuff inside
now the chain rule tells us that the
derivative of craves ice cream
with respect to time is
the derivative of craves ice cream with
respect to the stuff
inside times the derivative of the stuff
inside
with respect to time the power rule
gives us the derivative of craves ice
cream with respect to the stuff
inside and the power rule gives us the
derivative of the stuff inside
with respect to time now we just plug
the derivatives
into the chain rule and plug in the
equation for the stuff inside
cancel out the twos and we get the
derivative of craves ice cream
with respect to the time since last
snack
and that's exactly what we got before
bam
now let's look at how the chain rule
applies to the residual sum of squares
a commonly used loss function in machine
learning
note if this does not make any sense to
you
just imagine i said now let's look at
one last example
imagine we measured someone's weight and
height
and we wanted to fit this green line to
the measurement
now to keep things simple let's assume
we can only move the green line
up and down the equation for the green
line
is height equals the intercept
plus 1 times weight and we can change
the intercept
but to keep things simple we can't
change the slope
which is set to 1. if we set the
intercept to 0
then this location on the green line is
the predicted height
and we can calculate the residual the
difference between the observed height
and the value predicted by the line
and we can plot the residual on this
graph
which has the intercept on the x-axis
and the residual on the y-axis
if we change the intercept here
then we can see the change in the
residual here
and because a common way to evaluate how
good the green line fits the data
is the squared residual we can plot the
squared residual
here where we have the residuals on the
x-axis
and the squared residuals on the y-axis
now if we change the intercept here
then we change the residual here and
here
and changing the residual here changes
the squared residual
here in order to find the value for the
intercept that minimizes the squared
residual
we are going to find the derivative of
the squared residual
with respect to the intercept and then
we're going to find where the derivative
equals zero because given the function
y equals the residual squared the
derivative
is zero at the lowest point
the chain rule says that because the
residual links the intercept to the
squared residual
then the derivative of the squared
residual with respect to the intercept
is the derivative of the squared
residual with respect to the residual
times the derivative of the residual
with respect to the intercept
the power rule tells us that the
derivative of the residual squared
is just two times the residual
so let's plug that in to solve for the
derivative of the residual
with respect to the intercept we move
the equation for the residual
over here so we have room to work
then we plug in the equation for the
predicted height
then in order to remove these
parentheses
we multiply everything inside by
negative one
now the derivative of the residual with
respect to the intercept
is zero because this term does not
contain the intercept
plus negative one because the derivative
of the negative
intercept equals negative one plus zero
because the last term does not contain
the intercept
now do the math and we are left with
negative one
and that makes sense because the
derivative is just the slope of the
orange line
and by i we can see that the slope of
the orange line
is negative one so let's plug this
derivative
in here and do a little math
and plug in the equation for the
residual
now we have the derivative for the
residual squared in terms of the
intercept
note if instead of starting with
separate equations for the residual
and the residual squared we started with
just the equation for the residual
squared with the equation for the
predicted height
jammed into it then just like before
we can use parentheses to help us out
in this case we'll call everything
between the outermost parentheses
the stuff inside which equals the
observed
minus the intercept minus one times
weight
and that means the residual squared can
be rewritten
as the square of the stuff inside
now we can use the chain rule to
determine the derivative of the residual
squared
with respect to the intercept it's the
derivative of the residual squared with
respect to the stuff inside
times the derivative of the stuff inside
with respect to the intercept
just like before the derivative of the
residual
with respect to the stuff inside is two
times the stuff inside so we plug that
into the chain rule
and the derivative of the stuff inside
with respect to the intercept
is negative one so we plug that into the
chain rule now we just plug in the stuff
inside
multiply two with negative one
and we end up with the exact same
derivative as before
bam now we want to find the value for
the intercept
such that the derivative of the residual
squared equals zero
so we plug in the observed height and
the observed weight
set the derivative equal to 0
and solve for the intercept
and at long last we see that when the
intercept
equals one we minimize the squared
residual
and we have the best fitting line
triple bam hooray
we've made it to the end of another
exciting stack quest
if you like this stat quest and want to
see more please subscribe
and if you want to support statquest
consider contributing to my patreon
campaign
becoming a channel member buying one or
two of the statquest study
guides or a t-shirt or a hoodie or just
donate
the links are in the description below
alright
until next time quest on