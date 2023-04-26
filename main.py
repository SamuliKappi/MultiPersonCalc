from flask import Flask, jsonify, request
import argon2
import re
import jwt
import datetime
import secrets

ph = argon2.PasswordHasher()
app = Flask(__name__)
key = None
num1 = "0"
operator = None
num2 = "0"

@app.post("/signup")
def sign_post():
    name = request.form.get("name")
    if (not re.match("^[A-Za-z0-9_-]*$", name)):
        return jsonify(status=404, message="Invalid name"), 404
    
    f = open("users.db", "rb")
    lines = f.readlines()
    for line in lines:
        namesInDb = line.split(':'.encode(), 1)
        if(namesInDb[0] == name.encode()):
            return jsonify(status=400, message="Name is already taken"), 400
    f.close()

    hashpw = ph.hash(request.form.get("password"))
    f = open("users.db", "ab")
    f.write(name.encode() + ":".encode() + hashpw.encode() + "\n".encode())
    f.close()
    return jsonify(status=201, message="Account created"), 201


@app.post("/login")
def login_post():
    name = request.form.get("name")
    password = request.form.get("password")

    f = open("users.db", "rb")
    lines = f.readlines()
    for line in lines:
        credentails = line.split(':'.encode(), 1)
        if(credentails[0] == name.encode()):
            try:
              if(ph.verify(credentails[1].strip(), password)):
                  print("logged in")
                  f.close()
                  jwttoken = jwt.encode({"exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=10)}, key, algorithm="HS256")
                  return jsonify(status=202, message="Logged in", token=jwttoken, num1=num1, operator=operator, num2=num2), 202
              
            except argon2.exceptions.VerifyMismatchError:
                f.close()
                return jsonify(status=401, message="Wrong password or username"), 401
            
    f.close()
    return jsonify(status=401, message="Wrong password or username"), 401


@app.post("/test")
def test_post():
    token = request.form.get("token")
    try:
        jwt.decode(token.encode(), key, algorithms=["HS256"])
        print("Succ")
        return jsonify(status=202), 202
    except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
        print("Token has expired or is invalid")
        return jsonify(status=401), 401

def is_operator(char):
    if(re.match("[/*+-]", str(char))):
        return True
    else:
        return False

@app.post("/addNumber")
def add_number():
    token = request.form.get("token")
    try:
        jwt.decode(token.encode(), key, algorithms=["HS256"])
        print("Succ")
    except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
        print("Token has expired or is invalid")
        return jsonify(status=401), 401
    userinput = request.form.get("input")
    if(len(userinput) != 1):
        return jsonify(status=418, message="Should not be possible"), 418
    global operator, num1, num2
    if(operator == None and not is_operator(userinput)):
        if(num1 == "0"):
            num1 = userinput
        else:
            num1 += str(userinput)
    elif(operator == None and is_operator(userinput)):
        operator = str(userinput)
    elif(operator != None):
        if(num2 == "0"):
            num2 = userinput
        else:
            num2 += str(userinput)

    print("Current state is " + str(num1) + " " + str(operator) + " " + str(num2))
    return jsonify(status=200, num1=num1, operator=operator, num2=num2), 200

@app.post("/reset")
def reset():
    token = request.form.get("token")
    if(not validate_token(token)):
        return jsonify(status=401, message="Token has expired or is invalid"), 401
    global num1, num2, operator
    num1 = "0"
    num2 = "0"
    operator = None
    return jsonify(status=200, num1=num1, operator=operator, num2=num2, message="Succesfully reset"), 200

@app.get("/status")
def status():
    token = request.form.get("token")
    if(not validate_token(token)):
        return jsonify(status=401, message="Token has expired or is invalid"), 401
    return jsonify(status=200, num1=num1, operator=operator, num2=num2), 200
@app.post("/equals")
def equals():
    token = request.form.get("token")
    if(not validate_token(token)):
        return jsonify(status=401, message="Token has expired or is invalid"), 401
    global num1, num2, operator
    if(operator == "+"):
        result = int(num1) + int(num2)
        num1 = "0"
        num2 = "0"
        operator = None
        return jsonify(status=200, result=result), 200
    elif(operator == "*"):
        result = int(num1) * int(num2)
        num1 = "0"
        num2 = "0"
        operator = None
        return jsonify(status=200, result=result), 200
    elif(operator == "/"):
        result = int(num1) / int(num2)
        num1 = "0"
        num2 = "0"
        operator = None
        return jsonify(status=200, result=result), 200
    elif(operator == "-"):
        result = int(num1) - int(num2)
        num1 = "0"
        num2 = "0"
        operator = None
        return jsonify(status=200, result=result), 200
def validate_token(token):
    try:
        jwt.decode(token.encode(), key, algorithms=["HS256"])
    except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
        print("Token has expired or is invalid")
        return False
    return True

if __name__ == "__main__":
    key = secrets.token_bytes(32)
    app.run(ssl_context='adhoc')