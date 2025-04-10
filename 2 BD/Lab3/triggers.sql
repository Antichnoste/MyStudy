-- Проверка, что у одной души не может быть много тел
CREATE OR REPLACE FUNCTION check_single_body_per_soul()
    RETURNS TRIGGER AS
$$
BEGIN
    IF EXISTS (SELECT 1
               FROM soul
               WHERE body_id = NEW.body_id
                 AND id != NEW.id)
    THEN
        RAISE EXCEPTION 'Тело % уже принадлежит другой душе', NEW.body_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER single_body_per_soul_trigger
    BEFORE INSERT OR UPDATE
    ON SOUL
    FOR EACH ROW
EXECUTE FUNCTION check_single_body_per_soul();

--Автоматически обновляем кол-во сущностей на каждом уровне
ALTER TABLE level ADD COLUMN entity_count INTEGER DEFAULT 0;

CREATE OR REPLACE FUNCTION update_level_entity_count()
    RETURNS TRIGGER AS $$
BEGIN
    -- При добавлении новой души
    IF TG_OP = 'INSERT' THEN
        UPDATE level
        SET entity_count = entity_count + 1
        WHERE id = NEW.level_id;
        -- При удалении души
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE level
        SET entity_count = entity_count - 1
        WHERE id = OLD.level_id;
        -- При изменении уровня души
    ELSIF TG_OP = 'UPDATE' AND NEW.level_id != OLD.level_id THEN
        UPDATE level
        SET entity_count = entity_count - 1
        WHERE id = OLD.level_id;

        UPDATE level
        SET entity_count = entity_count + 1
        WHERE id = NEW.level_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Триггер для таблицы soul
CREATE TRIGGER level_entity_count_trigger
    AFTER INSERT OR UPDATE OR DELETE
    ON SOUL
    FOR EACH ROW
    EXECUTE FUNCTION update_level_entity_count();