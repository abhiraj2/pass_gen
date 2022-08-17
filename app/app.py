import random
from re import L
import numpy as np
from flask_restful import Api, Resource, reqparse
from flask import request, jsonify, Flask, make_response, render_template




alpha_dic = {
    'a' : 0,
    'b' : 1,
    'c' : 2,
    'd' : 3,
    'e' : 4,
    'f' : 5,
    'g' : 6,
    'h' : 7,
    'i' : 8,
    'j' : 9,
    'k' : 10,
    'l' : 11,
    'm' : 12,
    'n' : 13,
    'o' : 14,
    'p' : 15,
    'q' : 16,
    'r' : 17,
    's' : 18,
    't' : 19,
    'u' : 20,
    'v' : 21,
    'w' : 22,
    'x' : 23,
    'y' : 24,
    'z' : 25,
}

def reverse_dic(mydict, val):
    return list(mydict.keys())[list(mydict.values()).index(val)]

def eq_len(fi_ph, sec_ph):
    i=0
    res = ''
    while len(res) < len(fi_ph):
        if i<len(sec_ph):
            res += sec_ph[i]
            i += 1
        else:
            i = 0
    return res

def gen_pas(fi_ph, sec_ph):
    pin = ""
    sec_ph = eq_len(fi_ph, sec_ph)
    for i in range(len(fi_ph)):
        res = (alpha_dic[fi_ph[i]] + alpha_dic[sec_ph[i]])%26
        choice = np.random.random_sample(2)
        if choice[0] > 0.3:
            if choice[1] > 0.5:
                pin += reverse_dic(alpha_dic, res).upper()
            else: 
                pin += reverse_dic(alpha_dic, res).lower()
        else:
            pin += str(res)
    return pin



app = Flask(__name__)
api = Api(app)

class Hello(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'),200,headers)

api.add_resource(Hello, '/')

class GenPass(Resource):
    def get(self):
        parser = reqparse.RequestParser()  
        parser.add_argument('phrase', required=True)
        parser.add_argument('key', required=True)
        args = parser.parse_args()
        args['phrase'] =  args['phrase'].lower()
        args['key'] =  args['key'].lower()
        pas = gen_pas(args['phrase'], args['key'])
        dic = {
            'pass' : pas,
            'return' : 200
        }
        return jsonify(dic)

api.add_resource(GenPass, '/genpass')

if __name__ == '__main__':
    app.run()