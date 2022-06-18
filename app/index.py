
from flask import Flask, jsonify, request, make_response
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/proyectalien'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

#<--Tabla en base de datos
class Alien(db.Model):
    alien_id = db.Column(db.Integer, primary_key=True)
    alien_usuario = db.Column(db.String(30))
    alien_nombre = db.Column(db.String(30))
    alien_ap = db.Column(db.String(30))
    alien_am = db.Column(db.String(30))
    alien_correo = db.Column(db.String(100))
    alien_contrasenia = db.Column(db.String(300))
    alien_nac = db.Column(db.Date())
    alien_status = db.Column(db.String(30))

    def __init__(self, usuario, nombre, ap, am, correo, contrasenia, nac, status):
        self.alien_usuario = usuario
        self.alien_nombre = nombre
        self.alien_ap = ap
        self.alien_am = am
        self.alien_correo = correo
        self.alien_contrasenia = contrasenia
        self.alien_nac = nac
        self.alien_status = status

db.create_all()

#<--Esquema de la tabla alien-->
class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('alien_id', 'alien_usuario', 'alien_nombre', 'alien_ap', 'alien_am', 'alien_correo', 'alien_contrasenia', 'alien_nac', 'alien_status')
categoria_schema = CategoriaSchema() #<--Una respuesta-->
categorias_schema = CategoriaSchema(many=True)#<--Varias respuestas-->


#<--objetoAlien(GET)-->
@app.route('/aliens', methods=['GET'])
def get_aliens():
    all_aliens = Alien.query.all()
    result = categorias_schema.dump(all_aliens)
    return jsonify(result)


#<--registrarAlien(POST)-->
@app.route('/aliens', methods=['POST'])
def reg_alien():
    data = request.get_json(force=True)
    hash_contrasenia = generate_password_hash(data['alien_contrasenia'], method='sha256')
    usuario = data['alien_usuario']
    nombre =  data['alien_nombre']
    ap = data['alien_ap']
    am = data['alien_am']
    correo = data['alien_correo']
    
    nac = data['alien_nac']
    status = data['alien_status']

    registro_alien = Alien(usuario, nombre, ap, am, correo, hash_contrasenia, nac, status )
    db.session.add(registro_alien)
    db.session.commit()
    return categoria_schema.jsonify(registro_alien)


#<--loginAlien-->
@app.route('/login', methods=['GET','POST'])
def log_alien():
    auth = request.authorization
    data = request.get_json(force=True)
    auth.usuario = data['alien_usuario']
    auth.contrasenia =  data['alien_contrasenia']
    

    if not auth or not auth.usuario or not auth.contrasenia:
        return jsonify({'Estatus' : 'Sin acceso'})

    
    alien = Alien.query.filter_by(alien_usuario=auth.usuario).first()

    if not alien:
        return jsonify({'Mensaje': 'Sin acceso'})

    if check_password_hash(alien.alien_contrasenia, auth.contrasenia):
        return jsonify({'Mensaje':'Con acceso'})

    
    return jsonify({'Estatus' : 'Sin acceso'})




#<--Mensaje de bienvenida--> 
@app.route('/inicio', methods=['GET'])
def index():
    mensaje = [{"Mensaje":"Bienvenido al apiAlien"}, {"Integrantes":"Raul Estrada, " + "Jesus Acosta, " + "Eduardo Paz, " + "Calos Manuel, " + "Ulises Montana, " + "Hector Virrueta, " + "Jorge Alberto"}]
    
    return jsonify(mensaje)

if __name__ == '__main__':
    app.run(debug=True)




#{
#    "alien_usuario" : "rem",
#    "alien_nombre" : "Raul",
#    "alien_ap" : "Estrada",
#    "alien_am" : "Mejia",
#    "alien_correo" : "rau1l@upt.com",
#    "alien_contrasenia" : "123",
#    "alien_nac" : "20000814",
#    "alien_status" : "Activo"
#}