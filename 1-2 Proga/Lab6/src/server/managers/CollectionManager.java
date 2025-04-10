package server.managers;

import common.models.Movie;
import common.utillity.Sortable;

import java.io.Serializable;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;

/**
 * Класс менеджера коллекции
 */
public class CollectionManager implements Serializable, Sortable {
    private static final long serialVersionUID = 2L;

    private int currentId = 1;
    private LocalDateTime LastSaveTime = null;
    private LocalDateTime LastInitTime = null;
    private Map<Integer, Movie> movies = new HashMap<>();
    private LinkedList<Movie> collection = new LinkedList<>();
    private final DumpManager dumpManager;

    /**
     * Конструктор
     * @param dumpManager
     */
    public CollectionManager(DumpManager dumpManager) {
        this.dumpManager = dumpManager;
        LastSaveTime = null;
        LastInitTime = null;
    }

    /**
     * @return ID последнего добавленного элемента
     */
    public int getCurrentId() {
        return currentId;
    }

    /**
     * @return Время последнего сохранения коллекции
     */
    public LocalDateTime getLastSaveTime() {
        return LastSaveTime;
    }

    /**
     * @return Время последней инициалтзации коллекции
     */
    public LocalDateTime getLastInitTime() {
        return LastInitTime;
    }

    /**
     * @return коллекцию
     */
    public LinkedList<Movie> getCollection() {
        return collection;
    }

    /**
     * @param id индекс, по которому надо вернуть объект класса Movie
     * @return объект класса Movie по индексу id
     */
    public Movie getById(int id) {
        return movies.get(id);
    }

    /**
     * Проверяет находиться ли фильм в коллекции
     * @param movie объект класса, который мы проверяем
     * @return True если находится в коллекции, False - не находится
     */
    public boolean isContains(Movie movie) {
        return getById(movie.getId()) != null;
    }

    /**
     * @return свободный ID коллекции
     */
    public int getFreeId(){
        while (getById(currentId) != null){
            currentId++;
        }
        return currentId;
    }

    /**
     * Обеспечивает наличие объекта класса Movie в коллекции
     * @param movie объект класса Movie, который надо добавить в коллекцию
     * @return True - объекта не было и время обновлено, False - объект был и время не обновлено
     */
    public boolean add(Movie movie) {
        if (isContains(movie)) {
            return false;
        }

        movies.put(movie.getId(), movie);
        collection.add(movie);
        sort();
        return true;
    }

    /**
     * Сортировать коллекцию
     */
    public void sort() {

        Comparator<Movie> nameComparator = new Comparator<Movie>() {
            @Override
            public int compare(Movie o1, Movie o2) {
                return o1.getName().compareTo(o2.getName());
            }
        };

        Collections.sort(collection, nameComparator);

        //Collections.sort(collection, (m1, m2) -> Integer.compare(m1.getOscarsCount(), m2.getOscarsCount()));
    }

    /**
     * Сохраняет коллекцию в файл
     */
    public void saveCollection(){
        dumpManager.writeCollection(collection);
        LastSaveTime = LocalDateTime.now();
    }

    /**
     * Обеспечивает отсутствие элемента в коллекции по ID
     * @param id уникалтный номер элемента в коллекции
     * @return True - объект был и его не стало, False - объекта не было
     */
    public boolean remove(int id) {
        Movie movie = getById(id);
        if (movie == null) { return false;}

        movies.remove(movie.getId());
        collection.remove(movie);
        sort();
        return true;
    }

    /**
     * Загрузка коллекции из файла (инициализация)
     * @return True - успешно всё загрузилось, False - произошла обшибка
     */
    public boolean loadCollection(){
        movies.clear();
        dumpManager.readCollection(collection);
        LastInitTime = LocalDateTime.now();

        for (Movie movie : collection) {
            if (getById(movie.getId()) != null) {
                collection.clear();
                movies.clear();
                return false;
                // Очищаем коллекцию так как мы встретили элемент, ID которого уже есть в коллекции
            } else{
                if (movie.getId() > currentId) {
                    currentId = movie.getId();
                }
                movies.put(movie.getId(), movie);
            }
        }
        sort();
        return true;
    }

    /**
     * @return возвращает коллекцию, переведённую в строку
     */
    @Override
    public String toString()    {
        //if (collection.isEmpty()) {return "Коллекция пуста!";}

        StringBuilder sb = new StringBuilder();

        sb.append("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n");

        sb.append(String.format("|%5s%s%5s", "", "ID", "") + //12
                String.format("|%8s%s%8s", "", "Name", "") + // 20
                String.format("|%5s%s%5s", "", "X", "") + //11
                String.format("|%5s%s%5s", "", "Y", "") + // 11
                String.format("|%1s%s%1s", "", "CreationTime", "") + // 14
                String.format("|%1s%s%1s", "", "CreationDate", "") + // 14
                String.format("|%1s%s%1s", "", "OscarsCount", "") + //13
                String.format("|%8s%s%8s", "", "Tagline", "") + //23
                String.format("|%2s%s%2s", "", "Genre", "") + // 9
                String.format("|%1s%s%1s", "", "MpaaRating", "") + // 12
                String.format("|%1s%s%1s", "", "Screenwriter's Name", "") + // 21
                String.format("|%1s%s%1s", "", "Screenwriter's Height", "") + // 23
                String.format("|%1s%s%1s", "", "Screenwriter's Weight", "") + // 23
                String.format("|%1s%s%1s|%n", "", "Screenwriter Eye Color", "")); // 24

        sb.append("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n");

        for(Movie movie : collection) {
            sb.append(String.format("|%" + ((12 - Integer.valueOf(movie.getId()).toString().length() + 1) / 2) + "s%s%" + ((12 - Integer.valueOf(movie.getId()).toString().length()) / 2 ) + "s", "", movie.getId(), "") + //12
                    String.format("|%"+ ((20 - movie.getName().length() + 1) / 2) + "s%s%" + ((20 - movie.getName().length()) / 2) + "s", "", movie.getName(), "") + // 20
                    String.format("|%"+ ((11 - movie.getCoordinates().getX().toString().length() + 1) / 2) + "s%s%" + ((11 - movie.getCoordinates().getX().toString().length()) / 2) + "s", "", movie.getCoordinates().getX(), "") + //11
                    String.format("|%"+ ((11 - movie.getCoordinates().getY().toString().length() + 1) / 2) +"s%s%"+ ((11 - movie.getCoordinates().getY().toString().length()) / 2) +"s", "", movie.getCoordinates().getY(), "") + // 11
                    String.format("|%3s%s%3S", "", movie.getCreationDate().format(DateTimeFormatter.ofPattern("HH:mm:ss")), "") + // 14
                    String.format("|%2s%s%2s", "", movie.getCreationDate().format(DateTimeFormatter.ofPattern("dd.MM.yyyy")), "") + // 14
                    String.format("|%"+ ((13 - Integer.valueOf(movie.getOscarsCount()).toString().length() + 1) / 2) +"s%s%"+ ((13 - Integer.valueOf(movie.getOscarsCount()).toString().length()) / 2) +"s", "", movie.getOscarsCount(), "") + //13
                    String.format("|%"+ ((23 - movie.getTagline().length() + 1) / 2) +"s%s%" + ((23 - movie.getTagline().length()) / 2) +"s", "", movie.getTagline(), "") + //23

                    String.format("|%"+ ((9 - (movie.getGenre() == null ? "null" : movie.getGenre().toString()).length() + 1) / 2) +"s%s%"+ ((9 - (movie.getGenre() == null ? "null" : movie.getGenre().toString()).length()) / 2) +"s", "", (movie.getGenre() == null ? "null" : movie.getGenre()), "") + // 9

                    String.format("|%"+ ((12 - movie.getMpaaRating().toString().length() + 1) / 2) +"s%s%"+ ((12 - movie.getMpaaRating().toString().length()) / 2) +"s", "", movie.getMpaaRating(), "") + // 12
                    String.format("|%"+ ((21 - movie.getScreenwriter().getName().length() + 1) / 2) +"s%s%"+ ((21 - movie.getScreenwriter().getName().length()) / 2) +"s", "", movie.getScreenwriter().getName(), "") + // 21

                    String.format("|%"+ ((23 - (movie.getScreenwriter().getHeight() == null ? "null" : movie.getScreenwriter().getHeight().toString()).length() + 1) / 2) +"s%s%"+ ((23 - (movie.getScreenwriter().getHeight() == null ? "null" : movie.getScreenwriter().getHeight().toString()).length()) / 2) +"s","", movie.getScreenwriter().getHeight() == null ? "null" : movie.getScreenwriter().getHeight(),"") + // 23

                    String.format("|%"+ ((23 - movie.getScreenwriter().getWeight().toString().length()+1) / 2) +"s%s%"+ ((23 - movie.getScreenwriter().getWeight().toString().length()) / 2) +"s","", movie.getScreenwriter().getWeight(),"") + // 23
                    String.format("|%"+ ((24 - movie.getScreenwriter().getEyeColor().toString().length()+1) / 2) +"s%s%"+ ((24 - movie.getScreenwriter().getEyeColor().toString().length()) / 2) +"s|%n","", movie.getScreenwriter().getEyeColor(),"")); // 24
        }

        sb.append("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n");

        return sb.toString();
    }
}
