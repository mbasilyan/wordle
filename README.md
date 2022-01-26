# my wordle "solver"
My goofy little script for playing [wordle](https://www.powerlanguage.co.uk/wordle/). It actually runs really slowly at first but once you've added some info (e.g. which letters are green, yellow, black) it goes much faster. The reason it's slow at first is the heuristic is expensive (see below).

There are two files:
* *wordledict.py* does nothing but load the list of winning words and possible words (these I just extracted from the Javascript on the site itself)
* *find_cands.py* uses the word lists to eliminate and score remaining viable words based on a heuristic. 

The way the heuristic works is it goes letter by letter through the candidate word and goes: if this letter was yellow, how many words would be eliminated? What if it was green? What if it was black? Then it adds up the eliminated counts with a weight for each and adds up each letter, penalizing a word for having duplicate letters. 

## To use:
* Download both files and put them in the same directory.
* Open the *find_cands.py* and find "SET THE CURRENT STATE OF THE BOARD HERE" section.
* Set the current state of the board by providing the green letters, yellow letters and black letters you've seen. 
* Comments in the code explain how to do it.
* Finally, run it with *python find_cands.py* as you usually would. 

![screenshot of it running](https://github.com/mbasilyan/wordle/blob/main/screenshot2.PNG?raw=true)
