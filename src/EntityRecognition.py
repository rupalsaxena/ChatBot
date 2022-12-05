import os
import pandas as pd
import spacy  # version 3.0.6'
from Levenshtein import distance

class EntityRecognition:
    def __init__(self, input, prior_obj=None, humans=None, movies=None, entities=None):
        self.input = input
        if prior_obj is not None:
            self.humans = prior_obj.getHumans()
            self.movies = prior_obj.getMovies()
            self.entities_csv = prior_obj.getAllEntities()
        if humans is not None:
            self.humans = humans
        if movies is not None:
            self.movies = movies
        if entities is not None:
            self.entities_csv = entities
    
    def process(self):
        ent, ent_id = light_entity_recog(self.input)
        if len(ent_id) > 0 and None not in ent_id:
            return ent, ent_id 
        else:
            ent, ent_id = medium_entity_recog(self.input, self.humans, self.movies, self.entities_csv)
            if len(ent) > 0:
                return ent, ent_id
            else:
                print("Suggestion: apply another entity recognition")
        return [], []

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

def get_movies_nlp(input):
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(input)
    names = []
    for ent in doc.ents:
        names.append(ent.text)
    print(names)
    return names

def search_in_csv_files(entity, doc):
    doc["distance"] = doc["names"].apply(lambda x: distance(x, entity.lower()))
    df = doc.loc[doc["distance"]<2]
    if len(df) == 1:
        ids = df["ids"].values
        id = ids[0]
        return id
    if len(df) > 1:
        distances = list(df["distance"])
        ids = list(df["ids"])
        index = distances.index(min(distances))
        id = ids[index]
        return id
    else:
        return -1

def medium_entity_recog(input, humans, movies, entities_csv):
    entities = get_movies_nlp(input)
    final_entities = []
    ids = []
    if len(entities) > 0:
        for entity in entities:
            movie_id = search_in_csv_files(entity, movies)
            if movie_id == -1:
                human_id = search_in_csv_files(entity, humans)
                if human_id == -1:
                    entity_id = search_in_csv_files(entity, entities_csv)
                    if entity_id == -1:
                        final_entities.append(entity)
                        ids.append(-1)
                    else:
                        final_entities.append(entity)
                        ids.append(entity_id)
                else:
                    final_entities.append(entity)
                    ids.append(human_id)
            else:
                final_entities.append(entity)
                ids.append(movie_id)
    return final_entities, ids

def load_default_data():
    foldername = "data/all_data_folder"
    print("loading humans data")
    humans = pd.read_csv(os.path.join(foldername, "all_humans.csv"))
    humans["names"] = humans["names"].apply(lambda x: x.lower())
    print("loading movies data")
    movies = pd.read_csv(os.path.join(foldername, "all_movies.csv"))
    movies["names"] = movies["names"].apply(lambda x: x.lower())
    return humans, movies

def load_all_entities():
    foldername = "data/"
    print("loading all entity data")
    all_entities = pd.read_csv(os.path.join(foldername, "entity_mappings.csv"))
    all_entities = all_entities.astype(str)
    all_entities["label"] = all_entities["label"].apply(lambda x: x.lower())
    all_entities.rename(columns = {'label':'names'}, inplace = True)
    all_entities.rename(columns = {'wiki_code':'ids'}, inplace = True)
    all_entities.drop(columns='description', inplace=True)
    return all_entities

if __name__=="__main__":
    questions = [
    "Who is the director of Good Will Hunting?",
    "Who directed The Bridge on the River Kwai?",
    "Who is the director of Star Wars: Episode VI - Return of the Jedi?",
    "Show me a picture of Halle Berry.",
    "What does Julia Roberts look like?",
    "Let me know what Sandra Bullock look like?",
    "Who is the director of Game of Thrones?",
    "Do you have any recommendation for Horror movies?",
    "Recommend me some movies similar to The Masked Gang.",
    "Recommend movies similar to X-Men: First Class",
    "Recommend movies similar to Pocahontas, The Beauty and the Beast, The Lion King.",
    "Recommend me movies similar to The Bridge on the River Kwai",
    "Who is the screenwriter of The Masked Gang: Cyprus?",
    "What is the MPAA film rating of Weathering with You?",
    "What is the genre of Good Neighbors?",
    "What is the box office of The Princess and the Frog?",
    "Can you tell me the publication date of Tom Meets Zizou?",
    "Who is the executive producer of X-Men: First Class?"
    ]
    humans, movies = load_default_data()
    entities = load_all_entities()
    for question in questions:
        print(question)
        er = EntityRecognition(question, humans = humans, movies=movies, entities=entities)
        ent, ent_ids = er.process()
        print(ent, ent_ids)






        

    