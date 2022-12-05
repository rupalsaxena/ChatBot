import random
import EntityRecognition as er

"""
TODO: 
use moviedata to get path of image to be send to chatbot
add full entity recog algo here instead of small one
"""

default_response = "I am not sure what you mean. Can you rephrase it?"

class Multimedia:
    def __init__(self, input, graph, prior_obj):
        self.msg = input
        self.graph = graph
        self.prior_obj = prior_obj
        self.process()
        self.chooseResponse()
    
    def process(self):
        ent, ids = er.light_entity_recog(self.msg)
        print("entities and ids:", ent, ids)
        self.responses = []
        for id in ids:
            # self.responses.extend(self.graph.queryMultimedia(id))
            self.responses.extend(self.graph.queryMultimedia2(id))

    def chooseResponse(self):
        print("responses:", self.responses)
        if len(self.responses) > 1:
            response = random.choice(self.responses)
        elif len(self.responses) == 0:
            response = default_response
        elif len(self.responses) == 1:
            response = self.responses[0]
        self._response = response
    
    def getResponse(self):
        return self._response
