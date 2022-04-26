# Combinatorial_Game

## Installation
Python 3.8.10 was used to develop this program.

To install required packages run:
```bash
pip install -r requirements.txt
```

## Running
To play against agents firstly go into `src/` directory and then run:
```bash
python ./main.py 
```

You can also specify game configuration. To show possible arguments run:
```bash
python ./main.py --help
```

E.g. if you want to play against Monte Carlo agent which simulates move 500 times, where the game conditions are n = 8, r = 3 and maximum color occurences for each color are [3, 3, 3] run:
```bash
python ./main.py -a MonteCarlo --simulations 500 -n 8 -seq 3 3 3
```

NOTE: the only necessary argument is `-seq`