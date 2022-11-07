from flask import Flask, request, Response, g
from flask_cors import CORS
import sqlite3
#from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
import scrapper
from apscheduler.schedulers.background import BackgroundScheduler

#rodar o scrapper
sched = BackgroundScheduler(daemon=True)
sched.add_job(scrapper.main, 'interval', weeks=1)
sched.start()

app = Flask(__name__)
cors = CORS(app)

#app.config['CORS_HEADERS'] = 'Content-Type'
#app.config['JWT_SECRET_KEY'] = "123"
#jwt = JWTManager(app)

#access_token = create_access_token(identity='daniel')


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
#@jwt_required
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

@app.route("/ranking/ano/<year>")
def RankingPorAno(year):

    query = """
        select atleta, 
            sum(pontos) pontos 
            from pontuacao p 
            where p.evento like '{}%' 
            group by atleta order by pontos desc;
    """.format(year)

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
    if(len(json) > 0):
        return json
    else:
        json = [{'erro': 'Esse atleta não existe'}]
        return json, 404
@app.route("/atleta/procurar/<nomeAtleta>")
def ProcurarAtleta(nomeAtleta):
    query = """
            select atleta, 
            sum(pontos) pontos,
            categoria 
            from pontuacao p 
            where atleta like '%{}%' 
            group by atleta order by pontos desc;
        """.format(nomeAtleta)

    cursor = g.conn.execute(query)
    json = [{'nome': row[0], 'pontos': row[1], 'categoria': row[2]}
            for row in cursor.fetchall()]
    return json


@app.route("/ultima-atualizacao")
def ultimaAtualizacaoLeitura():
    query = """
        select data_atualizacao 
        from atualizacao a 
        order by id_atualizacao desc limit 1;
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