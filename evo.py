import scrapy

def get_evolution(div, pokemon_name) -> list[str]: 
        evolution_names = []
        evolution_datas = []
        evolutions = []
        for num_child in range(1, 16):

            child = div.xpath(f"./*[{num_child}]")
            child = child[0] if child else None

            if child != None:                 
                if child.root.tag == "div":
                    classes = child.attrib.get("class", "").split()

                    if "infocard" in classes:
                        name = child.css("span:nth-child(2) > a::text").get()    
                        
                        if name.lower() != pokemon_name:                
                            evolution_names.append(name)
                        #evolutions.append(name)
                    
                elif child.root.tag == "span": 
                    classes = child.attrib.get("class", "").split()

                    if "infocard-arrow" in classes:
                        small = child.css("small")
                        texto = small.xpath('string(.)').get().strip()
                        link = child.css("small > a::attr(href)").get()
                        if link != None:
                            data = { "texto": texto, "link": f"https://pokemondb.net{link}" }
                            #evolutions.append(data)
                            evolution_datas.append(data)

                        else:
                            #evolutions.append({ "texto": texto, "link": "" })
                            evolution_datas.append({ "texto": texto, "link": "" })

                    elif "infocard-evo-split" in classes:
                        divs = child.css("div.infocard-list-evo")
                        for div in divs: 
                            evolutions.extend(get_evolution(div, pokemon_name))
            else:
                if evolution_names:
                    
                    merged_evolutions = []
                    
                    for name, data in zip(evolution_names, evolution_datas):
                        merged_evolutions.append({
                            "nome": name,
                            "texto": data["texto"],
                            "link": data["link"]                            
                        })                        
                    
                    return merged_evolutions
                return []

class PokemonSpider(scrapy.Spider):
    name = "evo"
    start_urls = [f'https://pokemondb.net/pokedex/eevee']

    def parse(self, response):
        
        pokemon = "eevee"
        
        """
        Evolução Linear funcionando
        """
        evolutions = []

        div_pai = response.css("div.infocard-list-evo")
        for div in div_pai: 
            classes = div.attrib.get("class", "").split()
            if "infocard-list-evo" in classes:
                evolutions.extend(get_evolution(div, pokemon))

        for evo in evolutions:
            yield evo