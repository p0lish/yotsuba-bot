import os
from flask import Flask
import random

app = Flask(__name__)


@app.route("/")
def hello():
    res = random.uniform(1, 10)
    return str(res)

def main():
    app.run(port=os.environ['PORT', 8080])


if __name__ == '__main__':
    main()
