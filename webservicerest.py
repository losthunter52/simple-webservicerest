from flask import Flask, jsonify, make_response, request, abort
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

leituras = []

@app.route('/leituras', methods=['GET'])
def obtem_leituras():
    aux = leituras[-10:-1]
    return jsonify({'leituras': aux})

@app.route('/leituras/data', methods=['POST'])
def obtem_leituras_por_data():
    if not request.json or not 'data' in request.json:
        abort(400)
    data = request.json['data']
    resultado = [resultado for resultado in leituras if data == resultado['leitura_data']]
    return jsonify({'leituras': resultado })

@app.route('/leituras/<int:idLeitura>', methods=['GET'])
def detalhe_leitura(idLeitura):
    resultado = [resultado for resultado in leituras if resultado['id'] == idLeitura]
    if len(resultado) == 0:
        abort(404)
    return jsonify({'leitura': resultado[0]})

@app.route('/leituras/<int:idLeitura>', methods=['DELETE'])
def excluir_leitura(idLeitura):
    resultado = [resultado for resultado in leituras if resultado['id'] == idLeitura]
    if len(resultado) == 0:
        abort(404)
    leituras.remove(resultado[0])
    return jsonify({'resultado': True})

@app.route('/leituras', methods=['POST'])
def criar_leitura():
    if not request.json or not 'temperatura' in request.json:
        abort(400)
    if not request.json or not 'umidade' in request.json:
        abort(400)
    if not request.json or not 'luminosidade' in request.json:
        abort(400)
    if len(leituras) > 0:
        id = leituras[-1]['id'] + 1
    else:
        id = 1
    data = datetime.datetime.now()
    data = str(data.date())
    leitura = {
        'id': id,
        'temperatura': request.json['temperatura'],
        'umidade' : request.json['umidade'],
        'luminosidade' : request.json['luminosidade'],
        'leitura_data' : data
    }
    leituras.append(leitura)
    return jsonify({'leitura': leitura}), 201

@app.route('/leituras/<int:idLeitura>', methods=['PUT'])
def atualizar_leitura(idLeitura):
    resultado = [resultado for resultado in leituras if resultado['id'] == idLeitura]
    if len(resultado) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'temperatura' in request.json and type(request.json['temperatura']) != "<type 'unicode'>":
        abort(400)
    if 'umidade' in request.json and type(request.json['umidade']) != "<type 'unicode'>":
        abort(400)
    if 'luminosidade' in request.json and type(request.json['luminosidade']) != "<type 'unicode'>":
        abort(400)
    resultado[0]['temperatura'] = request.json.get('temperatura', resultado[0]['temperatura'])
    resultado[0]['umidade'] = request.json.get('umidade', resultado[0]['umidade'])
    resultado[0]['luminosidade'] = request.json.get('luminosidade', resultado[0]['luminosidade'])
    resultado[0]['leitura_data'] = datetime.datetime.now()
    return jsonify({'leitura': resultado[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'erro': 'Recurso Nao encontrado'}), 404)


if __name__ == "__main__":
    print('Servidor executando...')
    app.run(debug=True)
