from flask import Flask, request, redirect, url_for
from flask import render_template
import redis

def connect_db():
    conexion = redis.StrictRedis(host='127.0.0.1',port=6379,db=0,charset="utf-8", decode_responses=True)
    if (conexion.ping()):
        print ('conectado al servidor de redis')
    else:
        print ('error..')
    return conexion

db = connect_db()

def inicializar():
    db.geoadd('Cervecerias',-58.232675,-32.481966,'Ambar',-58.248284,-32.477277,'Lagash')
    db.geoadd('Universidades',-58.233333,-32.479041,'UADER FCyT',-58.229595,-32.495807,'UTN FRCU')
    db.geoadd('Farmacias',-58.232973,-32.486202,'Alberdi',-58.230944,-32.486648,'Suarez')
    db.geoadd('Emergencias',-58.236672,-32.484159,'Emergencias Cardiomedicas',-58.229500,-32.490082,'Urgencias Odontologicas')
    db.geoadd('Supermercados',-58.241763,-32.488522,'Dia',-58.230231,-32.489241,'Gran Rex')

def limpiar():
    db.flushdb()

app = Flask (__name__)

@app.route('/')
def index():
    #limpiar()
    #inicializar()
    grupos = db.keys('*')
    return render_template ('/index.html',grupos = grupos)

@app.route('/listado',methods=['GET'])
def listado():
    lista_final = []
    grupo = request.args.get ('grupo')
    lista = db.zrange(grupo,0,-1)
    for el in lista:
        long,lat = db.geopos(grupo,el)[0]
        lista_final.append({"nombre":el,"long":long,"lat":lat})
    return render_template ('/listado.html',lista = lista_final, grupo = grupo)

@app.route('/agregar',methods=['GET'])
def alquilar():
    grupo = request.args.get('grupo')
    nombre = request.args.get('nombre')
    lat = request.args.get('lat')
    long = request.args.get('long')
    db.geoadd (grupo,long,lat,nombre)
    return redirect(url_for('listado', grupo=grupo))

@app.route('/radio',methods=['GET'])
def radio():
    lista_final = []
    grupo = request.args.get ('grupo')
    long = request.args.get ('long')
    lat = request.args.get ('lat')
    lista = db.georadius(grupo,long,lat,5,unit='km',withdist=True)
    return render_template ('/radio.html',lista = lista, grupo = grupo)

if __name__ == '__main__':
    app.run(host='localhost',port='5000', debug=False)

