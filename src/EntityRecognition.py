import spacy  # version 3.0.6'
from transformers import pipeline

def light_entity_recog(input):
    entity_ids = []
    entity_names = []
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("entityfishing")
    doc = nlp(input)
    for ent in doc.ents:
        entity_names.append(ent.text)
        entity_ids.append(ent._.kb_qid)
    return entity_names, entity_ids

def medium_entity_recog(input):
    er = pipeline('ner')
    print(er)



        

    