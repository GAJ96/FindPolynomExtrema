
import numbers
import numpy

# Inputs
print("In order to solve for the polinomials exreme points it needs to be represented as below:")
print("a1 * x^b + a2 * x^(b-1) + ... + an * x^0")
b = float(input("What degree is your polynomial? Enter: "))
a1 = float(input("What is the coefficient of this term? Enter: "))
guess = float(input("Make a guess on where the extrema might be located on the x-axis: "))
tol = float(input("Maximum amount of tolerated error: "))
step = float(input("How large steps shall we begin the search process with? Enter: "))

# First derivative
def fprim(x):
    return(a1*b*(x**(b-1)))

#The second derivative is neede to determine if the exterma is a min or max
def fbis(x):
    return(a*b*(b-1)*(x**(b-2)))

# The bounds of the extrema
lowlim = 0
uplim = 0

# The guesses to the right and to hte left are stored in these respectively
guesspos = guess
guessneg = guess

# Iterations count
iterations = 0


typ = " "
# The algorithm
# If we have a positive slope do this:
if fprim(guess) > 0:

    while step > tol:
        while fprim(guesspos)  > 0 and fprim(guessneg) > 0:
            guesspos += step
            guessneg -= step
            iterations += 1
        step = step/2

    if fprim(guesspos) < 0:
        lowlim = guesspos
        uplim = guesspos + step

    elif fprim(guessneg) < 0:
        lowlim = guessneg - step
        uplim = guessneg


# If slope negative , do this:
if fprim(guess) < 0:

    while step > tol:
        while fprim(guesspos) < 0 and fprim(guessneg) < 0:
            guesspos += step
            guessneg -= step
            iterations += 1
        step = step/2

    if fprim(guesspos) > 0:
        lowlim = guesspos
        uplim = guesspos + step

    elif fprim(guessneg) > 0:
        lowlim = guessneg - step
        uplim = guessneg

# Checking if its a min or a max
if fbis( (lowlim + uplim)/2 ) < 0:
    typ = "maximum"
elif fbis( (lowlim + uplim)/2 ) > 0:
    typ = "minimum"

print()
print()
print()

# Output:
print("The extrema is predicted to be in the boudns of (",lowlim,";",uplim,").")
print("The extrema is a ",typ,".")
print("It took ",iterations, "iterations to find this",typ,".")
