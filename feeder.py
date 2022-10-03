import random, time, requests

while(True):
    temperatura = 20 + random.randint(-8, 8)
    luminosidade = 10 + random.randint(-10, 69)
    umidade = 70 + random.randint(-29, 29)
    url = 'http://127.0.0.1:5000/leituras'
    leitura = {
            'temperatura': temperatura,
            'luminosidade': luminosidade,
            'umidade': umidade,   
            }
    x = requests.post(url, json = leitura)
    print(x.text)
    time.sleep(10)
