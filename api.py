from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with, marshal
from flaskext.mysql import MySQL
import json

app = Flask(__name__)
api = Api(app)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'fab014'
app.config['MYSQL_DATABASE_DB'] = 'universitat'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

# Cria o objeto para conexão com o banco e o inicia com o objeto app, previamente
# configiurado para conexão com o banco de dados.
mysql = MySQL()
mysql.init_app(app)

# Cria a conexao com o banco de dados.
conn = mysql.connect()

# Cria um cursor para iterar sobre os elementos retornados do banco.
cursor = conn.cursor()

# Cria um parser para tipar os parâmetros de um request.
parser = reqparse.RequestParser()


class Pesquisador(Resource):
    def get(self, id):
        try:
            # Busca todos os pesquisadores cadastrados
            query = "SELECT * FROM universitat.pesquisador where id = %s"

            cursor.execute(query, (id))

            pesquisador = [dict((cursor.description[i][0], value)
                                for i, value in enumerate(row)) for row in cursor.fetchmany(1)]

            if pesquisador is None:
                return "Pesquisador não encontrado", 404
            else:
                return pesquisador

        except Exception as e:
            return {'error': str(e)}

    def delete(self, id):
        try:
            query = "DELETE FROM universitat.pesquisador where id = %s"

            cursor.execute(query, (id))

            conn.commit()

        except Exception as e:
            return {'error': str(e)}

    def put(self, id):
        try:
            parser.add_argument('nome', type=str, help='Nome do pesquisador.')
            parser.add_argument('cpf', type=int, help='CPF do pesquisador.')
            args = parser.parse_args()

            _nome = args['nome']
            _cpf = args['cpf']

            query = "UPDATE `universitat`.`pesquisador` SET `nome` = %s, `cpf` = %s WHERE `id` = %s"

            cursor.execute(query, (_nome, _cpf, id))

            conn.commit()

        except Exception as e:
            return {'error': str(e)}


class PesquisadorList(Resource):
    def get(self):
        try:
            # Busca todos os pesquisadores cadastrados
            query = "SELECT * FROM universitat.pesquisador"

            cursor.execute(query)

            pesquisadores = [dict((cursor.description[i][0], value)
                                  for i, value in enumerate(row)) for row in cursor.fetchall()]

            return pesquisadores, 200

        except Exception as e:
            return {'error': str(e)}

    def post(self):
        try:
            # Parse the arguments
            parser.add_argument('nome', type=str, help='Nome do pesquisador.')
            parser.add_argument('cpf', type=int, help='CPF do pesquisador.')
            args = parser.parse_args()

            _nome = args['nome']
            _cpf = args['cpf']

            # Cria a conexao com o banco de dados.
            conn = mysql.connect()

            # Cria um cursor para iterar sobre os elementos retornados do banco.
            cursor = conn.cursor()

            query = "INSERT INTO `universitat`.`pesquisador` (`nome`,`cpf`) VALUES (%s,%s)"

            cursor.execute(query, (_nome, _cpf))

            conn.commit()

            return "Ok", 200

        except Exception as e:
            return {'error': str(e)}

fields = {
    'id': fields.Integer,
    'titulo': fields.String,
    'tempo_previsto': fields.Integer,
    'data_inicio': fields.DateTime(dt_format='iso8601'),
    'data_conclusao': fields.DateTime(dt_format='iso8601'),
    'status': fields.String
}

class ProjetoPesquisa(Resource):
    @marshal_with(fields, envelope=None)
    def get(self, id, **kwargs):
        try:
            # query = "SELECT * FROM universitat.projeto_pesquisa where id = %s"
            query = "SELECT p.*, s.status FROM universitat.projeto_pesquisa p, universitat.status_pesquisa s " \
                    "where p.status_pesquisa_id = s.id and p.id = %s"

            cursor.execute(query, (id))

            projeto = [dict((cursor.description[i][0], value)
                                for i, value in enumerate(row)) for row in cursor.fetchmany(1)]

            if projeto is None:
                return "Projeto não encontrado", 404
            else:
                return projeto, 200

        except Exception as e:
            return {'error': str(e)}

    def delete(self, id):
        try:
            query = "DELETE FROM universitat.projeto_pesquisa where id = %s"

            cursor.execute(query, (id))

            conn.commit()

        except Exception as e:
            return {'error': str(e)}

    def put(self, id):
        try:
            parser.add_argument('titulo', type=str)
            parser.add_argument('tempo_previsto', type=int)
            parser.add_argument('data_inicio', type=str)
            parser.add_argument('data_conclusao', type=str)
            parser.add_argument('status', type=int)

            args = parser.parse_args()

            _titulo = args['titulo']
            _tempo_previsto = args['tempo_previsto']
            _data_inicio = args['data_inicio']
            _data_conclusao = args['data_conclusao']
            _status = args['status']

            # Busca todos os pesquisadores cadastrados
            query = "UPDATE `universitat`.`projeto_pesquisa` SET `titulo` = %s, `tempo_previsto` = %s, `data_inicio` = %s, `data_conclusao` = %s, `status_pesquisa_id` = %s WHERE `id` = %s"

            cursor.execute(query, (_titulo, _tempo_previsto, _data_inicio, _data_conclusao, _status, id))

            conn.commit()

        except Exception as e:
            return {'error': str(e)}


class ProjetoPesquisaList(Resource):
    @marshal_with(fields, envelope=None)
    def get(self):
        try:
            # Busca todos os pesquisadores cadastrados
            query = "SELECT p.*, s.status FROM universitat.projeto_pesquisa p, universitat.status_pesquisa s " \
                    "where p.status_pesquisa_id = s.id"

            cursor.execute(query)

            projetos = [dict((cursor.description[i][0], value)
                                  for i, value in enumerate(row)) for row in cursor.fetchall()]

            return projetos, 200

        except Exception as e:
            return {'error': str(e)}

    def post(self):
        try:
            parser.add_argument('titulo', type=str)
            parser.add_argument('tempo_previsto', type=int)
            parser.add_argument('data_inicio', type=str)
            parser.add_argument('data_conclusao', type=str)
            parser.add_argument('status', type=int)

            args = parser.parse_args()

            _titulo = args['titulo']
            _tempo_previsto = args['tempo_previsto']
            _data_inicio = args['data_inicio']
            _data_conclusao = args['data_conclusao']
            _status = args['status']

            # Cria a conexao com o banco de dados.
            conn = mysql.connect()

            # Cria um cursor para iterar sobre os elementos retornados do banco.
            cursor = conn.cursor()

            query = "INSERT INTO `universitat`.`projeto_pesquisa` (`titulo`,`tempo_previsto`,`data_inicio`,`data_conclusao`,`status_pesquisa_id`) VALUES (%s,%s,%s,%s,%s)"

            cursor.execute(query, (_titulo, _tempo_previsto, _data_inicio, _data_conclusao, _status))

            conn.commit()

            return "Ok", 200

        except Exception as e:
            return {'error': str(e)}


api.add_resource(Pesquisador, '/pesquisadores/<id>')
api.add_resource(PesquisadorList, '/pesquisadores')
api.add_resource(ProjetoPesquisa, '/projetospesquisa/<id>')
api.add_resource(ProjetoPesquisaList, '/projetospesquisa')


if __name__ == '__main__':
    app.run(debug=True)
