import aiohttp, asyncio, bs4, csv, re, requests

def get_first_page(url, filter_name) -> requests.models.Response:
    return requests.get(
        f"{url}/pesquisaideia?pesquisa={filter_name}",
        headers={'Cache-Control': 'no-cache'}
    ) 

def get_last_page_to_search(first_page) -> int:
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

async def execute(url, last_page, filter_name):
    ideas = {}
    async with aiohttp.ClientSession() as session:

        for page in range(1, last_page+1):
            print(page)
            url = f"{url}/pesquisaideia?p={page}&pesquisa={filter_name}"
            async with session.get(url) as resp:
                data = await resp.text()
                data_parser = bs4.BeautifulSoup(data, 'html.parser')
                proposes = data_parser.find_all("article", {"class":"resumo-ideia"})
                
                for idea in proposes:
                    id = idea.find("a")["href"]
                    async with session.get(f"{url}/{id}") as resp:
                        data_idea = await resp.text()
                        article_parser = bs4.BeautifulSoup(data_idea, 'html.parser')
                        title = article_parser.find_all("div", {"style":"font-size:24px;margin-bottom:15px;"})[0].text
                        first_paragraph = article_parser.find_all("div", {"style": "margin-bottom:15px;"})[0].text
                        second_paragraph = article_parser.find_all("div", {"id": "collapseOne"})[0].text
                        text = first_paragraph + " " + second_paragraph
                        ideas[title] = text                  
    return add_data_in_csv(ideas)


if __name__ == '__main__':
    url = "https://www12.senado.leg.br/ecidadania"
    filter_name = "homofobia"
    first_page = get_first_page(url, filter_name)
    last_page = get_last_page_to_search(first_page)
    asyncio.run(execute(url, last_page, filter_name))
