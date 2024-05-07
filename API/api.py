from flask import Flask
from flask_restful import Api, Resource, reqparse
import random
#import py_diode_squares_v1
app = Flask(__name__)
api = Api(app)

items = [{
    'id': 0,
    'Model': '.MODEL 1N914 D (IS=4.33e-09 N=1.99 RS=0.654 CJ0=8.7e-13 VJ=0.223 M=0.0165 TT=1.32e-08)\n', 
    'model_sat': '(array([3.e-06, 6.e-05, 7.e-04, 3.e-03, 8.e-03, 3.e-02, 9.e-02, 7.e-01]), array([0.32602538, 0.4753935 , 0.5982751 , 0.67232232, 0.7244847 ,\n       0.80476002, 0.89876518, 1.39997382]))", "model_cap": "(array([ 0,  1,  2,  3,  7, 10, 14]), array([0.87026982, 0.84618589, 0.83788315, 0.83276249, 0.82174503,\n       0.81704716, 0.81260605]))", "rev_time": "(array([0.01 , 0.015, 0.035, 0.055]), array([3.97550045, 2.92980705, 1.44139751, 0.95812781]))'
}]


class Quote(Resource):
    def get(self, id=0):
        for item in items:
            if(item["id"] == id):
                return item, 200
        return "Something went wrong...", 404


api.add_resource(Quote, "/item", "/item/", "/item/<int:id>")
if __name__ == '__main__':
    app.run(host='0.0.0.0' ,debug=True)
