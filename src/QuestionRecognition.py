import spacy
import classy_classification

class QuestionRecognition:
    def __init__(self):
        self.train_spacy_model()
    
    def train_spacy_model(self):
        data = {
            "questions":[
                "Who is the screenwriter of The Masked Gang: Cyprus?",
                "What is the MPAA film rating of Weathering with You?",
                "What is the genre of Good Neighbors?",
                "Who is the director of Good Will Hunting?",
                "Who directed The Bridge on the River Kwai?",
                "Who is the director of Star Wars: Episode VI - Return of the Jedi?",
                "Lord of the Rings is directed by whom?",
                "Who directed Titanic?",
                "What is the box office of The Princess and the Frog?",
                "Can you tell me the publication date of Tom Meets Zizou?",
                "Who is the executive producer of X-Men: First Class?",
                "Who directed Titanic?"
            ],
            "multimedia":[
                "Show me a picture of Halle Berry.",
                "What does Julia Roberts look like?",
                "Let me know what Sandra Bullock looks like.",
                "Show me photo of Adam Levine",
                "How does Adam Levine look like?",
                "Show me face of Adam Levine",
                "Show how Adam Levine look like",
                "What does Adam Levine look like",
                "Image of Amitabh Bachchan?",
                "Images of Julia Roberts?"
            ],
            "recommendation":[
                "Recommend movies similar to Hamlet and Othello.",
                "Give that I like The Lion King, Pocahontas, and The Beauty and the Beast, can you recommend some movies?",
                "Recommend movies like Nightmare on Elm Street, Friday the 13th, and Halloween.",
                "Recommendations for thriller movies",
                "Can you recommend me some horror movies?",
                "Best movies for 2022",
                "Suggestions for The Sky is Pink"
            ]
        }
        self.spacy_model = spacy.load('en_core_web_md')
        self.spacy_model.add_pipe("text_categorizer", 
            config={
                "data": data,
                "model": "spacy",
                "device":"cpu"
            }
        )
    
    def get_question_category(self, input):
        # TODO: Do a manual fix here by using commonly used words in question to recognize the type of question.
        # TODO: if manual fix is inconclusive then perform machine learning way
        # TODO: post machine learning, apply another manual fix using the commonly used entities
        predictions = self.spacy_model(input)._.cats
        best_prediction = max(predictions, key=predictions.get)
        return best_prediction

