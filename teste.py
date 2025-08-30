import scrapy

class PokemonSpider(scrapy.Spider):
    name = "teste"
    start_urls = ['https://pokemondb.net/pokedex/pichu']

    def parse(self, response):
        types = []
        # seleciona todas as tabelas de tipo
        altura = response.css("table.vitals-table > tbody > tr:nth-child(4) > td::text").get()
        peso = response.css("table.vitals-table > tbody > tr:nth-child(5) > td::text").get()
        habilidade_texto = response.css("table.vitals-table > tbody > tr:nth-child(6) > td > span > a::text").get()
        habilidade_link = response.css("table.vitals-table > tbody > tr:nth-child(6) > td > span > a::attr(href)").get()
        hidden_text = response.css("table.vitals-table > tbody > tr:nth-child(6) > td > small > a::text").get()
        hidden_link = response.css("table.vitals-table > tbody > tr:nth-child(6) > td > small > a::attr(href)").get()

        hability = {
                "name": habilidade_texto,
                "link": habilidade_link
        }

        hidden = {
            "name": hidden_text,
            "link": hidden_link
        }

        data = { 
            "height": altura,
            "Weight": peso,
            "hability": hability,
            "hidden": hidden
        }

        yield data

       