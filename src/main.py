from flask import Flask
import codecs
import HTML_IMDB

app = Flask(__name__)


@app.route('/')
def display():
    myPage = codecs.open("MainPage.html", 'r')
    return myPage.read()


@app.route('/run')
def execute(string="http://www.imdb.com/title/tt5114356/"):
    return HTML_IMDB.main(string)

if __name__ == '__main__':
    app.run()
