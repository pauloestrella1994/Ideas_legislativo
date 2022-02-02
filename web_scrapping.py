import csv, time, re, requests
from bs4 import BeautifulSoup

url = "https://www12.senado.leg.br/ecidadania"
filter = "ideologia+de+gênero"
first_page = requests.get(f"{url}/pesquisaideia?pesquisa={filter}", headers={'Cache-Control': 'no-cache'})

parser = BeautifulSoup(first_page.content, 'html.parser')
pagination = parser.find_all("a", {"class": "page-link", "title": "último"})
if pagination != []:
    last_page = int(re.search("p=[0-9]{1,4}", pagination).group(0).replace("p=", ""))
else:
    last_page = 1

ideas = {}
start_time = time.time()
for page in range(1, last_page+1):
    print(f"Página {page} sendo executada")
    data = requests.get(f"{url}/pesquisaideia?p={page}&pesquisa={filter}", headers={'Cache-Control': 'no-cache'})
    data_parser = BeautifulSoup(data.content, 'html.parser')
    proposes = data_parser.find_all("article", {"class":"resumo-ideia"})
    for idea in proposes:
        id = idea.find("a")["href"]
        data_idea = requests.get(f"{url}/{id}")
        article_parser = BeautifulSoup(data_idea.content, 'html.parser')
        title = article_parser.find_all("div", {"style":"font-size:24px;margin-bottom:15px;"})[0].text
        first_paragraph = article_parser.find_all("div", {"style": "margin-bottom:15px;"})[0].text
        second_paragraph = article_parser.find_all("div", {"id": "collapseOne"})[0].text
        text = first_paragraph + " " + second_paragraph
        ideas[title] = text

with open("dados_legislativo.csv", "w") as csvfile:
    csv_write = csv.writer(csvfile)
    csv_write.writerow(["Ideias", "Texto"])
    for item in ideas:
        csv_write.writerow([item,ideas[item]])

execution_time = time.time() - start_time
print(f"Execution time: {execution_time}")
print("finished")
