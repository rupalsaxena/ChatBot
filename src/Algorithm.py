import random
import EntityRecognition as er
from Multimedia import Multimedia
from Recommendation import Recommend
from Questions import Question
from PredicateRecognition import RecognizePredicate
"""
hndle film rating seperately
"""


default_response = "I am not sure what you mean. Can you rephrase it?"

def getResponse(msg, prior_obj):
    alg = Algorithm(msg, prior_obj)
    response = alg.get_reply()
    print("response:", response)
    return response

class Algorithm:
    def __init__(self, input, prior_obj):
        self.input = input
        self.prior_obj = prior_obj

        # load graph
        self.graph = self.prior_obj.get_graph()

        # question detection
        question_model = self.prior_obj.get_question_model()
        category = question_model.get_question_category(input.lower())
        print("question category:", category)

        if category == "multimedia":
            self.reply = self.multimedia()
        elif category == "recommendation":
            self.reply = self.recommend()
        else:
            prior_pred = self.prior_obj.get_all_predicates()
            rp = RecognizePredicate(self.input, prior=prior_pred)
            predicates = rp.get_predicate_ID()
            self.reply = self.question(predicates)

    def multimedia(self):
        mm = Multimedia(self.input, self.graph, self.prior_obj)
        response = mm.getResponse()
        return response
    
    def recommend(self):
        re = Recommend(self.input, self.graph, self.prior_obj)
        response = re.getResponse()
        return response

    def question(self, predicates):
        qe = Question(predicates, self.input, self.prior_obj, self.graph)
        response = qe.getResponse()
        return response

    def get_reply(self):
        return self.reply
