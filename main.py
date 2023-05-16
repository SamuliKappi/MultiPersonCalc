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

#Default return for all wrong endpoints
@app.errorhandler(404) 
def non_existant_route(error):
   return jsonify({"message":"I'm a teapot"}), 418

@app.post("/signup")
def sign_post():
    #Verifying that request contains correct input
    try:
      name = request.form.get("name")
      password = request.form.get("password")
    except:
        return jsonify(message="Invalid credentials"), 400
    #Checking that password length is 8 or more characters long
    if(len(password) < 8):
        return jsonify(message="Invalid password"), 404
    #Matching username with regex to validate characters
    if (not re.match("^[A-Za-z0-9_-]{1,}$", name)):
        return jsonify(message="Invalid name"), 404
    #Since this is in the backend we can assume users.db exists
    f = open("users.db", "rb")
    lines = f.readlines()
    #Checking if the name already exists
    for line in lines:
        namesInDb = line.split(':'.encode(), 1)
        if(namesInDb[0] == name.encode()):
            return jsonify(message="Name is already taken"), 400
    f.close()
    #Hashing password with argon2id using default parameters ~50ms hash time
    hashpw = ph.hash(password)
    f = open("users.db", "ab")
    f.write(name.encode() + ":".encode() + hashpw.encode() + "\n".encode())
    f.close()
    return jsonify(), 201


@app.post("/login")
def login_post():
    #Verifying that request contains correct input
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
              #verifying that password matches the hash in the db
              if(ph.verify(credentails[1].strip(), password)):
                  f.close()
                  #Creating jwt token for the session
                  jwttoken = jwt.encode({"exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=10)}, key, algorithm="HS256")
                  return jsonify(token=jwttoken, num1=num1, operator=operator, num2=num2), 202
              
            except argon2.exceptions.VerifyMismatchError:
                f.close()
                return jsonify(message="Invalid credentials"), 401
            
    f.close()
    return jsonify(message="Invalid credentials"), 401


def is_operator(char):
    if(re.match("[/*+^-]", str(char))):
        return True
    else:
        return False

@app.post("/addNumber")
def add_number():
    #Verifying that request contains correct input
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
    #Validating that userinput is exactly 1 char long
    if(len(userinput) != 1):
        return jsonify(message="I'm a teapot"), 418
    global operator, num1, num2
    #Logic and further input validation for adding of a number or an operator
    if(operator == "" and re.match("[0-9]", userinput)):
        if(num1 == "0"):
            num1 = userinput
        elif(num1 == "-0"):
            num1 = "-" + userinput
        elif(len(num1) < 10):
            num1 += str(userinput)
    elif(is_operator(userinput)):
        operator = str(userinput)
    elif(operator != "" and re.match("[0-9]", userinput)):
        if(num2 == "0"):
            num2 = userinput
        elif(num2 == "-0"):
            num2 = "-" + userinput
        elif(len(num2) < 10):
            num2 += str(userinput)

    print("Current state is " + str(num1) + " " + str(operator) + " " + str(num2))
    return jsonify(num1=num1, operator=operator, num2=num2), 200

@app.post("/reset")
def reset():
    #Verifying that request contains correct input
    try:
      token = request.form.get("token")
    except:
        return jsonify(message="Token is missing"), 401
    if(not validate_token(token)):
        return jsonify(message="Token is invalid"), 401
    global num1, num2, operator
    num1 = "0"
    num2 = ""
    operator = ""
    return jsonify(num1=num1, operator=operator, num2=num2), 200

@app.post("/erase")
def erase():
    #Verifying that request contains correct input
    try:
      token = request.form.get("token")
    except:
        return jsonify(message="Token is missing"), 401
    if(not validate_token(token)):
        return jsonify(message="Token is invalid"), 401
    global num1, num2, operator
    if(num2 != ""):
        if(num2[0] == "-" and len(num2) == 2):
            num2 = ""
        else:
          num2 = num2[:-1]
        return jsonify(num1=num1, operator=operator, num2=num2), 200
    elif(operator != ""):
        operator = ""
        return jsonify(num1=num1, operator=operator, num2=num2), 200
    else:
        
        if(len(num1) == 1 or (len(num1) == 2 and num1[0] == "-")):
            num1 = "0"
        else:
            num1 = num1[:-1]
        return jsonify(num1=num1, operator=operator, num2=num2), 200
    
@app.post("/swap")
def swap():
    #Verifying that request contains correct input
    try:
      token = request.form.get("token")
    except:
        return jsonify(message="Token is missing"), 401
    if(not validate_token(token)):
        return jsonify(message="Token is invalid"), 401
    global num1, num2, operator
    if(num2 != ""):
        if(num2[0] == "-"):
          num2 = num2[1:]
        else:
          num2 = "-" + num2
        return jsonify(num1=num1, operator=operator, num2=num2), 200
    else:
        if(num1[0] == "-"):
          num1 = num1[1:]
        else:
          num1 = "-" + num1
        return jsonify(num1=num1, operator=operator, num2=num2), 200

@app.post("/status")
def status():
    #Verifying that request contains correct input
    try:
      token = request.form.get("token")
    except:
        return jsonify(message="Token is missing"), 401
    if(not validate_token(token)):
        return jsonify(message="Token is invalid"), 401
    return jsonify(num1=num1, operator=operator, num2=num2), 200
@app.post("/equals")
def equals():
    #Verifying that request contains correct input
    try:
      token = request.form.get("token")
    except:
        return jsonify(message="Token is missing"), 401
    if(not validate_token(token)):
        return jsonify(message="Token is invalid"), 401
    global num1, num2, operator
    #Logic for math
    if(num2 == "" and is_operator(operator)):
        num2 = num1
    if(operator == "+"):
        num1 = str(int(num1) + int(num2))
        num2 = ""
        operator = ""
    elif(operator == "*"):
        num1 = str(int(num1) * int(num2))
        num2 = ""
        operator = ""
    elif(operator == "/"):
        if(num2 == "0" or num2 == "-0"):
            num1 = "0"
        else:
          num1 = str(int(num1) // int(num2))
        num2 = ""
        operator = ""
    elif(operator == "-"):
        num1 = str(int(num1) - int(num2))
        num2 = ""
        operator = ""
    elif(operator == "^"):
        if(len(num2) > 2):
          num1 = "0"
        else:
          num1 = str(int(num1) ** int(num2))
        num2 = ""
        operator = ""
        
    if (len(num1) > 10):
        num1 = "0"
    return jsonify(num1=num1, operator=operator, num2=num2), 200


def validate_token(token):
    try:
        jwt.decode(token.encode(), key, algorithms=["HS256"])
    except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
        print("Token is invalid")
        return False
    return True

if __name__ == "__main__":
    #Generating 32byte secret key that is later used for JWT generation
    key = secrets.token_bytes(32)
    #Running server over HTTPS generating certificate and keys on the fly
    app.run(ssl_context='adhoc')