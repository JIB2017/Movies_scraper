import scrapy
import json
from IMDB_scraper.items import MovieItem
from scrapy.loader import ItemLoader

class IMDBSpider(scrapy.Spider):
    name = "IMDB"
    start_urls = ["https://www.imdb.com/chart/top/"]

    def parse(self,response):
        # Script with a JSON object with some the information needed
        try:
            movies = response.css('script#__NEXT_DATA__::text').get()
            json_movies = json.loads(movies)
        except Exception as e:
            self.logger.warning(f'Failed to obtain JSON at {response.url}: {e}')


        data = json_movies["props"]["pageProps"]["pageData"]["chartTitles"]["edges"]
        data = json_movies.get("props", {}).get("pageProps", {}).get("pageData", {}).get("chartTitles", {}).get("edges", {})

        if (data):
            for movie in data:
                
                node = movie["node"]
                id = node["id"]
                # Url of detail page
                details_url = f'https://www.imdb.com/es-es/title/{id}/?ref_=chttp_t_21'
                
                # Request with: movie url, callback for parse, meta with data obtained in current page and cookies
                yield scrapy.Request(
                    details_url,
                    callback=self.parse_details,
                    meta={
                        "id": id,
                        "titulo": node["titleText"]["text"],
                        "anio": node["releaseYear"]["year"],
                        "calificacion": node["ratingsSummary"]["aggregateRating"]
                    }
                )



    def parse_details(self,response):
        # Script with a JSON object with the rest of the information needed
        try:
            script = response.css('script#__NEXT_DATA__::text').get()
            data = json.loads(script)
        except Exception as e:
            self.logger.warning(f'Failed to obtain JSON script in {response.url}: {e}')
        
        data_json = data.get("props", {}).get("pageProps", {}).get("aboveTheFoldData", {})

        if data_json:
            metascore = None
            metacritic = data_json.get("metacritic",{})
            if (metacritic and metacritic.get("metascore",{})):
                metascore = metacritic.get("metascore",{}).get("score",{})
            duration = data_json.get("runtime",{}).get("displayableProperty",{}).get("value",{}).get("plainText",{})
            cast = data["props"]["pageProps"]["mainColumnData"]["cast"]["edges"]
            cast = data.get("props",{}).get("pageProps",{}).get("mainColumnData",{}).get("cast",{}).get("edges",{})
            actor_names = [
                actor.get("node", {}).get("name", {}).get("nameText", {}).get("text")
                for actor in cast if actor.get("node")
            ]

            # Item Loaders
            loader = ItemLoader(item=MovieItem(),response=response)

            loader.add_value("id", response.meta["id"])
            loader.add_value("titulo", response.meta["titulo"])
            loader.add_value("anio", response.meta["anio"])
            loader.add_value("calificacion", response.meta["calificacion"])
            loader.add_value("duracion", duration)
            loader.add_value("metascore", metascore)
            loader.add_value("actores", actor_names)

            yield loader.load_item()

