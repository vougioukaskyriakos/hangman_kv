Files explanation:
-words.txt : is the file that contains all the words that hangman will use
(located in data directory) user can add/delete more words
-Config.ini : Using configuration file in order to configure max tries and lexicon (etc)
(located in config_files directory) user can change parameters even point to another file
-pre_process_file.py : Separate class for pre processing data in order to create lexicon
-hangman.py : Class that contains the business logic of hangman:
    -complies with the rules noted
    -randomly choosing a word from external file
    -contains dynamic schemas of hangman related to the configuration of the max tries
    -printing to logging instead of having a simple print os sys.stdout.write
-main.py this is the main class that runs the application

in order to run the project:
-Make sure you have installed python 3.x
-Copy the project in a directory of your desire
-Through command line access project root
-type in command line: python main.py
-enjoy :)








