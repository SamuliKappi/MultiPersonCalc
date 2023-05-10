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
operator = ""
num2 = ""

@app.errorhandler(404) 
def non_existant_route(error):
   return jsonify({"message":"I'm a teapot"}), 418

@app.post("/signup")
def sign_post():
    try:
      name = request.form.get("name")
      password = request.form.get("password")
    except:
        return jsonify(message="Invalid credentials"), 400

    if(len(password) < 4):
        return jsonify(message="Invalid password"), 404
    if (not re.match("^[A-Za-z0-9_-]{1,}$", name)):
        return jsonify(message="Invalid name"), 404
    
    f = open("users.db", "rb")
    lines = f.readlines()
    for line in lines:
        namesInDb = line.split(':'.encode(), 1)
        if(namesInDb[0] == name.encode()):
            return jsonify(message="Name is already taken"), 400
    f.close()

    hashpw = ph.hash(password)
    f = open("users.db", "ab")
    f.write(name.encode() + ":".encode() + hashpw.encode() + "\n".encode())
    f.close()
    return jsonify(), 201


@app.post("/login")
def login_post():
    try:
      name = request.form.get("name")
      password = request.form.get("password")
    except:
        return jsonify(message="Invalid credentials"), 400
    f = open("users.db", "rb")
    lines = f.readlines()
    for line in lines:
        credentails = line.split(':'.encode(), 1)
        if(credentails[0] == name.encode()):
            try:
              if(ph.verify(credentails[1].strip(), password)):
                  f.close()
                  jwttoken = jwt.encode({"exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=10)}, key, algorithm="HS256")
                  return jsonify(token=jwttoken, num1=num1, operator=operator, num2=num2), 202
              
            except argon2.exceptions.VerifyMismatchError:
                f.close()
                return jsonify(message="Invalid credentials"), 401
            
    f.close()
    return jsonify(message="Invalid credentials"), 401


def is_operator(char):
    if(re.match("[/*+-]", str(char))):
        return True
    else:
        return False

@app.post("/addNumber")
def add_number():
    try:
      token = request.form.get("token")
    except:
        return jsonify(message="Token is missing"), 401
    try:
        jwt.decode(token.encode(), key, algorithms=["HS256"])
    except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
        return jsonify(message="Token is invalid"), 401
    try:
        userinput = request.form.get("input")
    except:
        return jsonify(message="Input is invalid"), 400
    
    if(len(userinput) != 1):
        return jsonify(message="Should not be possible"), 418
    global operator, num1, num2
    if(operator == "" and not is_operator(userinput)):
        if(num1 == "0"):
            num1 = userinput
        else:
            num1 += str(userinput)
    elif(operator == "" and is_operator(userinput)):
        operator = str(userinput)
    elif(operator != "" and not is_operator(userinput) and re.match("[0-9]", userinput)):
        if(num2 == "0"):
            num2 = userinput
        else:
            num2 += str(userinput)

    print("Current state is " + str(num1) + " " + str(operator) + " " + str(num2))
    return jsonify(num1=num1, operator=operator, num2=num2), 200

@app.post("/reset")
def reset():
    try:
      token = request.form.get("token")
    except:
        return jsonify(message="Token is missing"), 401
    if(not validate_token(token)):
        return jsonify(message="Token is invalid"), 401
    global num1, num2, operator
    num1 = "0"
    num2 = "0"
    operator = None
    return jsonify(num1=num1, operator=operator, num2=num2, message="Succesfully reset"), 200

@app.get("/status")
def status():
    try:
      token = request.form.get("token")
    except:
        return jsonify(message="Token is missing"), 401
    if(not validate_token(token)):
        return jsonify(message="Token is invalid"), 401
    return jsonify(num1=num1, operator=operator, num2=num2), 200
@app.post("/equals")
def equals():
    try:
      token = request.form.get("token")
    except:
        return jsonify(message="Token is missing"), 401
    if(not validate_token(token)):
        return jsonify(message="Token is invalid"), 401
    global num1, num2, operator
    if(operator == "+"):
        result = int(num1) + int(num2)
        num1 = "0"
        num2 = ""
        operator = ""
        return jsonify(result=result), 200
    elif(operator == "*"):
        result = int(num1) * int(num2)
        num1 = "0"
        num2 = ""
        operator = ""
        return jsonify(result=result), 200
    elif(operator == "/"):
        result = int(num1) / int(num2)
        num1 = "0"
        num2 = ""
        operator = ""
        return jsonify(result=result), 200
    elif(operator == "-"):
        result = int(num1) - int(num2)
        num1 = "0"
        num2 = ""
        operator = ""
        return jsonify(result=result), 200
    elif(operator == "^"):
        result = int(num1) ** int(num2)
        num1 = "0"
        num2 = ""
        operator = ""
        return jsonify(result=result), 200
    else:
        return jsonify(messsage="Invalid operator"), 400
def validate_token(token):
    try:
        jwt.decode(token.encode(), key, algorithms=["HS256"])
    except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
        print("Token is invalid")
        return False
    return True

if __name__ == "__main__":
    key = secrets.token_bytes(32)
    app.run(ssl_context='adhoc')