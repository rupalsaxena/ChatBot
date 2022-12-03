import EntityRecognition as er
from PredicateRecognition import RecognizePredicate

# TODO: NER for entity recognition
# TODO: first query using questions which are ready
# TODO: check how recommendation and multimedia is working

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
        ent, ids = er.light_entity_recog(self.input)
        responses = []
        print("entities and ids:", ent, ids)
        for id in ids:
            response = self.graph.queryMultimedia(id)
            responses.extend(response)
        print("reply:", responses)
        return responses
    
    def recommend(self):
        ent, ids = er.light_entity_recog(self.input)
        print("entities and ids:", ent, ids)
        return -1

    def question(self, predicates):
        predicate, pred_ids = predicates
        if len(predicate) == 0:
            return "I don't understand it. Please rephrase the sentence."
        else:
            print("predicates and id:", predicate, pred_ids)
            ents, ent_ids = er.light_entity_recog(self.input)
            print("entities and ids:", ents, ent_ids)
            assert(len(ents)!=(ent_ids))
            if len(ent_ids) != 0:
                responses = []
                for ent_id in ent_ids:
                    if ent_id is not None:
                        for pred_id in pred_ids:
                            response = self.graph.queryFactual(ent_id, pred_id)
                            responses.extend(response)
                if len(responses) == 0:
                    print("Suggestion: Apply another query method")
                    return -1
                else:
                    return responses
            else:
                print("Suggestion: Apply another NER algo")
                print("Applying another entity recognition method")
                ab = er.medium_entity_recog(self.input)
                return -1

    def get_reply(self):
        return self.reply
