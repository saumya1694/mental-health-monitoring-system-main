import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

# Step 1: Load dataset
data = pd.read_csv("dataset.csv")

# Step 2: Split into input and output
X = data["text"]
y = data["label"]

# Step 3: Convert text into numbers using TF-IDF
vectorizer = TfidfVectorizer()
X_vector = vectorizer.fit_transform(X)

# Step 4: Train Machine Learning Model
model = LogisticRegression()
model.fit(X_vector, y)

# Step 5: Save the trained model
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("Model training completed successfully!")