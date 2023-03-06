import json

class Recipe:
    def __init__(self, number, title, photo, text, time, place, ingredients):
        self.number = number
        self.title = title
        self.photo = photo
        self.text = text
        self.time = time
        self.place = place
        self.ingredients = ingredients

    @staticmethod
    def load_json(filename):
        with open(filename, 'r', encoding='utf-8') as infile:
            data = json.load(infile)
        return list(data)
