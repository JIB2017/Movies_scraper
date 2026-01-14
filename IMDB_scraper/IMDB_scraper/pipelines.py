# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
import logging


class ImdbScraperPipeline:
    def process_item(self, item, spider):
        return item


class PostgresPipeline:
    def __init__(self, db_settings):
        self.db_settings = db_settings
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_settings = {
                'host': crawler.settings.get("POSTGRES_HOST"),
                'dbname': crawler.settings.get("POSTGRES_DB"),
                'user': crawler.settings.get("POSTGRES_USER"),
                'password': crawler.settings.get("POSTGRES_PASSWORD"),
                'port': crawler.settings.get("POSTGRES_PORT", 5432),
            }
        )
    
    def open_spider(self, spider):
        self.conn = psycopg2.connect(self.db_settings)
        self.cur = self.conn.cursor()
    
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
    
    def process_item(self, item, spider):
        query = """
            INSERT INTO peliculas (id, titulo, anio, calificacion, duracion, metascore, actores)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """,
        values = (
            item.get("id"),
            item.get("titulo"),
            item.get("anio"),
            item.get("calificacion"),
            item.get("duracion"),
            item.get("metascore"),
            item.get("actores"),
        )

        try:
            self.cur.execute(query, values)
        except Exception as e:
            logging.error(f"Failed to save to database: {e}")
        
        return item