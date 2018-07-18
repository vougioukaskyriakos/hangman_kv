import random
import logging
import configparser
import copy

from pre_process_file import PreProcessFile


class HangMan(object):
    hang = [
        ' +---+',
        ' |   |',
        '     |',
        '     |',
        '     |',
        '     |',
        '=======']

    man = {0: [' 0   |'], 1: [' 0   |', ' |   |'], 2: [' 0   |', '/|   |'], 3: [' 0   |', '/|\\  |'],
           4: [' 0   |', '/|\\  |', '/    |'], 5: [' 0   |', '/|\\  |', '/ \\  |']}

    pics = []

    def __init__(self):
        conf = configparser.ConfigParser()
        conf.read('config_files/config.ini')

        self.file_path = conf.get('hangman_std_config', 'hangman_lexicon')
        self.max_guess_init = int(conf.get('hangman_std_config', 'max_guess'))
        self.max_guess = copy.copy(self.max_guess_init)
        self.yes = conf.get('hangman_play', 'yes')
        self.no = conf.get('hangman_play', 'no')

        self.init_pics()

        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

        words = PreProcessFile(self.file_path).read_file()

        self.word_to_guess = (random.choice(words)).lower()
        self.guess_letter = ""
        self.correct_guessed_letters = []
        self.wrong_guessed_letters = []
        self.wrong_words = []
        self.init_hidden = ["_"] * len(self.word_to_guess)
        self.break_while = False

        self.welcome_message()

    def init_pics(self):
        i, j = 2, 0
        while len(self.hang) < self.max_guess_init:
            self.hang.insert(-1, '     |')

        self.pics.append(self.hang[:])
        for ls in self.man.values():
            pic, j = self.hang[:], 0
            for m in ls:
                pic[i + j] = m
                j += 1
            self.pics.append(pic)

        extra_item = '---  |'
        while len(self.pics) < self.max_guess_init:
            ls.append(extra_item)
            pic, j = self.hang[:], 0
            for r in ls:
                pic[i+j] = r
                j += 1
            self.pics.append(pic)
            extra_item.replace(' ', '-', 1)

    def print_pic(self, idx):
        for line in self.pics[idx]:
            logging.warning(line)

    def welcome_message(self):
        logging.info("welcome to hangman_old")
        logging.info("today's word has {} characters".format(len(self.word_to_guess)))
        self.print_init_word()
        logging.info("do you want to play ?")
        logging.info("type any of {} for yes or any of {} for no".format(self.yes, self.no))

    def print_init_word(self):
        logging.info("current word is:")
        logging.info("".join([x + " " for x in self.init_hidden]))

    def continue_game(self):
        self.print_current_guessed_word()
        self.print_guessed_letters()
        self.guess_letter = input()
        self.guess_letter = str(self.guess_letter).lower()

        if len(self.guess_letter) == 1:
            if self.guess_letter in (self.correct_guessed_letters + self.wrong_guessed_letters):
                logging.warning("you have already tried these letters")
            elif self.guess_letter in self.word_to_guess:
                self.correct_guessed_letters.append(self.guess_letter)
            else:
                self.wrong_letter()

        elif len(self.guess_letter) > 1:
            if self.guess_letter == self.word_to_guess:
                self.print_success()
            else:
                self.wrong_letter()
        else:
            logging.critical('please guess a letter or word')

    def print_current_guessed_word(self):
        if self.guess_letter != "":
            for i, x in enumerate(self.word_to_guess):
                if x == self.guess_letter:
                    self.init_hidden[i] = self.guess_letter
        self.print_init_word()

        if ''.join(self.init_hidden) == self.word_to_guess:
            self.print_success()

    def print_success(self):
        logging.critical("congratulations you have guessed the right word {}".format(self.word_to_guess))
        self.break_while = True
        self.play()

    def print_guessed_letters(self):
        logging.warning("you have {} tries left".format(self.max_guess))
        self.print_pic(self.max_guess_init - self.max_guess)
        logging.warning("wrong guessed letters {}".format(self.wrong_guessed_letters))
        logging.info("correct guessed letters {}".format(self.correct_guessed_letters))
        logging.info("guess a letter")

    def wrong_letter(self):
        self.wrong_guessed_letters.append(self.guess_letter)
        self.max_guess -= 1
        if self.max_guess == 0:
            logging.critical("no more tries left")
            logging.critical("game over")
            self.break_while = True
        else:
            self.continue_game()

        return self.max_guess

    def play(self):
        if self.break_while is False:
            choice = input().lower()
            while self.break_while is False:
                if choice in self.yes:
                    self.continue_game()
                elif choice in self.no:
                    self.break_while = True
                else:
                    logging.info("Please respond with 'yes' or 'no'")
                    logging.info("type any of {} for yes or any of {} for no".format(self.yes, self.no))
                    choice = input().lower()
        else:
            logging.info("thank you for playing")
            exit()
