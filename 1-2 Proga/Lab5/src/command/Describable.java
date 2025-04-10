package command;

/**
 * Интерфейс для классов, которые имею имя и описание
 */
public interface Describable {

    /**
     * @return возвращает название
     */
    public String getName();

    /**
     * @return возвращает описание
     */
    public String getDescription();
}
