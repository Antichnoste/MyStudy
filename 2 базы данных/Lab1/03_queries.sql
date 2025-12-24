SELECT * FROM enity;

SELECT NAME, world_id FROM level GROUP BY world_id, NAME;

-- SELECT * FROM actions where evaluation_of_actions <> 'положительное' ORDER BY committed_at ASC;

-- SELECT name FROM enity WHERE id = (
--     SELECT enity_id FROM soul where id = (
--         SELECT id_soul FROM ID_SOUL_ID_ACTIONS where id_actions = (
--             SELECT id FROM actions where evaluation_of_actions = 'положительное')));
