from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
from flaskext.mysql import MySQL

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
            # Busca todos os pesquisadores cadastrados
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

            # Busca todos os pesquisadores cadastrados
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
            parser.add_argument('id', type=int, help='ID do pesquisador.')
            parser.add_argument('nome', type=str, help='Nome do pesquisador.')
            parser.add_argument('cpf', type=int, help='CPF do pesquisador.')
            args = parser.parse_args()

            _id = args['id']
            _nome = args['nome']
            _cpf = args['cpf']

            # Cria a conexao com o banco de dados.
            conn = mysql.connect()

            # Cria um cursor para iterar sobre os elementos retornados do banco.
            cursor = conn.cursor()

            query = "INSERT INTO `universitat`.`pesquisador` (`id`,`nome`,`cpf`) VALUES (%s,%s,%s)"

            cursor.execute(query, (_id, _nome, _cpf))

            conn.commit()

            return "Ok", 200

        except Exception as e:
            return {'error': str(e)}


api.add_resource(Pesquisador, '/pesquisadores/<id>')
api.add_resource(PesquisadorList, '/pesquisadores')

if __name__ == '__main__':
    app.run(debug=True)
