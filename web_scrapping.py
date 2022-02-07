import csv, bs4, time, re, requests


def get_first_page(url: str, filter: str) -> requests.models.Response:
    return requests.get(f"{url}/pesquisaideia?pesquisa={filter}", headers={'Cache-Control': 'no-cache'}) 

def get_last_page_to_search(url: str, filter: str) -> int:
    first_page = get_first_page(url, filter)
    parser = bs4.BeautifulSoup(first_page.content, 'html.parser')
    pagination = parser.find_all("a", {"class": "page-link", "title": "último"})
    if len(pagination) > 0:
        last_page = int(re.search("p=[0-9]{1,4}", str(pagination)).group(0).replace("p=", ""))
        return last_page
    else:
        return 1

def add_data_in_csv(ideas: dict) -> None:
    with open("dados_legislativo.csv", "w") as csvfile:
        csv_write = csv.writer(csvfile)
        csv_write.writerow(["Ideias", "Texto"])
        for item in ideas:
            csv_write.writerow([item,ideas[item]])
    return

def scrape_data(url: str, filter: str) -> None:
    last_page = get_last_page_to_search(url, filter)
    ideas = {}
    for page in range(1, last_page+1):
        print(f"Página {page} sendo executada")
        data = requests.get(f"{url}/pesquisaideia?p={page}&pesquisa={filter}", headers={'Cache-Control': 'no-cache'})
        data_parser = bs4.BeautifulSoup(data.content, 'html.parser')
        proposes = data_parser.find_all("article", {"class":"resumo-ideia"})
        for idea in proposes:
            id = idea.find("a")["href"]
            data_idea = requests.get(f"{url}/{id}")
            article_parser = bs4.BeautifulSoup(data_idea.content, 'html.parser')
            title = article_parser.find_all("div", {"style":"font-size:24px;margin-bottom:15px;"})[0].text
            first_paragraph = article_parser.find_all("div", {"style": "margin-bottom:15px;"})[0].text
            second_paragraph = article_parser.find_all("div", {"id": "collapseOne"})[0].text
            text = first_paragraph + " " + second_paragraph
            ideas[title] = text
    add_data_in_csv(ideas)
    return


if __name__ == '__main__':
    url = "https://www12.senado.leg.br/ecidadania"
    filter = "+".join(input("Digite o filtro de busca: ").lower().split())
    start_time = time.time()
    ideas = scrape_data(url, filter)
    execution_time = time.time() - start_time
    print(f"Execution time: {execution_time}")
    print("Finished")
