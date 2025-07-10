import random

class Question:
    def __init__(self, q_text, q_answer, incorrect_answers):
        self.text = q_text
        self.answer = q_answer
        self.options = incorrect_answers + [q_answer]
        random.shuffle(self.options)

