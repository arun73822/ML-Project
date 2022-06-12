from flask import Flask
from flask_cors import cross_origin

app=Flask(__name__)

@app.route('/',methods=['POST','GET'])
@cross_origin()
def test():
    return " CI/CD and CT"

if __name__=='__main__':
    app.run(debug=True)  