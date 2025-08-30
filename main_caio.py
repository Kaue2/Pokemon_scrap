import scrapy
import re

## to load  --->   scrapy runspider nome_do_arquivo.py -O x.csv

class PokeSpider(scrapy.Spider):
    name = 'pokespider'
    start_urls = ['https://pokemondb.net/pokedex/all']
    
    def parse(self, response):
        lines = response.css('table#pokedex > tbody > tr')
        for line in lines:
            id = int(line.css('td:first-child > span::text').get())
            name = line.css('td:nth-child(2) > a::text').get()
            link = line.css('td:nth-child(2) > a::attr(href)').get()

            yield response.follow(link, self.parse_pokemon, meta={"id": id, "name": name, "url": link})

    def parse_pokemon(self, response):
        meta = response.meta.copy()

        height = None
        weight = None
        types = None
        
        rows = response.css('table.vitals-table > tbody > tr')

        for row in rows:
            header = (row.css('th::text').get() or '').strip()
            if header == "Height":
                height = row.css('td::text').get()
                match = re.search(r'(\d+\.\d+)\sm', height)
                height = match.group(0)
                height = float(height[:-2]) * 100
            elif header == "Weight":
                weight = row.css('td::text').get()
                match = re.search(r'(\d+\.\d+)\skg', weight)
                weight = match.group(0)
            elif header == "Type":
                types = row.css('td a::text').getall()

        rows = response.css('div.infocard-list-evo > .infocard')

        i, j = (-1,-1)
        levels = []
        items = []
        evolutions = []

        for row in rows:
            level = (row.css('span.infocard-arrow > small::text').get() or '').strip()
            if level.__contains__('Level'):
                match = re.search(r'\d+', level)
                levels.append(match.group(0))
                i += 1
            elif level.__contains__("use"):
                item = row.css('span.infocard-arrow > small > a::text').get()
                items.append(item)
                j += 1

            evolution_data = row.css('div.infocard > span.infocard-lg-data') or ''

            if evolution_data != '':
                evolution = {}
                evolution['id'] = (evolution_data.css('small::text').get())[1:]
                evolution['name'] = evolution_data.css('a::text').get()
                evolution['url'] = evolution_data.css('a::attr(href)').get()
                if i > -1:
                    evolution['level'] = levels[i]
                    levels.pop(i)
                    i = -1

                if j > -1:
                    evolution['item'] = items[j]
                    items.pop(j)
                    j = -1

                if any(obj['id'] == evolution['id'] for obj in evolutions):
                    print("")
                else:
                    evolutions.append(evolution)
        
        tables = response.css('table.type-table-pokedex')
        
        types_defenses = []
        
        for table in tables:
            trs = table.css('tr')
            ths_types = trs[0].css('th a::attr(title)').getall()
            ths_num = trs[1].css('td')
            
            for i in range(len(ths_types)):
                type = ths_types[i]
                defense = ths_num[i].css('::text').get()
                if defense is None:
                    defense = 1
                
                type_defense = {
                    "type_against": type,
                    "defense": defense
                }
                types_defenses.append(type_defense)

        yield {
            "id" : meta["id"],
            "url": meta["url"],
            "name": meta["name"],
            "evolutions": evolutions,           
            "altura": f"{height:.1f} cm",
            "peso": weight,
            "types": ", ".join(types or []) if len(types) > 1 else types,
            "types_defenses": types_defenses
        }
        