import os
import pandas as pd
import Constants
from nltk.corpus import stopwords
from Graphs import Graphs
from QuestionRecognition import QuestionRecognition


class Preprocess:
    def __init__(self):
        self.datapath="data"
        self.load_predicates()
        self.load_default_data()
        self.question_model = QuestionRecognition()
        self.g = Graphs()
    
    def load_default_data(self):
        foldername = "data/all_data_folder"
        print("loading humans data")
        self.humans = pd.read_csv(os.path.join(foldername, "all_humans.csv"))
        print("loading movies data")
        self.movies = pd.read_csv(os.path.join(foldername, "all_movies.csv"))
        print("loading character data")
        self.chars = pd.read_csv(os.path.join(foldername, "all_character.csv"))
        print("loading genres data")
        self.genre = pd.read_csv(os.path.join(foldername, "all_genres.csv"))
        print("loading awards data")
        self.awards = pd.read_csv(os.path.join(foldername, "all_awards.csv"))

    def getDefaultData(self):
        return self.humans, self.movies, self.chars, self.genre, self.awards

    def load_predicates(self):
        self.df_pred = pd.DataFrame(columns=['ID', 'predicate'])
        files = os.listdir(self.datapath)
        for filename in files:
            if filename.startswith("predicate"):
                self.filepath = os.path.join(self.datapath, filename)
                name = filename.split(".")[0]
                if name == "predicate_1":
                    self.df_pred = pd.concat([self.df_pred, self.load_pred_1()])
                if name == "predicate_2":
                    self.df_pred = pd.concat([self.df_pred, self.load_pred_2()])
                if name == "predicate_3":
                    self.df_pred = pd.concat([self.df_pred, self.load_pred_3()])
        self.df_pred["predicate"] = self.df_pred["predicate"].apply(lambda x: str(x).lower())
        self.df_pred = self.df_pred.drop_duplicates()
        self.df_pred["list"] = self.df_pred["predicate"].apply(lambda x: self.remove_stopwords(x))
        self.df_pred.dropna(inplace=True)
        self.df_pred.reset_index(drop=True, inplace=True)

    def load_pred_1(self):
        df = pd.read_csv(self.filepath)
        df.rename(columns={'Title':'predicate'}, inplace=True)
        df = df[['ID','predicate']]
        print("predicate file 1 loaded")
        return df
    
    def load_pred_2(self):
        df = pd.read_csv(self.filepath)
        df.rename(columns={'label': 'predicate'}, inplace=True)
        df.rename(columns={'wiki_code': 'ID'}, inplace=True)
        df = df[['ID','predicate']]
        print("predicate file 2 loaded")
        return df
    
    def load_pred_3(self):
        df = pd.read_csv(self.filepath)
        df.rename(columns={'Property_pastedval': 'predicate'}, inplace=True)
        df.rename(columns={'Name of Relation': 'ID'}, inplace=True)
        df = df[['ID','predicate']]
        df['predicate'] = df['predicate'].apply(lambda x: x.split("(")[0])
        print("predicate file 3 loaded")
        return df
    
    def get_all_predicates(self):
        return self.df_pred
    
    def get_question_model(self):
        return self.question_model
    
    def get_graph(self):
        return self.g
    
    def remove_stopwords(self, input):
        # removing stopwords and useless words from input
        words = input.split(" ")
        stop_words = stopwords.words('english')
        stop_words.extend(Constants.USELESS_WORDS)

        filtered_input = []
        for word in words:
            for char in Constants.SPECIAL_CHARS:
                if char in word:
                    word = word.replace(char, "")
            if word not in stop_words:
                filtered_input.append(word)
        return filtered_input

if __name__=="__main__":
    p = Preprocess()