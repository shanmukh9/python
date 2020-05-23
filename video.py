from flask import Flask
from string import Template
import requests

def is_url_ok(url):
    return 200 == requests.head(url).status_code

HTML_TEMPLATE = Template("""
<!DOCTYPE html>
<head>
   <title>My Video App</title>
   <style>
      body{
          text-align: center;
          background-color: #FFAAAA;
      }

      iframe{
          width: 80%;
          height: 600px;
          -webkit-animation: fun-function 2.5s linear infinite;
          -webkit-animation-direction: alternate;
          -moz-animation: fun-function 2.5s linear infinite;
          -moz-animation-direction: alternate;
      }

      @-webkit-keyframes fun-function{
        from{
          -webkit-transform: rotate(0deg) skew(-30deg);
        }
        to{
          -webkit-transform: rotate(360deg) skew(30deg);
        }
      }

      @-moz-keyframes fun-function{
        from{
          -moz-transform: rotate(0deg) skew(-30deg);
        }
        to{
          -moz-transform: rotate(360deg) skew(30deg);
        }
      }
   </style>
</head>
<body>
    <h2>${headline}</h2>
    <iframe src="https://www.youtube.com/embed/${youtube_id}?autoplay=1" frameborder="0" allowfullscreen></iframe>
</body>""")

app = Flask(__name__)
@app.route('/')
def homepage():
    return "Hello world"

@app.route('/videos/<vid>')
def videos(vid):
    youtube_url = 'https://www.youtube.com/watch?v=' + vid
    if True == is_url_ok(youtube_url):
        headline_html = """<a href="{url}">YouTube video: {id}</a>""".format(url=youtube_url, id=vid)
        all_html = HTML_TEMPLATE.substitute(headline=headline_html, youtube_id=vid)
    else:
        headline_html = """YouTube video <u>{id}</u> does not exist""".format(id=vid)
        all_html = HTML_TEMPLATE.substitute(headline=headline_html, youtube_id='dQw4w9WgXcQ')
    return all_html

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)