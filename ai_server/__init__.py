from flask import Flask
app = Flask(__name__)


from pathlib import Path
print(Path(__file__).parent)

(Path(__file__).parent / 'static1' / 'test').mkdir(parents=True, exist_ok=True)

@app.route('/')
def hello_world():
   return 'Hello world'

