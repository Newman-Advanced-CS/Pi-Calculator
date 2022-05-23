# IMPORTANT PACKAGES NEEDED TO RUN THE PROGRAM
import math
import sys
from decimal import *
import PySimpleGUI as sg # pip install pysimplegui
import matplotlib.pyplot as plt # pip install matplotlib

# The first KNOWN 105 digits of PI (stored as a string to stop rounding)
known105 = "3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214"

# The amount of digits to calculate ahead to increase accuracy
digitsAhead = 2

# Python implementation of math.max
def max(a, b):
    if a > b:
        return a
    elif b > a:
        return b
    else:
        return a

# Recursive factorial function
def factorial(x):
       if x==0:
           return 1
       else:
           return Decimal(x*factorial(x-1))

def CalculatePI(digits, showApproximation = False): # Calculates pi to a specific number of digits
    getcontext().prec = digits + digitsAhead # Change the precision of the decimal variables
    sys.setrecursionlimit(max(math.floor(digits/1.5), 1000)) # Change the recursion limit of the system (yikes)

    sum = Decimal(0)
    n = Decimal(0)
    coefficient = Decimal((2 * math.sqrt(2))/9801)

    approximationList = [] # Array that stores all the approximated values over time
    while True:
        #Ramanujan's Formula:
        frac1Num = Decimal(factorial(4*n))
        frac1Den = Decimal(pow(factorial(n),4))
        frac1 = frac1Num/frac1Den
        frac2 = Decimal(((26390*n+1103)/pow(396,4*n)))
        tmp = frac1 * frac2
        sum +=tmp
        inversePi = sum * coefficient

        n += 1
        calculatedPi = 1/inversePi
        if len(approximationList) != 0:
            fixedPi = Decimal(str(calculatedPi)[0:len(str(calculatedPi))-digitsAhead]) # Remove the last two digit of the number to stop rounding
            if calculatedPi == approximationList[-1]: # When the last result is equal to the new result, no furthur specificity can be reached.
                if showApproximation == True:
                    return approximationList
                else:
                    return fixedPi

        approximationList.append(calculatedPi)

# GUI with pysimplegui
sg.theme('DarkAmber')   # Add a touch of color

def NumberInput(values, key):
    # Get input
    INPUT = values[key]

    # Make sure input is valid
    if INPUT.isnumeric() == False or int(INPUT) == 0:
        MainMenu() # Restart program if input is not a number (this includes negative numbers) OR the input is 0
        return
    else:
        return int(INPUT)

def ErrorGraph(approximations, known, start):
    # Calculate the error for every value of the approximation list
    errors = []
    xaxis = range(start, len(approximations))
    for i in xaxis:
        print(f"{i} -> {approximations[i]}")
        # Calculate errors
        errorAtI = abs((approximations[i] - known) / known * 100)
        errors.append(errorAtI)

    # Graph the trend
    plt.plot(xaxis, errors)
    plt.title("Percentage of error over iterations of series")
    plt.xlabel("n")
    plt.xticks(xaxis) # Set the scale of the x-axis
    plt.ylabel("Error %")

    plt.show()

    # Expert analysis of graph (from a .txt file)
    text_file = open("./graphAnalysis.txt", "r")
    data = text_file.read()
    text_file.close()   

    layout = [[sg.Multiline(data, disabled=True, size=(350, 10))], [sg.HorizontalSeparator()], [sg.Button("SHOW GRAPH"), sg.Button("SHOW GRAPH (N = 2)"), sg.Button("OK")]]
    analysisWindow = sg.Window("Analysis", layout=[[sg.Frame(title="Graph Analysis", layout=layout)]], size=(400, 200))
    while True:
        event, values = analysisWindow.read()
        if event == sg.WIN_CLOSED or event == "OK":
            analysisWindow.close()
            MainMenu()
            break
        elif event == "SHOW GRAPH":
            analysisWindow.close()
            ErrorGraph(approximations, known, 0)
            break
        elif event == "SHOW GRAPH (N = 2)":
            analysisWindow.close()
            ErrorGraph(approximations, known, 1)
            break

def MainMenu():
    # Create window
    menu = [[sg.Text("Calculate PI")],
    [sg.HorizontalSeparator()],
    [sg.Text("How many digits?"), sg.InputText(size=(5, 50), key="-DIGIT-"), sg.Button("Calculate"), sg.Button("Approxmimation over time")],
    [sg.HorizontalSeparator()], 
    [sg.Button("Get error %")]]
    menuWindow = sg.Window(title="PI-thon", layout=[[sg.Frame(title="PI-thon", layout=menu, element_justification='c')]], size=(420, 140), element_justification='c')

    # Check for events and values
    event, values = menuWindow.read()
    if event == "Calculate":
        menuWindow.close() # Close main menu

        INPUT = NumberInput(values, "-DIGIT-")
        pi = CalculatePI(INPUT)
        # Create result window to show approximation
        layout = [[sg.Multiline(pi, size=(350, 10), disabled=True)], [sg.Button("OK")]]
        result = sg.Window(title="RESULT", layout=layout, size=(400,160), finalize=True)
        while True:
            event, values = result.read()
            if event == sg.WIN_CLOSED or event == "OK":
                result.close()
                MainMenu()
                break
    elif event == "Get error %":
        menuWindow.close() # Close main menu

        # Calculate an appoximate value of pi to 105 digits
        approximations = CalculatePI(105, True)
        approximation = approximations[-1]
        # Calculate the percentage of error
        known = Decimal(known105)
        error = abs((approximation - known) / known * 100)
        # Display results
        labelColumn = [[sg.Text("Known Value:")], [sg.Text("Approximated Value:")], [sg.Text("Percentage of Error:")]]
        resultColumn = [[sg.Multiline(known, size=(25, 5), disabled=True)], [sg.Multiline(approximation, size=(25, 5), disabled=True)], [sg.Multiline(error, size=(25, 5))]]
        layout = [[sg.Column(labelColumn, justification="left", vertical_alignment="left"), sg.Column(resultColumn, justification="right")], [sg.HorizontalSeparator()], [sg.Button("OK"), sg.Button("ERROR TREND")]]

        result = sg.Window(title="Error Test", layout=[[sg.Frame(title="ERROR (at 105 digits)", layout=layout)]], size=(380, 280), element_justification='c')
        while True:
            event, values = result.read()
            if event == sg.WIN_CLOSED or event == "OK":
                result.close()
                MainMenu()
                break
            elif event == "ERROR TREND":
                result.close()
                ErrorGraph(approximations, known, 0)
                break
                
    elif event == "Approxmimation over time":
        menuWindow.close() # Close main menu

        # Do the actual assignment
        INPUT = NumberInput(values, "-DIGIT-")
        approximations = CalculatePI(INPUT, True)

        # Assignment done, display results        
        piColumn = [[sg.Text("[n] pi")], [sg.HorizontalSeparator()]] # key
        for i in range(len(approximations)): # Add a column for all the values of pi
            piColumn.append([sg.Text(f"[{i}]"), sg.Text(str(approximations[i])[0:len(str(approximations[i]))-digitsAhead])])

        layout = [[sg.Column(piColumn, justification="left", vertical_alignment="left", scrollable=True, size=(400, 300))]]
        result = sg.Window(title="Approximation over time", layout=[[sg.Frame(title=f"RESULTS ({len(approximations)} iterations)", layout=layout, size=(400, 300), element_justification='l')], [sg.Button("OK")]], size=(450, 350), element_justification='c')
        while True:
            event, values = result.read()
            if event == sg.WIN_CLOSED or event == "OK":
                result.close()
                MainMenu()
                break
    
# Start the program
MainMenu()