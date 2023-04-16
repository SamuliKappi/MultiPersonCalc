from flask import Flask, jsonify, request
import bcrypt
import re
import jwt
import datetime

app = Flask(__name__)
key = None
@app.post("/signup")
def sing_post():
    name = request.form.get("name")
    if (not re.match("^[A-Za-z0-9_-]*$", name)):
        return jsonify(status=404, message="Invalid name")
    hashpw = bcrypt.hashpw(request.form.get("password").encode('utf8'), bcrypt.gensalt(5))
    f = open("users.db", "ab")
    f.write(name.encode() + ":".encode() + hashpw + "\n".encode())
    f.close()
    return jsonify(status=200, message="Account created")
@app.post("/login")
def login_post():
    name = request.form.get("name")
    passw = request.form.get("password")
    f = open("users.db", "rb")
    lines = f.readlines()
    for line in lines:
        credentails = line.split(':'.encode(), 1)
        if(credentails[0] == name.encode()):
            if(bcrypt.checkpw(passw.encode(), credentails[1].strip())):
                print("logged in")
                f.close()
                jwttoken = jwt.encode({"exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=1)}, key, algorithm="HS256")
                return jsonify(status=200, message="Logged in", token=jwttoken)
    f.close()
    return jsonify(status=401, message="Wrong password or username")
@app.post("/test")
def test_post():
    token = request.form.get("token")
    try:
        jwt.decode(token.encode(), key, algorithms=["HS256"])
        print("Succ")
        return jsonify(status=200)
    except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
        print("Token has expired or is invalid")
        return jsonify(status=400)
        

if __name__ == "__main__":
    key = input("Enter any secret key for cookie generation: ")
    app.run(ssl_context='adhoc')