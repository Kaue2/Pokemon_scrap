import scrapy


def get_evolution(div) -> list[str]: 
        evolutions = []
        for num_child in range(1, 16):

            child = div.xpath(f"./*[{num_child}]")
            child = child[0] if child else None

            if child != None: 
                if child.root.tag == "div":
                    classes = child.attrib.get("class", "").split()

                    if "infocard" in classes:
                        name = child.css("span:nth-child(2) > a::text").get()
                        evolutions.append(name)
                    
                elif child.root.tag == "span": 
                    classes = child.attrib.get("class", "").split()

                    if "infocard-arrow" in classes:
                        small = child.css("small")
                        texto = small.xpath('string(.)').get().strip()
                        link = child.css("small > a::text").get()
                        if link != None:
                            print(link)
                        
                        evolutions.append(texto)

                    elif "infocard-evo-split" in classes:
                        divs = child.css("div.infocard-list-evo")
                        for div in divs: 
                            evolutions.extend(get_evolution(div))
            else:
                if evolutions:
                    return evolutions
                return

class PokemonSpider(scrapy.Spider):
    name = "evo"
    start_urls = ['https://pokemondb.net/pokedex/eevee']

    def parse(self, response):
        """
        Evolução Linear funcionando
        """
        evolutions = []

        div_pai = response.css("div.infocard-list-evo")
        for div in div_pai: 
            classes = div.attrib.get("class", "").split()
            if "infocard-list-evo" in classes:
                evolutions = get_evolution(div)

        for evo in evolutions:
            print(evo)
