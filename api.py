from flask import Flask
from flask_restful import Resource, Api, reqparse
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

class CreatePesquisador(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
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

            query = "INSERT INTO `universitat`.`pesquisador` (`id`,`nome`,`cpf`) VALUES (%s,%s,%s);"

            cursor.execute(query, (_id, _nome, _cpf))

            conn.commit()

            return "Ok", 200

        except Exception as e:
            return {'error': str(e)}


api.add_resource(CreatePesquisador, '/CreatePesquisador')

if __name__ == '__main__':
    app.run(debug=True)
