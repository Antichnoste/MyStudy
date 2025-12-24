
-- CREATE INDEX idx_люди_ид_отчество ON "Н_ЛЮДИ" USING BTREE ("ИД", "ОТЧЕСТВО");
-- CREATE INDEX idx_обучения_члвк_ид ON "Н_ОБУЧЕНИЯ" USING BTREE ("ЧЛВК_ИД");
-- CREATE INDEX idx_ученики_члвк_ид ON "Н_УЧЕНИКИ" USING BTREE ("ЧЛВК_ИД");


EXPLAIN ANALYSE SELECT P."ФАМИЛИЯ", E."НЗК", S."ИД"
FROM "Н_УЧЕНИКИ" S
JOIN "Н_ОБУЧЕНИЯ" E ON S."ЧЛВК_ИД" = E."ЧЛВК_ИД"
JOIN "Н_ЛЮДИ" P ON P."ИД" = E."ЧЛВК_ИД"
WHERE P."ОТЧЕСТВО" > 'Александрович'
  AND E."ЧЛВК_ИД" = 105590;