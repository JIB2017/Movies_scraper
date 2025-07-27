# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from itemloaders.processors import MapCompose, TakeFirst, Join
import re


def clean_duration(duration):
    match = re.search(r'(\d+)h\s*(\d+)?',duration)
    if match:
        hours = int(match.group(1))
        minutes = int(match.group(2) or 0)
        return hours * 60 + minutes


class MovieItem(Item):

    id = Field(
        output_processor=TakeFirst()
    )
    titulo = Field(
        output_processor=TakeFirst()
    )
    anio = Field(
        output_processor=TakeFirst()
    )
    calificacion = Field(
        output_processor=TakeFirst()
    )
    duracion = Field(
        input_processor=MapCompose(clean_duration),
        output_processor=TakeFirst()
    )
    metascore = Field(
        output_processor=TakeFirst()
    )
    actores = Field(
        output_processor=Join(", ")
    )
