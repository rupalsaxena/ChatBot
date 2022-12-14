import random
from Multimedia import Multimedia
from Recommendation import Recommend
from Questions import Question

GREETINGS = [
    "Good luck with Evaluation today :) I am sure you are enjoying this :)",
    "I hope you are having a nice day :)",
    "Best wishes for you :D",
    "Good Luck :D",
    "Enjoy :D",
    "Happy Wednesday :D"
]
help_str = "Hello, I am Griot. \n I can answer following types of questions, examples attached with each type of question: \n FACTUAL QUESTIONS: Who is director of The Bridge on the River Kwai? \n EMBEDDING QUESTIONS: Who is screenwriter of The Masked Gang: Cyprus? \n  MULTIMEDIA QUESTIONS: Show me a picture of Halle Berry. \n RECOMMENDATION QUESTIONS: Recommend movies similar to Hamlet and Othello. \n I hope you enjoy playing with me :)"

def getResponse(msg, prior_obj):
    alg = Algorithm(msg, prior_obj)
    response = alg.get_reply()
    print("response:", response)
    return response

class Algorithm:
    def __init__(self, input, prior_obj):
        self.input = input
        self.greeting()
        self.help()

        if not self.is_help:
            if  not self.is_greeting: 
                self.prior_obj = prior_obj

                # load graph
                self.graph = self.prior_obj.get_graph()

                # question detection
                question_model = self.prior_obj.get_question_model()
                category = question_model.get_question_category(input.lower())


                if category != -1:
                    # process each question
                    if category == "multimedia":
                        self.reply = self.multimedia()
                    elif category == "recommendation":
                        self.reply = self.recommend()
                    else:
                        self.reply = self.question()
                else:
                    self.reply = help_str
            else:
                self.reply = random.choice(GREETINGS)
        else:
            self.reply = help_str

    def multimedia(self):
        mm = Multimedia(self.input, self.graph, self.prior_obj)
        response = mm.getResponse()
        return response
    
    def recommend(self):
        re = Recommend(self.input, self.graph, self.prior_obj)
        response = re.getResponse()
        return response

    def question(self):
        qe = Question(self.input, self.prior_obj, self.graph)
        response = qe.getResponse()
        return response

    def help(self):
        if self.input.lower() == "help":
            self.is_help = True
        else:
            self.is_help = False

    def greeting(self):
        list = self.input.split(" ")
        if len(list) < 3:
            self.is_greeting = True
        else:
            self.is_greeting = False

    def get_reply(self):
        return self.reply
