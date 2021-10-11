from flask import Flask, render_template, request, jsonify
from googletrans import Translator
from model_prediction import *
import csv


app = Flask(__name__)

text=""
predicted_emotion=""
predicted_emotion_img_url=""

translator = Translator()

@app.route("/")
def home():
    entries = show_entry()
    return render_template("index.html", entries=entries)
    

@app.route("/predict-emotion", methods=["POST"])
def predict_emotion():
    input_text = request.json.get("text")  

    if not input_text:
        return jsonify({
            "status": "error",
            "message": "Please enter some text to predict emotion!"
        }), 400
    else:      
        translated_input_text = translator.translate(input_text)       
       
        predicted_emotion, predicted_emotion_img_url = predict(translated_input_text.text)

        return jsonify({
            "data": {
                "predicted_emotion": predicted_emotion,
                "predicted_emotion_img_url": predicted_emotion_img_url
            },
            "status": "success"
        }), 200
        

@app.route("/save-entry", methods=["POST"])
def save_entry():
    date = request.json.get("date")            
    
    emotion = request.json.get("emotion")

    input_text = request.json.get("text")
    translated_input_text = translator.translate(input_text)  
    save_text = translated_input_text.text
    save_text = save_text.replace("\n", " ")
    entry = f'"{date}","{save_text}","{emotion}"\n'         
    with open("./static/assets/data_files/data_entry.csv", "a") as f:
        f.write(entry)
    return jsonify("Success")
           
                
if __name__ == "__main__":
    app.run(debug=True)