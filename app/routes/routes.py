from app import app
from ..views import index, authentication

#rodar o scrapper
#sched = BackgroundScheduler(daemon=True)
#sched.add_job(scrapper.main, 'interval', weeks=1)
#sched.start()

@app.route("/", methods=['GET'])
@authentication.token_required
def ExibirRanking():
    return index.ExibirRanking()

@app.route("/ranking/<top>")
@authentication.token_required
def ExibirRankingQuantidadeAtletas(top):
    return index.ExibirRankingQuantidadeAtletas(top)

@app.route("/ranking/ano/<year>")
@authentication.token_required
def RankingPorAno(year):
    return index.RankingPorAno(year)

@app.route("/atleta/<nomeAtleta>")
@authentication.token_required
def ExibirDesempenhoAtleta(nomeAtleta):
    return index.ExibirDesempenhoAtleta(nomeAtleta)

@app.route("/atleta/procurar/<nomeAtleta>")
@authentication.token_required
def ProcurarAtleta(nomeAtleta):
    return index.ProcurarAtleta(nomeAtleta)


@app.route("/ultima-atualizacao")
@authentication.token_required
def UltimaAtualizacaoLeitura():
    return index.ultimaAtualizacaoLeitura()

#autenticacao
@app.route("/authenticate", methods=["POST"])
def authenticate():
    return authentication.auth()

@app.route("/auth", methods=["POST"])
def auth():
    pass


#servidor heroku

#heroku login
#git add .
#git commit -m ""
#git push heroku master