from flask.views import MethodView
from flask import Flask, jsonify, request , session
from flask_pymongo import PyMongo
import json
from flask import jsonify, request
import bcrypt
import jwt
from config import KEY_TOKEN_AUTH
import bcrypt
from flask_bcrypt import Bcrypt 
import binascii
from app import app

#Importacion de modelos
from Models.Qrcode import Qrcode
from Models.Conexion import * 
from Models.PeticionAgregar import Peticion
from Models.Carrito import Carrito
from Models.CrudMenu import CrudMenu

#inicializacion de clases importadas
crudMenu = CrudMenu()
peticion = Peticion()



'''
Clase CodigoQR
Responsable Michael Giraldo
Methods POST
'''

app.config["MONGO_URI"]='mongodb+srv://comApp:qawsed123@cluster0.adpmk.mongodb.net/comApp?retryWrites=true&w=majority'

mongo = PyMongo(app)
bcrypt = Bcrypt(app)


class QrCodeControllers(MethodView):

    def post(self):
        qrcode = Qrcode()

        answer = qrcode.qrcode()

        return jsonify({"Status": "Codigo generado",
                        "image" : answer
                        }), 200


class LoginAdminControllers(MethodView):
    def post(self):
        users = mongo.db.usuarios
        correo = request.get_json()['correo']
        password = request.get_json()['password']
        result = ""

        response = users.find_one({'correo': correo})
    # 'correo': response['correo']


        if response:
            if bcrypt.check_password_hash(response['password'], password):
                encoded_jwt = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=1000), 'correo': response['correo']}, KEY_TOKEN_AUTH , algorithm='HS256')
                return jsonify({"Status": "Login exitoso", "token": str(encoded_jwt),'correo': response['correo']}), 200    
                
            else:
                return jsonify({"error":"Invalid username and password"}),400
        else:
            return jsonify({"error":"Invalid username and password"}),400
        return result 




class RegisterUserControllers(MethodView):
    def post(self):
        
        users = mongo.db.usuarios
        existing_user = users.find_one({'correo' : request.json['correo']})
        correo = request.get_json()['correo']
        password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
        
        if existing_user is None:
            user_id = users.insert({
            
                'correo': correo,
                'password': password,
                
            })

            new_user = users.find_one({'_id': user_id})

            result = {'correo': new_user['correo'] + ' registered'}

            return jsonify({'result' : result}),200  

        return jsonify("el correo ya esta"),400


class CarritoCompras(MethodView):
    def get(self):
        
        data = mongo.db.carritoCompras.find({})
        listado_carrito = list(data)
        print(data,"esto el print")

        if data == None:
            data = []

        return(listado_carrito)

class MenuControllers(MethodView):
    def get(self):

        answer =  crudMenu.mostrar()
        return jsonify({"transaccion":True,"data":answer})


'''
Menu de platillo
Responsable Andres Taborda
Methods POST
'''
class CarritoCompras(MethodView):
    def get(self):

        answer =  crudMenu.mostrarcarrito()
        return jsonify({"transaccion":True,"data":answer})

class CrearMenuControllers(MethodView):
    def post(self):
        
        answer = crudMenu.crear()
        return(answer)


class MandarMenuControllers(MethodView):
    def post(self):
        
        answer = peticion.peticion()

        return jsonify({"transaccion": True, "mensaje": "Los datos se enviaron de forma exitosa"})

class EditarMenuControllers(MethodView):
    def put(self):
        answer = crudMenu.actualizar()

        return (answer)

class EliminarMenuControllers(MethodView):
    def post(self):
        answer = crudMenu.eliminar()

        return (answer) 
'''
Clase Carrito
Responsable Michael Giraldo
Methods POST
'''
class CarritoControllers(MethodView):

    def post(self):
        datos_token = ""
        idMesa = 1
        tokenR = request.headers.get('Authorization').split(" ")
        token = tokenR[1]
       
        datos_token = jwt.decode(token, KEY_TOKEN_AUTH , algorithms=['HS256'])
        # correo = datos_token.get("correo")

        json_req = request.get_json(force=True)
        idPlatillo = json_req["idPlatillo"]
 
        carrito = Carrito()
        
        carrito.idMesa = idMesa
        carrito.idPlatillo = idPlatillo
        
        answer = carrito.Add()

        return jsonify({"Status": "Platillo añadido correctamente",
                        }), 200



