import string


class PreProcessFile(object):
    def __init__(self, path):
        self.path = path

    def read_file(self):
        with open(self.path, 'r') as f:
            words = f.read().splitlines()
        f.close()

        return words

    def clean_data(self):
        words = self.read_file()
        translator = str.maketrans('', '', string.punctuation)

        words = [word.strip(' ').replace(' ', '').translate(translator) for word in words]

        return words
