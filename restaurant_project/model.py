from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Training Data
x_train = [
"very tasty idli",
"good dosa",
"amazing veg biryani",
"excellent chicken biryani",
"delicious meals",
"awesome ice cream",
"bad noodles",
"worst juice",
"not tasty vada",
"very bad food"
]

y_train = [
"positive",
"positive",
"positive",
"positive",
"positive",
"positive",
"negative",
"negative",
"negative",
"negative"
]

vectorizer = CountVectorizer()

X = vectorizer.fit_transform(x_train)

model = MultinomialNB()

model.fit(X, y_train)

# Prediction Function
def predict_review(review):

    review_vector = vectorizer.transform([review])

    prediction = model.predict(review_vector)

    return prediction[0]