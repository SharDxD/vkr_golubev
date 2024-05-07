from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
import random
import numpy as np
import math
import json
import csv
import sys

data_ex = {
"GUID": "1267fghhc19837hc",
"Order id": "6831gdh13",
"Extra_description": "Example of order.",
"Status": "Delivered",
"Time_stamp": "04-04-2023T20:20:00Z",
"Characteristics": {
            "Weight": "123",
            "Туре": "Bricks",
            "Category": "5"
            }
}

data_ex_create = {
"GUID": "4567ckshc38737hc",
"Order id": "1341smm82",
"Extra_description": "Example of order creation.",
"Status": "New",
"Time_stamp": "20-04-2023T00:00:00Z",
"Characteristics": {
            "Weight": "10",
            "Туре": "Glass",
            "Category": "2"
            }
}

tokens_main = {
    "user": "QwjyktdcIVhOwhjPjkwzqA",
    "s_user": "s1RxlS2H70Adq5jvuMF0Jg",
    "viewer": "epTmgDyfW6jL562-9sekPg",
    "editor": "XHHV8iY4SIoe13NH0gWxog",
    "admin": "Z3bMnDFqEICwveTAsbdJhw"
}

app = Flask(__name__)
api = Api(app)

def check_token(tokens_main,token):
    try:
        if token == tokens_main.get("user"):
            #print("user")
            return "user"
        elif token == tokens_main.get("s_user"):
            #print("s_user")
            return "s_user"
        elif token == tokens_main.get("viewer"):
            #print("viewer")
            return "viewer"
        elif token == tokens_main.get("editor"):
            #print("editor")
            return "editor"
        elif token == tokens_main.get("admin"):
            #print("admin")
            return "admin"
        else:
            #print("token unmatched or null")
            return ""
    except:
        #print("token invalid")
        return ""


class orders(Resource):
    def get(self):
        try:
            args = request.args
            try:
                id = args.get("id")
                token = args.get("tkn")
                #print(id)
                #print(token)
            except:
                id = ""
                token = ""

            tkn_chck = check_token(tokens_main, token)
            if tkn_chck != "":  
                if id == "0" and tkn_chck == "admin":
                    body = {    
                                "id": id,
                                "Order": data_ex,
                                "Status_code": 200,
                                "Message": "Order example."
                    }
                    return body, 200
                elif id !="0" and tkn_chck != "":
                    #mysql connect
                    body = {    
                                "id": id,
                                "Order": data_ex,
                                "Status_code": 200,
                                "Message": "Order."
                    }
                    return body, 200
                else:
                    
                    data = []
                    body = {
                                "Params of order you have sent": data,
                                "Status_code": 400,
                                "Error_message": "The sent params are Null or incorrect."
                    }
                    return body, 400
            else:
                body = {
                                "Status_code": 401,
                                "Error_message": "Token is invalid or null"
                }
                return body, 401

        except:
            body = {
                    "Status_code": 404,
                    "Error_message": "Something went wrong."                
            }
            return body, 404
        
class neworder(Resource):
    def post(self):
        try:
            args = request.args
            try:
                data = request.json
                #print(data)
            except:
                data = []
            try:
                token = args.get("tkn")
                #print(token)
            except:
                token = ""
            tkn_chck = check_token(tokens_main, token)          
            if tkn_chck != "":
                if data != [] and (tkn_chck == "editor" or tkn_chck == "admin" or tkn_chck == "s_user"  ) :
                    #mysql
                    body = {    
                                "Order": data_ex_create,
                                "Status_code": 200,
                                "Message": "Order has been created."
                    }
                    return body
                else:
                    body = {
                                "Order you have sent": data,
                                "Status_code": 400,
                                "Error_message": "The order are incorrect or you have no permisson."
                    }
                    return body, 400
            else:
                body = {
                                "Status_code": 401,
                                "Error_message": "Token is invalid or null"
                }
                return body, 401                

        except:
            body = {
                    "Status_code": 404,
                    "Error_message": "Something went wrong."                
            }
            return body, 404



api.add_resource(orders, "/order")
api.add_resource(neworder, "/neworder")

if __name__ == '__main__':
    app.run(host='0.0.0.0' ,debug=True)
