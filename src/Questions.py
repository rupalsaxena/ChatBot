import random
from EntityRecognition import EntityRecognition

"""
TODO: change the code to make it work for names rather than ids
"""
default_response = "I don't understand it. Can you rephrase it?"

class Question:
    def __init__(self, predicates, msg, prior_obj, graph):
        self.predicates = predicates
        self.msg = msg
        self.prior_obj = prior_obj
        self.graph = graph
        self.responses = []
        predicate, pred_ids = self.predicates
        self.embed = self.prior_obj.get_emb_obj()
        print("predicates and id:", predicate, pred_ids)
        if len(predicate) > 0:
            ents, ent_ids = self.recognize_entities()
            if ents != -1:
                self.process(ents, ent_ids, pred_ids)
        self.chooseResponse()

    def process(self, ent, ent_ids, pred_ids):
        if len(ent_ids) > 0:
            for ent_id in ent_ids:
                if ent_id is not None and ent_id != -1:
                    for pred_id in pred_ids:
                        response = self.graph.queryFactual(ent_id, pred_id)
                        self.responses.extend(response)
        print("responses:", self.responses)

        if len(self.responses) < 1:
            for ent in ent:
                for pred_id in pred_ids:
                    response = self.embed.apply_embedding(ent, pred_id)
                    self.responses.append(response)
            print("responses:", self.responses)

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
            response = random.choice(self.responses)
            response = "I think it is "+response
        elif len(self.responses) == 0:
            response = default_response
        elif len(self.responses) == 1:
            response = self.responses[0]
            response = "I think it is "+response
        self._response = response

    def getResponse(self):
        return self._response
