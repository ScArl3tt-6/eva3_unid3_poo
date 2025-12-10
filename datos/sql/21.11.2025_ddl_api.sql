CREATE TABLE IF NOT EXISTS api_productos(
    id INTEGER AUTO_INCREMENT,
    api_id INTEGER NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    categoria VARCHAR(50),
    fecha_guardado DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_api_productos PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS api_posts(
    id INTEGER AUTO_INCREMENT,
    api_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_api_posts PRIMARY KEY (id)
);