CREATE TABLE IF NOT EXISTS peliculas (
    id TEXT PRIMARY KEY,
    titulo TEXT NOT NULL,
    anio INTEGER,
    calificacion NUMERIC,
    duracion INTEGER,
    metascore INTEGER
);