# Movies Scraper

This project started as a technical challenge and I later decided to extended to run as a small, production-style data ingestion pipeline.

The project extract data of top movies from IMDB and then save it to a PostgreSQL database. I use Docker to containerized the scraper and later on to be executed as a scheduled job in Kubernetes.

My main goal of this project is to build a scraping workflow solution that can be scheduled and monitored in production.

---

The scraper does the following:

Crawls the top ranked. Follows the links to each movie’s detail page and extracts additional attributes such as rating, duration, metascore, and main actors. Normalizes it and stores the data in PostgreSQL.


