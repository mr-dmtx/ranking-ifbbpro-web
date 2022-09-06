from flask import Flask, request, Response, g
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

DB_URL = "champsifbb.db"
@app.before_request
def before_request():
    print("Conectando ao banco!")
    conn = sqlite3.connect(DB_URL)
    g.conn = conn

@app.teardown_request #executado final da requisicao
def after_request(exception):
    if g.conn is not None:
        g.conn.close()
        print("Conexão encerrada!")

@app.route("/")
def ExibirRanking():
    query = """
        select atleta, sum(pontos) pontos_t from pontuacao p 
        group by atleta
         order by pontos_t desc limit 100;
    """
    cursor = g.conn.execute(query)
    json = [{'nome': row[0], 'pontos': row[1]}
                    for row in cursor.fetchall()]
    return json

@app.route("/ranking/<top>")
def ExibirRankingQuantidadeAtletas(top):
    query = """
        select atleta, sum(pontos) pontos_t from pontuacao p 
        group by atleta
         order by pontos_t desc limit "{}";
    """.format(top)
    cursor = g.conn.execute(query)
    json = [{'nome': row[0], 'pontos': row[1]}
                    for row in cursor.fetchall()]
    return json

@app.route("/atleta/<nomeAtleta>")
def ExibirDesempenhoAtleta(nomeAtleta):
    query = """
            select p.posicao_atleta_nome nome, p.posicao_lugar posicao, c.categoria_nome categoria, s.show_nome evento from show s 
            inner join categoria c on c.categoria_show = s.show_id 
            inner join posicao p on p.posicao_categoria = c.categoria_id 
            where posicao_atleta_nome like '{}';
        """.format(nomeAtleta)
    cursor = g.conn.execute(query)
    json = [{'nome': row[0], 'posicao': row[1], 'categoria': row[2], 'evento': row[3]}
            for row in cursor.fetchall()]
    return json

@app.route("/ultima-atualizacao")
def ultimaAtualizacaoLeitura():
    query = """
        select data_atualizacao 
        from atualizacao a 
        order by data_atualizacao desc limit 1;
    """

    cursor = g.conn.execute(query)
    json = [{"data": row[0]} for row in cursor.fetchall()]

    return json

if __name__ == "__main__":
    app.run(debug=True)

#servidor heroku

#heroku login
#git add .
#git commit -m ""
#git push heroku master