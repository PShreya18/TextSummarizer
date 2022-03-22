
from flask import Flask , render_template , request
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
app = Flask("Project")


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
                    sentenceValue [ sentence] = freq

    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]
    average = int(sumValues / len(sentenceValue))
    
    summary =""
    for sentence in sentences:
        if (sentence in sentenceValue) and (sentenceValue [sentence] > (1.2 * average)):
            summary += sentence
    #print(summary)
    return render_template("index.html",result=summary)
#Summarize()
app.run(host="localhost",port=8080)