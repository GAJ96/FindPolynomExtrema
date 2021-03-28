import PySimpleGUI as sg
import copy
import numbers
import numpy
from time import process_time

title = "Find My Extrema"

#sg.theme("BluePurple")                                                                         # This changes the theme colours

layout = [ [sg.Text("Represent the polynomial as below:")],                                     # Each [], indicates its own row
           [sg.Text("a1*x^b1 + a2*x^b2 + ... + an*x^bn")],
           [sg.Text("")],
           [sg.Text("Input the coefficients and exponents respectively separated by one space each.")],
           [sg.Text("For the polynomial P(x) = a1x^b1 + a2x^b2 + a3x^b3 the input should look like:")],
           [sg.Text("Coefficients: a1 a2 a3")],
           [sg.Text("Exponents: b1 b2 b3")],
           [sg.Text("NOTE:        The order in which the coefficients and exponents are entered must match so that the")],
           [sg.Text("             elements in each correspond to the same term in the polynomial.")],
           [sg.Text("             EVEN EXPONENTS OF POWER 0 MUST BE INCLUDED!!!")],
           [sg.Text("")],
           [sg.Text("Your polynomial is: "), sg.Text(size = (15,1), key = "-POLYNOM-")],
           [sg.Text("Coefficients: "), sg.InputText(key = "-COEF-")],          # Input the coefficients...
           [sg.Text("Exponents:  "), sg.InputText(key = "-EXP-")],             # ...and exonents here
           [sg.Text("Guess:        "), sg.InputText(key = "-GUESS-")],         # input guess (about the x-coordinate of the extrema)
           [sg.Text("Step width:  "), sg.InputText(key = "-STEP-")],           # input step width
           [sg.Text("Tolerance:   "), sg.InputText(key = "-TOL-")],            # input error tolerance
           [sg.Button("Enter"), sg.Button("Terminate")],                       # buttons
           [sg.Text('An extrema found in the interval: '), sg.Text(size=(15,1), key='-LOWLIM-'), sg.Text(size=(1,1), key='-MIDDLEX-'), sg.Text(size=(15,1), key = "-UPLIM-")],    # When Enter i clicked the code should run, when Terminate is clicked the operation should come to a halt.
           [sg.Text('Type: '), sg.Text(size=(15,1), key='-TYP-')],
           [sg.Text('Outer iterations:'), sg.Text(size=(15,1), key='-OUTERITER-')],
           [sg.Text('Inner iterations:'), sg.Text(size=(15,1), key='-INNERITER-')],
           [sg.Text('Timer:'), sg.Text(size=(15,1), key='-TIME-')]]

margins = (100, 40)                                                                            # (width, height)

window = sg.Window(title = title, layout = layout, resizable = True, margins = margins)                           # This is the window


while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == "Terminate":
        break
    if event == "Enter":
        # Start timer
        t0 = process_time()

        # Store the inputs in these variables
        coefficients    = [float(item) for item in values["-COEF-"].split()] #float(values["-COEF-"])
        exponents       = [float(item) for item in values["-EXP-"].split()] #float(values["-EXP-"])
        guess           = float(values["-GUESS-"])
        step            = float(values["-STEP-"])
        tol             = float(values["-TOL-"])


        # Check if the polynomial has an high enough degree
        if max(exponents) < 2:
            print("Error: Polynomials of degree less than 2 has either constant or 0 slopes.")
            print("Program N/A.")
            break

        # Polynomial
        def p():
          polynom = copy.deepcopy(coefficients)
          for i in range(0, len(coefficients) ):
            polynom[i] = [coefficients[i],"x^",exponents[i]]
          return polynom

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
                guesspos -= 2*step # This was corrected for above (line83)
                guessneg += 2*step # This was corrected for above (line84)
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
            elif fbis(lowlim) < 0 and fbis(uplim) > 0:
                typ = "inflexion point"
            elif fbis(lowlim) > 0 and fbis(uplim) < 0:
                typ = "inflexion point"
            elif fbis(lowlim) == fbis(uplim) == 0:
                typ = "inflexion point"


        # Send output to the GUI
        middlex = "< x <"
        window['-LOWLIM-'].update(lowlim)
        window['-UPLIM-'].update(uplim)
        window["-MIDDLEX-"].update(middlex)
        window["-POLYNOM-"].update(p())
        window["-TYP-"].update(typ)
        window["-INNERITER-"].update(inneriterations)
        window["-OUTERITER-"].update(outeriterations)
        t1 = process_time()
        window["-TIME-"].update(t1-t0)
