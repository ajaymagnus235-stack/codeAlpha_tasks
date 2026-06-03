from flask import Flask, render_template, request, jsonify
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

with open("faq.json", "r") as f:
    faqs = json.load(f)

questions = [faq["question"] for faq in faqs]

vectorizer = TfidfVectorizer()
question_vectors = vectorizer.fit_transform(questions)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_question = request.json["message"]

    user_vector = vectorizer.transform([user_question])

    similarity = cosine_similarity(user_vector, question_vectors)

    best_score = similarity.max()

    if best_score < 0.3:
        response = "Sorry, I don't know the answer to that question."
    else:
        best_match = similarity.argmax()
        response = faqs[best_match]["answer"]

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)