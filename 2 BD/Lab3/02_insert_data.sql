TRUNCATE TABLE BODY CASCADE;
TRUNCATE TABLE RACE CASCADE;
TRUNCATE TABLE ENITY CASCADE;
TRUNCATE TABLE WORLD CASCADE;
TRUNCATE TABLE SOUL CASCADE;

--Проверка перового триггера
INSERT INTO BODY(id, height, weight, body_type)
VALUES (1,180.0, 80.0, 'брахиморфный'),
       (2, 100, 100, 'брахиморфный');

INSERT INTO RACE(id, type, status)
VALUES (1, 'человек', 'Король');

INSERT INTO ENITY(id, name, age, race_id)
VALUES (1,'Василий', 43, 1),
       (2, 'Игорь', 34, 1);

INSERT INTO WORLD(id, type, cnt_angels, cnt_demons, cnt_human, is_war)
VALUES (1,'Земное царство', 0,0,0,FALSE);

INSERT INTO LEVEL(id, name, world_id)
VALUES (1,'Евразия', 1);

INSERT INTO SOUL(id, mind, body_id, enity_id, level_id, coordinate_x, coordinate_y)
VALUES (1, 100, 1,1, 1, 100, 199);

INSERT INTO SOUL(id, mind, body_id, enity_id, level_id, coordinate_x, coordinate_y)
VALUES (2,101, 1, 2, 1, 110, 100); -- тут будет ошибка


--Проверка второго триггера
INSERT INTO SOUL(id, mind, body_id, enity_id, level_id, coordinate_x, coordinate_y)
VALUES (2,101, 2, 2, 1, 110, 100);

SELECT * from level;


-- INSERT INTO BODY(id, height, weight, body_type)
-- VALUES (1,180.0, 80.0, 'брахиморфный'),
--        (2,200, 95.45, 'долихоморфный'),
--        (3,175.5, 87.4, 'мезоморфный');
--
-- INSERT INTO RACE(id, type, status)
-- VALUES (1,'человек', 'Король'),
--        (2,'демон', 'Владыка'),
--        (3,'ангел', 'Апостол');
--
-- INSERT INTO WORLD(id, type, cnt_angels, cnt_demons, cnt_human, is_war)
-- VALUES (1,'Рай', 0,0,0,FALSE),
--        (2,'Земное царство', 0,0,0,FALSE),
--        (3,'Ад', 0,0,0,FALSE);
--
-- INSERT INTO LEVEL(id, name, world_id)
-- VALUES (1,'Евразия', 2),
--        (2,'Сады благодати', 1),
--        (3,'Чистилище', 3);
--
-- INSERT INTO ENITY(id, name, age, race_id)
-- VALUES (1,'Василий', 43, 1),
--        (2,'Люцифер', 10000, 2),
--        (3,'Пётр', 10000, 3);
--
-- INSERT INTO SOUL(id, mind, body_id, enity_id, level_id, coordinate_X, coordinate_Y)
-- VALUES (1,100, 2, 1, 1, 120, 3400),
--        (2,80, 3, 2, 3, -1222, 345.12),
--        (3,140, 3, 3, 2, -3456.01, 33333.22);
--
-- INSERT INTO ACTIONS(name, description, committed_at, evaluation_of_actions)
-- VALUES ('вылечил', 'помог нуждающемуся царю',NOW(), 'положительное'),
--        ('проклял', 'за греховные деяния', NOW(),'отрицательное'),
--         ('ударил', 'повздорили между собой из-за Васи', NOW(), 'нейтральное');
--
-- INSERT INTO ID_SOUL_ID_ACTIONS(id_soul, id_actions)
-- VALUES (3,1),
--        (2,2),
--        (2,3);
--
