# Movies Scraper

This project started as a technical challenge and I later decided to extended to run as a small, production-style data ingestion pipeline.

The project extract data of top movies from IMDB and then persists the results into PostgreSQL database. I use Docker to containerized the scraper and later on to be executed as a scheduled job in Kubernetes.

My main goal of this project is to build a scraping workflow solution that can be scheduled and monitored in production.

---

At the moment the scraper does the following:

- Crawls the IMDB listing pages to collect the top movies
- Follows links to each movie’s detail page
- Extracts additional attributes such as rating, duration, metascore, and main actors
- Normalizes and stores the data in PostgreSQL


