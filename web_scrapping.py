import csv, bs4, time, re, requests


class ScrapeData:
    def __init__(self, url: str, filter_name: str) -> None:
        self.url = url
        self.filter_name = filter_name
        return

    def get_first_page(self) -> requests.models.Response:
        return requests.get(f"{self.url}/pesquisaideia?pesquisa={self.filter_name}", headers={'Cache-Control': 'no-cache'}) 

    def get_last_page_to_search(self) -> int:
        first_page = self.get_first_page()
        parser = bs4.BeautifulSoup(first_page.content, 'html.parser')
        pagination = parser.find_all("a", {"class": "page-link", "title": "último"})
        if len(pagination) > 0:
            last_page = int(re.search("p=[0-9]{1,4}", str(pagination)).group(0).replace("p=", ""))
            return last_page
        else:
            return 1

    def add_data_in_csv(self, ideas: dict) -> None:
        with open("dados_legislativo.csv", "w") as csvfile:
            csv_write = csv.writer(csvfile)
            csv_write.writerow(["Ideias", "Texto"])
            for item in ideas:
                csv_write.writerow([item,ideas[item]])
        return

    def execute(self) -> None:
        last_page = self.get_last_page_to_search()
        ideas = {}
        for page in range(1, last_page+1):
            print(f"Página {page} sendo executada")
            data = requests.get(f"{self.url}/pesquisaideia?p={page}&pesquisa={self.filter_name}", headers={'Cache-Control': 'no-cache'})
            data_parser = bs4.BeautifulSoup(data.content, 'html.parser')
            proposes = data_parser.find_all("article", {"class":"resumo-ideia"})
            for idea in proposes:
                id = idea.find("a")["href"]
                data_idea = requests.get(f"{self.url}/{id}")
                article_parser = bs4.BeautifulSoup(data_idea.content, 'html.parser')
                title = article_parser.find_all("div", {"style":"font-size:24px;margin-bottom:15px;"})[0].text
                first_paragraph = article_parser.find_all("div", {"style": "margin-bottom:15px;"})[0].text
                second_paragraph = article_parser.find_all("div", {"id": "collapseOne"})[0].text
                text = first_paragraph + " " + second_paragraph
                ideas[title] = text
        self.add_data_in_csv(ideas)
        return


if __name__ == '__main__':
    url = "https://www12.senado.leg.br/ecidadania"
    filter = "+".join(input("Digite o filtro de busca: ").lower().split())
    start_time = time.time()
    ScrapeData(url, filter).execute()
    execution_time = time.time() - start_time
    print(f"Execution time: {execution_time}")
    print("Finished")
