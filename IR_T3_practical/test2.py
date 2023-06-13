from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Sample documents
documents = ["This is a positive document javad", "This is reza a negative document", "Another positive document"]

# Create a vectorizer to convert text into numerical features
vectorizer = CountVectorizer()

# Vectorize the documents
X = vectorizer.fit_transform(documents)

# Labels for each document (0=negative, 1=positive)
y = ["1","2", "3"]

# Train a Naive Bayes classifier on the vectorized documents
clf = MultinomialNB()
clf.fit(X, y)

# Score a new document
new_doc = "javad javad"
new_vec = vectorizer.transform([new_doc])
prediction = clf.predict(new_vec)

print(prediction)  # Output: [1]
