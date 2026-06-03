from flask import Flask, render_template, request
from deep_translator import GoogleTranslator

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    translated_text = ""
    text = ""
    target_language = "hi"
    error = ""

    if request.method == "POST":

        text = request.form.get("text", "").strip()
        target_language = request.form.get("target", "hi")

        if text:
            try:
                translated_text = GoogleTranslator(
                    source="auto",
                    target=target_language
                ).translate(text)
            except Exception:
                error = "Translation failed. Please try again."
        else:
            error = "Please enter text to translate."

    return render_template(
        "index.html",
        translated_text=translated_text,
        text=text,
        target_language=target_language,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)