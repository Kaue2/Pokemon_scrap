import scrapy

class PokemonSpider(scrapy.Spider):
    name = "pokemon"
    start_urls = ['https://pokemondb.net/pokedex/all']

    def parse(self, response):
        for row in response.css("table#pokedex > tbody > tr"):
            dex = row.css("td.cell-num > span::text").get()
            name = row.css("td.cell-name > a::text").get()
            link = row.css("td.cell-name > a::attr(href)").get()
            types = row.css("td.cell-icon a::text").getall()
            mega = row.css("td.cell-name > small::text").get()

            data = {
                "dex": dex,
                "nome": name,
                "tipos": types,
                "link": f"https://pokemondb.net{link}"
            }

            if mega:
                data["nome"] = mega

            yield data
