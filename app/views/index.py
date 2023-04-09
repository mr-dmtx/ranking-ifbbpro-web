from flask import Flask, g, jsonify, make_response
import sqlite3
import config
from flask_cors import CORS
from server import app


CORS(app, resources={r"/*": {"origins": "*"}})
@app.before_request
def before_request():
    print("Conectando ao banco!")
    conn = sqlite3.connect(config.DB_URL)
    g.conn = conn

@app.teardown_request #executado final da requisicao
def after_request(response):
    if g.conn is not None:
        g.conn.close()
        print("Conexão encerrada!")
    return response

def ExibirRanking():
    query = """
        select atleta, round(sum(pontos)) pontos_t from pontuacao p 
        group by atleta
         order by pontos_t desc limit 100;
    """
    cursor = g.conn.execute(query)
    json = [{'nome': row[0], 'pontos': row[1]}
                    for row in cursor.fetchall()]
    return jsonify(json)

def ExibirRankingQuantidadeAtletas(top):
    query = """
        select atleta, sum(pontos) pontos_t from pontuacao p 
        group by atleta
         order by pontos_t desc limit "{}";
    """.format(top)
    cursor = g.conn.execute(query)
    json = [{'nome': row[0], 'pontos': row[1]}
                    for row in cursor.fetchall()]
    return jsonify(json)

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

    return jsonify(json)

def ExibirDesempenhoAtleta(nomeAtleta):
    query = """
            select p.posicao_atleta_nome nome, p.posicao_lugar posicao, c.categoria_nome categoria, SUBSTRING(s.show_data, 0, 5)||" "|| s.show_nome evento from show s 
            inner join categoria c on c.categoria_show = s.show_id 
            inner join posicao p on p.posicao_categoria = c.categoria_id 
            where posicao_atleta_nome like '{}' order by evento desc;
        """.format(nomeAtleta)
    cursor = g.conn.execute(query)
    json = [{'nome': row[0], 'posicao': row[1], 'categoria': row[2], 'evento': row[3]}
            for row in cursor.fetchall()]
    if(len(json) > 0):
        return jsonify(json)
    else:
        json = [{'erro': 'Esse atleta não existe'}]
        return jsonify(json), 404

def ProcurarAtleta(nomeAtleta):
    query = """
            select atleta, 
            round(sum(pontos)) pontos,
            categoria 
            from pontuacao p 
            where atleta like '%{}%' 
            group by atleta order by pontos desc;
        """.format(nomeAtleta)

    cursor = g.conn.execute(query)
    json = [{'nome': row[0], 'pontos': row[1], 'categoria': row[2]}
            for row in cursor.fetchall()]
    return jsonify(json)


def ultimaAtualizacaoLeitura():
    query = """
        select data_atualizacao 
        from atualizacao a 
        order by id_atualizacao desc limit 1;
    """

    cursor = g.conn.execute(query)
    json = [{"data": row[0]} for row in cursor.fetchall()]

    return jsonify(json)


#servidor heroku

#heroku login
#git add .
#git commit -m ""
#git push heroku master