
import numbers
import numpy
from time import process_time
import copy

print("")
print("")
print("")
print("")
print("")
print("")
print("")
print("")
print("")
print("")
print("")
print("")
print("")
print("")
print("")
print("")
print("")
print("")
print("")
print("")
print("")
print("")
print("")
print("")
print("")
print("")
print("")
print("")

# Inputs
print("")
print("_________________________Find the extreme points of polynomials____________________________")
print("")
print("In order to solve for the polinomials exreme points it needs to be represented as below:")
print("a1 * x^b + a2 * x^(b-1) + ... + an * x^0")
print("")
print("___________________________________________________________________________________________")
print("")
while True:
    try:
        print("____INPUTS___")
        coefficients = [float(item) for item in input("Enter the coefficients:.....").split()]
        exponents    = [float(item) for item in input("Enter the exponents:........").split()]
        guess                           = float(input("Guess location on x-axis:..."))
        tol                             = float(input("Maximum error tolerance:...."))
        step                            = float(input("Initial step width:........."))
        print("___________________________________________________________________________________________")
        break
    except ValueError:
        print("Error: Inputs can only be floatnumber. The exponent must also be an integer.")
        print("Try again of force the program to terminate using CTRL+c.")

# Start timer
t0 = process_time()

# Check if the polynomial has an high enough degree
if max(exponents) < 2:
    print("Error: Polynomials of degree less than 2 has either constant or 0 slopes.")
    print("Program N/A.")
    exit()

# Polynomial
#def p(x):
#  summa = 0
#  for i in range(0, len(coefficients) ):
#    summa += coefficients[i] * x ** exponents[i]
#  return summa

# First derivative
def fprim(x):
  summa = 0
  for i in range(0, len(coefficients)):
    if exponents[i] > 0:
      summa += coefficients[i] * exponents[i] * (x**(exponents[i] - 1))
    elif exponents[i] == 0:
      pass
  return summa

#The second derivative is neede to determine if the exterma is a min or max
def fbis(x):
  summa = 0
  for i in range(0, len(coefficients)):
    if exponents[i] > 1:
      summa += coefficients[i] * exponents[i] * (exponents[i]-1) * (x**(exponents[i]-2))
    elif exponents[i] == 0 or exponents[i] == 1:
      pass
  return summa

# The bounds of the extrema
lowlim = 0
uplim = 0

# The guesses to the right and to hte left are stored in these respectively
guesspos = copy.deepcopy(guess)
guessneg = copy.deepcopy(guess)
initialguess = copy.deepcopy(guess)
guesspos += 2*step # Corrects for the initial correction of the step in the outer while loop in the algorithm
guessneg -= 2*step # Corrects for the initial correction of the step in the outer while loop in the algorithm

# Iterations count
inneriterations = 0
outeriterations = 0

typ = " "
# The algorithm
# If we have a positive slope do this:
if fprim(initialguess) > 0:

    while step > tol:
        guesspos -= 2*step # This was corrected for above
        guessneg += 2*step # This was corrected for above
        while fprim(guesspos)  > 0 and fprim(guessneg) > 0:
            guesspos += step
            guessneg -= step
            inneriterations += 1
        step = step/2
        outeriterations += 1
    step = 2*step

    if fprim(guesspos) <= 0:
        lowlim = guesspos - step
        uplim = guesspos

    elif fprim(guessneg) <= 0:
        lowlim = guessneg
        uplim = guessneg + step


# If slope negative , do this:
if fprim(initialguess) < 0:

    while step > tol:
        guesspos -= 2*step
        guessneg += 2*step
        while fprim(guesspos) < 0 and fprim(guessneg) < 0:
            guesspos += step
            guessneg -= step
            inneriterations += 1
        step = step/2
        outeriterations += 1

    step = 2*step

    if fprim(guesspos) >= 0:
        lowlim = guesspos - step
        uplim = guesspos

    elif fprim(guessneg) >= 0:
        lowlim = guessneg
        uplim = guessneg + step

# Checking if its a min or a max
    if fbis(lowlim) < 0 and fbis(uplim) < 0:
        typ = "maximum"
    elif fbis(lowlim) > 0 and fbis(uplim) > 0:
        typ = "minimum"
    elif (fbis(lowlim) < 0 and fbis(uplim) > 0) or fbis(lowlim) > 0 and fbis(uplim) < 0:
        typ = "inflexion point"
    elif fbis(lowlim) == fbis(uplim) == 0:
        typ = "inflexion point"

#for
#coefficients[i]+"*x^("exponents[i]+")"


# Output:
#print("Your polynomial:    ", a1,"x^",b)
print("___________________________________________________________________________________________")
print("")
print("___Output___")
print("Location on the x-axis:...(",lowlim,";",uplim,")")
print("Type of extrema:...........", typ)
print("Inneriterations:............... ", inneriterations)
print("Outeriterations:............... ", outeriterations)
t1 = process_time()
print("Timer:....................[", t1-t0, "]")
if typ == "inflexion point":
    print("")
    print("Note: An inflexion point can be a stationary point but is never an extrema.")
print("___________________________________________________________________________________________")
