from os import error
from types import NoneType
from bs4 import BeautifulSoup
import requests
import sqlite3
import datetime

connectionBd = sqlite3.connect("champsifbb.db", check_same_thread=False)


def main():
    for i in range(12):
        urlPageContestYear = "https://contests.npcnewsonline.com/contests/ifbb_{}/index.php".format(2011 + i)
        htmlPageContestYear = requests.get(urlPageContestYear).content
        soupPageContestYear = BeautifulSoup(htmlPageContestYear, 'html.parser')
        linksContests = soupPageContestYear.find("div", class_="contest-listing")

        for j in linksContests.find_all('a', href=True):
            linkContest = j['href']

            urlContest = "https://contests.npcnewsonline.com/" + linkContest[6:]

            cursor = connectionBd.cursor()
            verify = cursor.execute("select show_id from show where show_url like ?", (urlContest,)).fetchall()

            if (len(verify) <= 0):
                getContestsResults(urlContest)

    dataAtualizacao = datetime.datetime.now();
    dataAtualizacaoFormatado = dataAtualizacao.strftime("%d/%m/%Y %H:%M:%S")

    connectionBd.execute("insert into atualizacao (data_atualizacao) values (?)", (dataAtualizacaoFormatado,))
    connectionBd.commit()

    print("Finalizado em ", dataAtualizacaoFormatado)


def getContestsResults(urlContest):
    try:
        htmlSite = requests.get(urlContest).content

        soup = BeautifulSoup(htmlSite, 'html.parser')

        nomeChamp = soup.find("h1", class_="entry-title")
        dateChamp = soup.find("span", class_="entry-date")
        if (type(dateChamp) == NoneType):
            dateChamp = soup.find("div", class_="date")

        table = soup.find('table', attrs={'class': 'contest_table'})
        categorias = table.find_all('td')

        print(nomeChamp.text)
        connectionBd.execute("insert into show (show_nome, show_data, show_url) values (?, ?, ?)",
                             (nomeChamp.text, dateChamp.text, urlContest))
        connectionBd.commit()
        print("Carregando Resultados...")
        for categoria in categorias:
            nomeCategoria = categoria.find('h2', class_="division-title")

            guestPose = categoria.find('div', attrs={'class': 'competitor-class'});

            if (guestPose == None or guestPose.text != 'Guest Poser'):
                atletas = categoria.find_all('a')
                if (nomeCategoria is not None):
                    connectionBd.execute(
                        "insert into categoria (categoria_nome, categoria_show) values (?, (select show_id from show where show_url like ?))",
                        (nomeCategoria.text.title(), urlContest))
                    connectionBd.commit()
                if (len(atletas) > 0):
                    posicao = 1
                    for atleta in atletas:
                        if (len(atleta.text) > 0):
                            if (atleta.text.find("Comparisons") == -1):
                                if (atleta.text.find("Awards") == -1):
                                    connectionBd.execute(
                                        "insert into posicao (posicao_lugar, posicao_categoria, posicao_atleta_nome) values (?, (select c.categoria_id from show s inner join categoria c on c.categoria_show = s.show_id where s.show_url like ? order by c.categoria_id desc), ?)",
                                        (posicao if posicao <= 16 else 16, urlContest, atleta.text.replace("  ", " ")))
                                    connectionBd.commit()
                                    posicao += 1
        print("Finalizado")
    except:
        print("Site invalido", error);
        pass


main()

