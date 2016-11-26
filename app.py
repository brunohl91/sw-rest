#/usr/bin/python2.4
#

# conexao com postgres
import psycopg2
# servidor rest, modulos principais
from flask import Flask, Response, request
# biblioteca de CORS
from flask_cors import CORS, cross_origin
# biblitoeca para auth
from flask_basicauth import BasicAuth
# json para responses
import simplejson as json

# criacao do app flask e CORS
app = Flask(__name__)
CORS(app)
# configuracao de autenticacao
app.config['BASIC_AUTH_USERNAME'] = 'sw'
app.config['BASIC_AUTH_PASSWORD'] = 'rest'
basic_auth = BasicAuth(app)

# classe para facilitar busca em dicionario
class AttributeDict(dict): 
  __getattr__ = dict.__getitem__
  __setattr__ = dict.__setitem__

# modelo de carro
class Carro:

  id = 0
  nome = ''
  custo = 0.0
  tipo = ''

  def toJson(self):
    return {
      "id": self.id,
      "nome": self.nome,
      "custo": self.custo,
      "tipo": self.tipo
    }

# DAO de carro
class CarroDAO:

  def one(self, db, cursor, idCarro):
    try:
      cursor.execute("SELECT * FROM carro WHERE id = %s", [idCarro])
      data = cursor.fetchone()
      if data:
        carro = Carro()
        carro.id = data[0]
        carro.nome = data[1]
        carro.custo = data[2]
        carro.tipo = data[3]
        return carro.toJson()
      else:
        return {}
    except Exception, e:
      print e

  def all(self, db, cursor):
    try:
      cursor.execute("SELECT * from carro;")
      carros = cursor.fetchall()
      ret = []
      for carro in carros:
        ret.append({
          "id": carro[0],
          "nome": carro[1],
          "custo": carro[2],
          "tipo": carro[3]
        })
      return ret
    except Exception, e:
      print e

  def save(self, db, cursor, carro):
    try:
      if carro.id == 0:
        cursor.execute("INSERT INTO carro (nome, custo, tipo) VALUES (%s, %s, %s);", ( carro.nome, carro.custo, carro.tipo ) )
      else:
        cursor.execute("UPDATE carro SET nome = %s, custo = %s, tipo = %s WHERE id = %s", ( carro.nome, carro.custo, carro.tipo, carro.id ) )
      db.commit()
      print "Registro persistido"
      return True
    except Exception, e:
      print e

  def delete(self, db, cursor, idCarro):
    try:
      cursor.execute("DELETE FROM carro WHERE id = %s;", [idCarro] )
      db.commit()
      print "Registro removido"
      return True
    except Exception, e:
      print e

# Conexao ao Banco
try:
  # DB
  db = psycopg2.connect("dbname='sw-carros' user='postgres' password='1234'")
  cursor = db.cursor()
  print "DB OK"
except:
  print "Nao conseguiu conectar a DB"

# Cria o dao de carro
dao = CarroDAO()

## FETCH ALL
@app.route("/all", methods = ['GET'])
@basic_auth.required
def all():
  js = json.dumps( dao.all(db, cursor) )
  return Response( js , status=200, mimetype='application/json')

## FETCH ONE
@app.route("/get/<carroid>", methods = ['GET'])
@basic_auth.required
def get( carroid ):
  js = json.dumps( dao.one(db, cursor, carroid) )
  return Response( js , status=200, mimetype='application/json')

## CADASTRAR
@app.route("/persist", methods = ['POST'])
@basic_auth.required
def persist():
  carro = Carro()
  carro.nome = request.values['nome']
  carro.custo = request.values['custo']
  carro.tipo = request.values['tipo']
  dao.save(db, cursor, carro)
  return Response( json.dumps( { "msg": "Carro cadastrado" } ) , status=200, mimetype='application/json')

## ALTERAR
@app.route("/update", methods = ['PUT'])
@basic_auth.required
def update():
  carro = Carro()
  carro.id = request.values['id']
  carro.nome = request.values['nome']
  carro.custo = request.values['custo']
  carro.tipo = request.values['tipo']
  dao.save(db, cursor, carro)
  return Response( json.dumps( { "msg": "Carro atualizado" } ) , status=200, mimetype='application/json')

## DELETAR
@app.route("/delete/<carroid>", methods = ['DELETE'])
@basic_auth.required
def delete( carroid ):
  dao.delete(db, cursor, carroid)
  return Response( json.dumps( { "msg": "Carro removido" } ) , status=200, mimetype='application/json')

# Cria o Server e permite acesso externo
if __name__ == "__main__":
  app.run(host= '0.0.0.0')