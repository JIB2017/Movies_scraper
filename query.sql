CREATE TABLE IF NOT EXISTS peliculas (
    id TEXT PRIMARY KEY,
    titulo TEXT NOT NULL,
    anio INTEGER,
    calificacion NUMERIC,
    duracion INTEGER,
    metascore INTEGER
);

CREATE TABLE IF NOT EXISTS actores (
    id SERIAL PRIMARY KEY,
    pelicula_id TEXT NOT NULL,
    nombre TEXT NOT NULL,
    FOREIGN KEY (pelicula_id) REFERENCES peliculas(id) ON DELETE CASCADE
);
