from Algorithm import Algorithm
from Preprocess import Preprocess

questions = [
"Who is the director of Good Will Hunting?",
"Who directed The Bridge on the River Kwai?",
"Who is the director of Star Wars: Episode VI - Return of the Jedi?",
"Show me a picture of Halle Berry.",
"What does Julia Roberts look like?",
"Let me know what Sandra Bullock look like?",
"Who is the director of Game of Thrones?",
"Do you have any recommendation for Horror movies?",
"Who is the screenwriter of The Masked Gang: Cyprus?",
"What is the MPAA film rating of Weathering with You?",
"What is the genre of Good Neighbors?",
"Lord of the Rings is directed by whom?",
"Who directed Titanic?",
"What is the box office of The Princess and the Frog?",
"Can you tell me the publication date of Tom Meets Zizou?",
"Who is the executive producer of X-Men: First Class?",
"Hello, how are you?",
"Thank you so much"
]

prior_obj = Preprocess()
for question in questions:
    print("Question:", question)
    alg = Algorithm(question, prior_obj)
