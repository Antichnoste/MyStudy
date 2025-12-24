package utility;

/**
 * Абстрактный класс элементов
 */
public abstract class Element implements Comparable<Element>, Validatable {
    /**
     * Функция получения id
     *
     * @return возвращает id элемента
     */
    abstract public int getId();
}
