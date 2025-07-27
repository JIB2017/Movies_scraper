import scrapy
import json
from IMDB_scraper.items import MovieItem
from scrapy.loader import ItemLoader

class IMDBSpider(scrapy.Spider):
    name = "IMDB"
    start_urls = ["https://www.imdb.com/es-es/chart/top/"]
    # cols = ["titulo", "anio", "calificacion", "duracion", "metascore", "actores"]

    def parse(self,response):
        movies = response.css('script#__NEXT_DATA__::text').get()
        json_movies = json.loads(movies)

        data = json_movies["props"]["pageProps"]["pageData"]["chartTitles"]["edges"]
        # self.log(data[:3])

        for movie in data[:2]:
            
            node = movie["node"]
            id = node["id"]
            details_url = f'https://www.imdb.com/es-es/title/{id}/?ref_=chttp_t_21'
            
            # Este no hace falta
            # cast_url = f'https://www.imdb.com/es-es/title/{id}/fullcredits/?ref_=tt_ov_3#cast' 
            yield scrapy.Request(
                details_url,
                callback=self.parse_details,
                meta={
                    "id": id,
                    "titulo": node["titleText"]["text"],
                    "anio": node["releaseYear"]["year"],
                    "calificacion": node["ratingsSummary"]["aggregateRating"]
                },
                cookies={
                    "ad-oo": "0",
                    "ci": "eyJpc0dkcHIiOmZhbHNlfQ",
                    "csm-hit": "tb:NS16Z7M3KWSXCYN1TYJ8+s-HKQM74A8GMF3BCNZ8X0Q|1753591769822&t:1753591769822&adb:adblk_no",
                    "international-seo": "es-ES",
                    "ubid-main	": "133-8605800-9962600"
                }
            )

            

        # yield loader.load_item()



    def parse_details(self,response):
        script = response.css('script#__NEXT_DATA__::text').get()
        data = json.loads(script)
        data_json = data["props"]["pageProps"]["aboveTheFoldData"]

        metascore = data_json["metacritic"]["metascore"]["score"]
        duration = data_json["runtime"]["displayableProperty"]["value"]["plainText"]
        cast = data["props"]["pageProps"]["mainColumnData"]["cast"]["edges"] # Es un array, tambien tienen un 'node' c/u
        actor_names = [
            actor.get("node", {}).get("name", {}).get("nameText", {}).get("text")
            for actor in cast if actor.get("node")
        ]

        loader = ItemLoader(item=MovieItem(),response=response)

        loader.add_value("id", response.meta["id"])
        loader.add_value("titulo", response.meta["titulo"])
        loader.add_value("anio", response.meta["anio"])
        loader.add_value("calificacion", response.meta["calificacion"])
        loader.add_value("duracion", duration)
        loader.add_value("metascore", metascore)
        loader.add_value("actores", actor_names)

        yield loader.load_item()

