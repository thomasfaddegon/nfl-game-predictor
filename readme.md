# Notes to Self

To activate the virtual environment, run the following command from the root of the project directory:
`source .venv/bin/activate`

To deactivate the virtual environment, simply run:
`deactivate`

If you need to reset the terminal after, run the following command:
`export PS1="\h:\W \u\$`

I've had a lot of problems with VScode not recognizing the virutal environment, so I've had to continually reinstall the environment. Run this code to reinstall the necessary packages:
`pip install pandas scikit-learn selenium flask flask-cors`

To start the flask server, run the following command:
`python3 api.py`

If you have trouble with modules not benig loaded, restart the app. If that doesn't work, try reinstalling the virtual environment.

# Predictions:

## Wild Card (4-1-1)

Texans vs. Browns
Predicted: Texans 24 Browns 20
Line: Browns -2
Actual: Texans 45, Browns 14

Dolphins vs. Chiefs
Predicted: Chiefs 23 Dolphins 23
Line: Chiefs -4.5
Acutal: Chiefs 26, Dolphins 7

Bills vs. Steelers
Predicted: Bills 25, Steelers 15
Line: Bills -10
Actual: Bills 31, Steelers 17

Cowboys vs. Packers
Predicted: Cowboys 26, Packers 20
Line: Cowboys -7
Actual: Packers 48, Cowboys 32

Lions vs. Rams
Predicted: Lions 30, Rams 26
Line: Lions -3
Actual: Lions 24, Rams 23

Buccaneers vs. Eagles
Predicted: Buccaneers 25, Eagles 21
Line: Eagles -2.5
Actual: Buccaneers 32, 9

## Divisional Round (3-1)

Ravens vs. Texans
Predicted: Ravens 28, Texans 16
Line: Ravens -10
Acutal: Ravens 34, Texans 10

Chiefs vs. Bills
Predicted: Chiefs 17, Bills 23
Line: Bills -2
Actual: Chiefs 27, Bills 24

49ers vs. Packers
Predicted: 49ers 30, Packers 19
Line: 49ers -10
Actual: 49ers 24, Packers 21

Lions vs. Buccaneers
Predicted: Lions 27, Buccaneers 22
Line Lions -6
Actual: Buccaneers 31, Lions 23

## Conference Championship (1-1)

Ravens vs. Chiefs
Predicted: Ravens 25, Chiefs 15
Line: Ravens -4.5
Actual: Chiefs 17, Ravens 10

49ers vs. Lions
Predicted: 49ers 33, Lions 23
Line: 49ers -7.5
Actual: 49ers 34, Lions 31

## Super Bowl (0-1)

Chiefs vs. 49ers
Predicted: Chiefs 18, 49ers 25
Line: 49ers -2
Actual: Chiefs 25, 49ers 22
