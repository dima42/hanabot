to run simulation:

python play.py 2 2 10000

to play with computer:

python play.py 0 2 1

current stats:

BasicPlayer and BasicPlayer: 18.1 +/- 2.6 pts

CardStatePlayer and CardStatePlayer: 20.7 +/- 2.5 pts


to write a new player:

* add new class to players.py overloading Player
* overload get_move() with your strategy logic
* modify simulator.py play() call to use your players
