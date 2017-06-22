import os
from flask import Flask
import random

app = Flask(__name__)


@app.route("/")
def hello():
    res = random.uniform(1, 10)
    return str(res)

def main():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)



if __name__ == '__main__':
    main()
