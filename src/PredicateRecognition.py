import re
import Constants
import difflib
import pandas as pd
from nltk.corpus import stopwords
from Levenshtein import distance

# TODO: Make algo strong enough for spelling mistakes

class RecognizePredicate:
    def __init__(self, input, prior=None):
        self.prior = prior
        self.msg = input
        if self.prior is not None:
            self.input_list = self.get_cleaned_input(input)
    
    def get_predicate_ID(self):
        predicates, IDs = self.find_similar_words(cutoff=0.6)
        if len(predicates) >= 1:
            print("returning from find_similar_words")
            return (predicates, IDs)
        else:
            predicates, IDs = self.light_search()
            if len(predicates) >= 1:
                print("returning from light_search")
                return (predicates, IDs)
            else:
                predicates, IDs = self.medium_search()
                if len(predicates) >= 1:
                    return (predicates, IDs)
                else:
                    predicates, IDs = self.entensive_search(self.prior)
                    return (predicates, IDs)

    def get_cleaned_input(self, input):
        sentence = input.lower()
        words = sentence.split(" ")
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

    def light_search(self):
        result = self.prior.loc[self.prior['predicate'].isin(self.input_list)]
        predicates=result["predicate"].values
        IDs=result["ID"].values
        return predicates, IDs
    
    def strong_search(self):
        predicates = []
        ids = []
        for row in self.prior.iterrows():
            for word in row[1]["list"]:
                if re.search(word, self.msg):
                    predicates.append(row[1]["predicate"])
                    ids.append(row[1]["ID"])
        return predicates, ids
    
    def medium_search(self):
        predicates = []
        ids = []
        for row in self.prior.iterrows():
            if re.search(row[1]["predicate"], self.msg):
                predicates.append(row[1]["predicate"])
                ids.append(row[1]["ID"])
        return predicates, ids
    
    def entensive_search(self, search_from):
        predicates = []
        ids = []
        for word in self.input_list:
            df = search_from
            df["distance"] = df["predicate"].apply(lambda x: distance(x, word))
            df = df.loc[df["distance"]<3]
            if len(df)>0:
                predicates.extend(df["predicate"].values)
                ids.extend(df["ID"].values)
        return predicates, ids

    def find_similar_words(self, cutoff=0.6):
        predicates = []
        ids = []
        df = self.prior
        for word in self.input_list:
            id = self.match_id(word, df, cutoff=cutoff)
            if id != -1:
                predicates.append(word)
                ids.append(id)
        return predicates, ids

    def match_id(self, label, df, cutoff=0.6):
        id = -1
        df['predicate'] = df['predicate'].apply(lambda x: x.strip())
        closest_matches = difflib.get_close_matches(label, df['predicate'].tolist(), cutoff=cutoff)
        if len(closest_matches)>0:
            closest_match = closest_matches[0]
            id = df['ID'][df['predicate']==closest_match].tolist()
            return id[0]
        return id
    

















    