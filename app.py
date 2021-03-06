
from flask import Flask , render_template , request
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
from happytransformer import HappyTextToText
from happytransformer import TTSettings
import pyautogui
from PIL import Image
from pytesseract import *

app = Flask("Project")

summary=""
input_length=0
summary_length=0
input_wordlen=0
summary_wordlen=0

@app.route("/extract")
def extract():
    pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    image1=Image.open("img2.png")
    text=pytesseract.image_to_string(image1)
    #path=r"C:\Users\hp\OneDrive\Desktop\sem6\Mini Project\Project\img2.png"
    return "<html><center><img src=static\img2.png alt=Image></center><br><h3>Extracted Text:</h3>"+text+"</html>"


@app.route("/home")
def home():
        return render_template( "index.html" )

@app.route("/process" , methods = ["POST"] )
def Summarize():
    text=request.form["input"]
    #print(text)
    stopWords = set (stopwords.words ("english"))
    words = word_tokenize(text)
    freqTable = dict()

    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1
    
    sentences = sent_tokenize(text)
    sentenceValue = dict()
    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence. lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue [sentence] = freq

    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]
    average = int(sumValues / len(sentenceValue))
    
    #summary =""
    global summary
    for sentence in sentences:
        if (sentence in sentenceValue) and (sentenceValue [sentence] > (1.2 * average)):
            summary += sentence
    
    global input_length
    input_length=len(sentences)
    global summary_length
    summary_length=len(sent_tokenize(summary))
    global input_wordlen
    input_wordlen=len(words)
    global summary_wordlen
    summary_wordlen=len(word_tokenize(summary))
    return render_template("index.html",result=summary)

@app.route("/translate")
def translate():
    model=HappyTextToText("MARIAN","Helsinki-NLP/opus-mt-en-hi")
    args=TTSettings(min_length=0)
    rest=model.generate_text(summary,args=args)
    return render_template("index.html",translated_val=rest.text)

@app.route("/analyze")
def analyze():
    return "<html><h2><div style=color:red;>Sentences before summarization="+str(input_length)+"</div><br><div style=color:green;>Sentences after summarization="+str(summary_length)+"</div><br><br><div style=color:red;>Words before summarization="+str(input_wordlen)+"</div><br><div style=color:green;>Words after summarization="+str(summary_wordlen)+"</div></h2><html>"

app.run(host="localhost",port=8080)
