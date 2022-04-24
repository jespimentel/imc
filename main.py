import sqlite3
from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

def gera_log(nome, imc, classificacao, req):
    utc_time = str(datetime.utcnow()) + ' (UTC)'
    remote = req.remote_addr
    user_agent = req.user_agent.string
    conn = sqlite3.connect('logs.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO logs (data_hora, nome, imc, classificacao, ip, navegador) VALUES (?, ?, ?, ?, ?, ?);', 
    (utc_time, nome, imc, classificacao, remote, user_agent))
    conn.commit()
    conn.close()

def classifica_imc(imc):
    if imc < 18.5:
        return 'Peso baixo'
    elif imc >= 18.5 and imc <= 24.9:
        return 'Peso normal ou adequado'  
    elif imc > 24.9 and imc <= 29.9:
        return 'Sobrepeso'  
    elif imc > 29.9 and imc <= 34.9:
        return 'Obesidade de Grau I'
    elif imc > 34.9 and imc <= 39.9:
        return 'Obesidade de Grau II'
    else:
        return 'Obesidade de Grau III (ou Mórbida)'
    
@app.route('/')
def home():
    return render_template('1.html', 
                            the_title='Prof. Pimentel', 
                            destaque='Palestra na FACAMP - 2022')

@app.route('/imc', methods=['POST'])
def imc():
    nome = request.form['nome']
    peso = request.form['peso']
    altura = request.form['altura']
    imc = round(float(peso)/(float(altura)/100)**2, 2)
    classificacao = classifica_imc(imc)
    gera_log(nome, imc, classificacao, request)
    return render_template('2.html', 
                            the_title = 'Prof. Pimentel', 
                            destaque = 'IMC calculado', 
                            o_nome = nome,
                            o_peso = peso, 
                            a_altura = altura, 
                            o_imc = imc,
                            a_classificacao = classificacao
                            )

@app.route('/logs')
def logs():
    conn = sqlite3.connect('logs.db')
    logs = conn.execute('SELECT * FROM logs ORDER BY id DESC LIMIT 10').fetchall()
    conn.close()
    return render_template('logs.html', 
                            the_title = 'Prof. Pimentel', 
                            destaque = 'Últimos logs da aplicação', 
                            logs=logs)

app.run(debug=True)