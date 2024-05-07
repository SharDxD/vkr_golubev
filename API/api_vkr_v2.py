from flask import Flask, request, jsonify, render_template, redirect 
from flask_restful import Api, Resource, reqparse
import random
import numpy as np
import math
import json
import csv
import sys
import mysql.connector


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

global tokens_main

tokens_main = {
    "user": "QwjyktdcIVhOwhjPjkwzqA",
    "s_user": "s1RxlS2H70Adq5jvuMF0Jg",
    "viewer": "epTmgDyfW6jL562-9sekPg",
    "editor": "XHHV8iY4SIoe13NH0gWxog",
    "admin": "Z3bMnDFqEICwveTAsbdJhw"
}

def upd_db(b):    
    #print("start")
    config = {
        'user': 'root',
        'password': 'O+yR_MT>',
        'database': 'orders'    
        }
    cnx = mysql.connector.connect(**config)
    try:
        order_id = b.get("order_id")
        #print(order_id)
        cursor = cnx.cursor()
        query = '''DELETE from ordr WHERE order_id LIKE %s'''
        cursor.execute(query, (order_id,))
        #print(cursor)
        cursor.close()
        #print("deleted")
    except:
        #print("not deleted")
        st = "not deleted"

    try:
        orders = b.get("orders")
        #print(orders)
        k = 1
        for m in orders:
            #print(k)
            #print(m.get("price"))
            #print(m.get("comment"))
            #print(m.get("datetime"))
            #print(m.get("name"))
            #print(m.get("category"))
            #print(m.get("num"))
            #print(m.get("status"))
            #print(m.get("weight"))
            cursor = cnx.cursor()
            query = '''INSERT INTO ordr (order_id, pos_id, comment, datetime, name, category, num, price, status, weight) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            data = (str(order_id), k, m.get("comment"), m.get("datetime"), m.get("name"), m.get("category"), m.get("num"), m.get("price"), m.get("status"), m.get("weight"))
            cursor.execute(query, (order_id, k, m.get("comment"), m.get("datetime"), m.get("name"), m.get("category"), m.get("num"), m.get("price"), m.get("status"), m.get("weight"),))
            cnx.commit()
            #print(cursor)
            cursor.close()
            k = k+1
            st = "success"
            #print("success")
    except:
        st = "not success"
        #print("not success")
    return st

def find_db(name_f):    
    config = {
        'user': 'root',
        'password': 'O+yR_MT>',
        'database': 'orders'    
        }
    cnx = mysql.connector.connect(**config)

    cursor = cnx.cursor()

    query = ("SELECT * FROM ordr WHERE order_id LIKE %s")

    name_b = name_f

    cursor.execute(query, (name_b,))
    body = {
    'order_id': name_b
    }
    k = 0
    for (order_id, pos_id, comment, datetime, name, category, num, price, status, weight) in cursor:
        b = {
                    str(pos_id): {"comment": comment, 
                    "datetime": datetime, 
                    "name": name,
                    "category": category, 
                    "num": num, 
                    "price": price, 
                    "status": status, 
                    'weight': weight
                    }
        }
        body.update(b)
        k = k+1
    #print(body)
    body.update({"number_of_rows": k})
    cursor.close()
    cnx.close()
    return body

app = Flask(__name__, template_folder='../templates', static_folder='../static')
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


class order_check(Resource):

    def post(self):
        try:
            try:
                body = request.json
            except:
                body = []
            if body != []:
                id = body.get("order_id")
                b = find_db(id)
                if b != {}:
                    st = upd_db(body)
                    #print("st", st)
                    if st == "success":
                        body = {
                                "Status_code": 200,
                                "Message": "Order updated."                
                        }
                        return body, 200                        
                    else:
                        body = {
                                "Status_code": 400,
                                "Message": "Order is not updated."                
                        }
                        return body, 400     
                else:
                    body = {
                                "Status_code": 400,
                                "Message": "Order is not updated."                
                    }
                    return body, 400
            else:
                body = {
                                "Status_code": 400,
                                "Message": "Order is not updated."                
                }
                return body, 400             
        except:
            body = {
                    "Status_code": 404,
                    "Error_message": "Something went wrong."                
            }
            return body, 404
        
    def get(self):
        try:
            args = request.args
            try:
                order_id = args.get("order_id")
                #print(order_id)
            except:
                order_id = ""

            if order_id != "":
                b = find_db(order_id)
                #print(b)
                if b != []:
                    #mysql
                    return b, 200

                else:
                    body = {
                                "Status_code": 400,
                                "type": 0,
                                "Error_message": "No such order."
                    }
                    return body, 400
            else:
                body = {
                                "Status_code": 404,
                                "Error_message": "Something went wrong."
                }
                return body, 404                

        except:
            body = {
                    "Status_code": 404,
                    "Error_message": "Something went wrong."                
            }
            return body, 404
        
class token_check(Resource):
    def get(self):
        try:
            args = request.args
            try:
                token = args.get("token")
                #print(token)
            except:
                token = ""
            tkn_chck = check_token(tokens_main, token)          
            if tkn_chck != "":
                if tkn_chck == "editor":
                    #mysql
                    body = {    
                                "Status_code": 200,
                                "type": 3,
                                "Message": "Token is valid. Role: editor."
                    }
                    return body, 200
                elif tkn_chck == "admin":
                    #mysql
                    body = {    
                                "Status_code": 200,
                                "type": 5,
                                "Message": "Token is valid. Role: admin."
                    }
                    return body, 200
                elif tkn_chck == "s_user":
                    #mysql
                    body = {    
                                "Status_code": 200,
                                "type": 4,
                                "Message": "Token is valid. Role: s_user."
                    }
                    return body, 200
                elif tkn_chck == "user":
                    #mysql
                    body = {    
                                "Status_code": 200,
                                "type": 2,
                                "Message": "Token is valid. Role: user."
                    }
                    return body, 200
                elif tkn_chck == "viewer":     
                    #mysql
                    body = {    
                                "Status_code": 200,
                                "type": 1,
                                "Message": "Token is valid. Role: viewer."
                    }
                    return body, 200
                else:
                    body = {
                                "Status_code": 400,
                                "type": 0,
                                "Error_message": "You have no permisson."
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



api.add_resource(order_check, "/order")
api.add_resource(token_check, "/token_chk")

@app.route("/orders")
def orders_page():
    return render_template("home_default.html")

@app.route("/order_qr")
def orders_qr():
    try:
        args = request.args
        id = args.get("order_id")
        try:
            b = json.dumps(find_db(id))
            #data = jsonify(b)
            #b = "'"+str(b)+"'"
            #print(b)
        except:
            data = [] 
        return render_template("home_v2.html", data=b, json=json)
    except:   
        return render_template("home_v2.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0' ,debug=True)
