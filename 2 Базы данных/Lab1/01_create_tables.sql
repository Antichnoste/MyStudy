
CREATE TYPE BODY_TYPE AS ENUM('мезоморфный', 'брахиморфный', 'долихоморфный');
CREATE TYPE EVALUATION_TYPE AS ENUM('отрицательное', 'нейтральное', 'положительное');
CREATE TYPE WORLD_TYPE AS ENUM('ад', 'земное царство', 'рай', 'Ад', 'Земное Царство', 'Земное царство', 'Рай');
CREATE TYPE RACE_TYPE AS ENUM('демон', 'человек', 'ангел');

CREATE DOMAIN POSSITIVE_INT AS INT CHECK (VALUE >= 0);

CREATE TABLE WORLD(
    id SERIAL PRIMARY KEY,
    type WORLD_TYPE NOT NULL,
    cnt_angels POSSITIVE_INT,
    cnt_demons POSSITIVE_INT,
    cnt_human POSSITIVE_INT,
    is_war BOOLEAN
);

CREATE TABLE LEVEL(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    world_id SERIAL,
    FOREIGN KEY (world_id) REFERENCES WORLD(id)
);

CREATE TABLE BODY(
    id SERIAL PRIMARY KEY,
    height FLOAT,
    weight FLOAT,
    body_type BODY_TYPE NOT NULL
);

CREATE TABLE RACE(
    id SERIAL PRIMARY KEY,
    type RACE_TYPE NOT NULL,
    status VARCHAR(20) -- для людей это всякие цари, старшие менеджеры и т.д. Для демонов - весшие, владыки и т.д. Для ангелов - высшие, архангелы, апостолы и т.д
);

CREATE TABLE ENITY( -- Enity = Soul + Body
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    age POSSITIVE_INT,

    race_id SERIAL,
    FOREIGN KEY (race_id) REFERENCES RACE(id)
);

CREATE TABLE SOUL (
    id SERIAL PRIMARY KEY,
    mind POSSITIVE_INT, -- Equal IQ

    body_id INT unique,
    FOREIGN KEY (body_id) REFERENCES BODY(id), -- Ссылка на таблицу BODY

    enity_id SERIAL,
    FOREIGN KEY (enity_id) REFERENCES ENITY(id),

    level_id SERIAL,
    FOREIGN KEY (level_id) REFERENCES LEVEL(id), -- Ссылка на таблицу LEVEL

    coordinate_X FLOAT,
    coordinate_Y FLOAT
);

CREATE TABLE ACTIONS(
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    description varchar(100),

    committed_at TIMESTAMPTZ, -- время с учётом временной зоны (TIMESTAMP - без временной зоны)

    evaluation_of_actions EVALUATION_TYPE NOT NULL
);

CREATE TABLE ID_SOUL_ID_ACTIONS(
    id_soul INT REFERENCES SOUL(id),

    id_actions INT REFERENCES ACTIONS(id),
    PRIMARY KEY (id_soul, id_actions)
);

