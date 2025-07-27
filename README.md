# IMDB Scraper - Challenge

Este scraper utiliza **Scrapy** para extraer información de las 250 películas mejor valoradas en IMDB. El objetivo es obtener los datos disponibles en el listado e información que esté disponible en la página de detalle de cada película.

## Instrucciones 
Para correr el spider primero preparamos el un entorno virtual:
```text
  python -m venv .venv
  source .venv/bin/activate # Linux
  .venv\Scripts\activat # Windows
  ```
Instalamos las dependencias: 
```text
  pip install scrapy scrapy-rotating-proxies 
  ```
En la carpeta del spider lo ejecutamos:
```text
  cd ./IMDB_scraper/
  scrapy crawl imdb 
  ```

## ¿Cómo funciona?

Se realiza un **fetch a la URL principal** del ranking de películas.
A partir del JSON embebido en la página (`#__NEXT_DATA__`), se extraen los datos base de cada película (título, año, rating, etc.).
Luego, por cada película, se hace una segunda petición a la página de detalle para obtener mas información (metascore, duracion, actores)


## Diseño del scraper

Item Loaders para la instanciación de cada ítem.
Manejo de errores con `try-except` y validación de campos.
Headers y cookies personalizadas en cada request.
Rotación de IPs usando proxies públicos.
Retry con backoff exponencial hasta 5 veces por petición.


## Manejo de errores

Si no se encuentra el script JSON en la página, se genera un log con un warning.
Si un campo como metascore no existe o es null, simplemente se ignora sin lanzar excepción.
Se implementa una lógica de backoff exponencial. Un delay con un mínimo de 2 segundos y un máximo de 20 segundos, para simular un comportamiento humano y evitar bloqueos.


## Rotación de Proxies

Se usaron alrededor de 20 proxies públicos extraídos de fuentes abiertas.
Los proxies fallidos se loguean con su IP y número de intento.
Si un proxy falla, se reintenta con otro.
Ejemplo de log con rotación de IPs y fallos:
  



## Salida del scraper

Se genera un archivo `output.csv` con los siguientes campos:
`id`, `titulo`, `anio`, `calificacion`, `duracion`, `metascore`, `actores`.

Los actores se listan como una cadena separada por comas.
Tambien está presente el archivo `query.sql` con las queries para la creación de las tablas.
Dentro de la carpeta del scraper se encuentra el `requirements.txt`.

---

## Comparación Técnica: Selenium o Playwright

Estas herramientas headless browser se suelen usar cuando los datos que se buscan extraer se populan dinámicamente mediante javascript (contenido dinámico). Por lo tanto no es posible encontrarlo en el HTML al hacer un fetch con Scrapy o con Request. O si tampoco es en el sitio web hay presente una API con los datos.
En estos casos lo mejor es usar un headless browser como Playwright o Selenium.

Tambien pueden ser útiles cuando existe algun antibot sofisticado (como Cloudflare, Datadome o PerimeterX) que busque detectar la presencia de un browser legítimo.

O cuando la información está disponible solamente despues de realizar clics, entonces estas herramientos son las mas útiles.

Con estas herramientas se pueden usar un `sleep` o un `await` para esperar que el antibot nos deje pasar y tambien para esperar que se renderize el contenido.

Se puede instalar plugins como Stealth para evitar la detección de un headless en Selenium y evitar bloqueos.

Siempre agregar `headers` y `cookies` para simular ser una persona real y no un bot.

Las deventajas de usar estas herramientas es que son mas difíciles de escalar en cuanto a eficiencia y rendimiento: 
 - Consumen mas recursos de hardware.
 - Son mas lentos.
 
 En cambio Scrapy consume menos recursos y es mas rápido.