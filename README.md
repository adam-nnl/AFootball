AFootball
=========

Small project using <a href="https://github.com/adam-nnl/ANNeML" target="_BLANK">ANNeML files</a> in conjunction with the 
<a href="https://github.com/adam-nnl/Erudite" target="_BLANK">Erudite neural network suite</a> to accurately predict NFL 
game outcomes. 

Home team and away team statistics(YPG, TO+/-, QBR, PPG, PPG-A, YPG-A) are inputted to the neural network and one of the
two output nodes representing the home and away team will "fire"(output close to 1.0) to indicating a predicted win. Example,
SEA @ ARI; stats are inputted; neural net is run; output node value for away team=0.99898; output node value for home
team=0.001938; neural network is predicting away(SEA) team to win and home(ARI) team to lose.

This repository mainly consists of python scripts that can produce training or testing sets for use with ANNeML neural 
networks. This repo also contains various .csv, .txt, .xlsx files with existing NFL data, stats and neural network results.

Requirements:
==========

- <a href="http://www.python.org/download/releases/2.7/" target="_BLANK">Python 2.7</a>
- <a href="https://github.com/BurntSushi/nflgame" target="_BLANK">nflgame python library</a>
- beautifulsoup4 (if updating rosters/stats)
- httplib2 (if updating roster/stats)
- MS Excel or Google Docs (for .xlsx files)
- <a href="https://github.com/adam-nnl/Erudite" target="_BLANK">Erudite Neural Network Suite</a>
- <a href="http://www.oracle.com/technetwork/java/javase/downloads/index.html" target="_BLANK">Java 1.7+</a>


File and Directories Purposes:
============

- ANNeML Files: directory containing ANNeML XML neural network files. Both trained and untrained
- Pythons Scripts: directory containing python scripts to  generate training data .csv files or weekly game data .csv sets for testing/prediction
- Training Sets: premade training set .csv files containing data of past NFL games to train the ANNeML neural net files with
- AFootball_training_results.xlsx: Excel spreadsheet with the training results for the trained ANNeML neural nets. Time to train, epochs, training options, etc.
- AFootball_testing_results.xlsx: Excel spreadsheet with the prediction testing results of the trained neural netws up to NFL week 6
- nfl_weeklystats_wk5.txt: Prediction test set data for NFL week 5 for manual entry
- nfl_weeklystats_wk6.txt Prediction test set data for NFL week 6 for manual entry
- nfl_weeklystats_week7.csv Prediction test set data for NFL week 7  in .csv form for batch entry
