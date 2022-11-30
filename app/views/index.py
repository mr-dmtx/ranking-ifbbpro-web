from flask import Flask, g, jsonify
import sqlite3
import config
from server import app

@app.before_request
def before_request():
    print("Conectando ao banco!")
    conn = sqlite3.connect(config.DB_URL)
    g.conn = conn

@app.teardown_request #executado final da requisicao
def after_request(exception):
    if g.conn is not None:
        g.conn.close()
        print("Conexão encerrada!")

def ExibirRanking():
    query = """
        select atleta, sum(pontos) pontos_t from pontuacao p 
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
            select p.posicao_atleta_nome nome, p.posicao_lugar posicao, c.categoria_nome categoria, s.show_nome evento from show s 
            inner join categoria c on c.categoria_show = s.show_id 
            inner join posicao p on p.posicao_categoria = c.categoria_id 
            where posicao_atleta_nome like '{}';
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
            sum(pontos) pontos,
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