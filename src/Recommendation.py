import random
from EntityRecognition import EntityRecognition

default_response = "I am not sure if I can find a recommendation for you. Can you rephrase it?"

class Recommend:
    def __init__(self, msg, graph, prior_obj):
        self.msg = msg
        self.graph = graph
        self.prior_obj = prior_obj
        self.embed = self.prior_obj.get_emb_obj()
        self.responses = []
        self._ents, self._ent_ids = self.recognize_entities()
        if self._ents != -1:
            self.process()
        self.chooseResponse()
    
    def process(self):
        print("looking for recommendations")
        for ent in self._ents:
            print("searching for :", ent)
            self.responses = self.embed.find_similar_entities(ent)
        print(self.responses)

    def recognize_entities(self):
        er = EntityRecognition(self.msg, prior_obj=self.prior_obj)
        ents, ent_ids = er.process()
        print("entities and ids:", ents, ent_ids)
        assert(len(ents)!=(ent_ids))
        if len(ents) == 0:
            return -1, -1
        else:
            return ents, ent_ids

    def chooseResponse(self):
        print("responses:", self.responses)
        if len(self.responses) > 1:
            init_resp = "Here are some recommendations:"
            response=""
            for i, resp in enumerate(self.responses):
                if i == 0:
                    response = response + " " + resp 
                else:
                    response = response + ", " + resp 
            response = init_resp + response 
        elif len(self.responses) == 0:
            response = default_response
        elif len(self.responses) == 1:
            response = self.responses[0]
            response = "I think it is "+response
        self._response = response

    def getResponse(self):
        return self._response