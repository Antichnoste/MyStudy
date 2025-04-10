package models;

import java.awt.*;
import java.time.ZonedDateTime;
import java.time.format.DateTimeParseException;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

import utility.*;

/**
 *  Класс "фильм"
 */

public class Movie extends Element implements Validatable{
    private Integer id; //Поле не может быть null, Значение поля должно быть больше 0, Значение этого поля должно быть уникальным, Значение этого поля должно генерироваться автоматически
    private String name; //Поле не может быть null, Строка не может быть пустой
    private Coordinates coordinates; //Поле не может быть null
    private java.time.ZonedDateTime creationDate; //Поле не может быть null, Значение этого поля должно генерироваться автоматически
    private int oscarsCount; //Значение поля должно быть больше 0
    private String tagline; //Поле не может быть null
    private MovieGenre genre; //Поле может быть null
    private MpaaRating mpaaRating; //Поле не может быть null
    private Person screenwriter;

    private int MIN_VALUE_ID = 1; // Значение поля не меньше этого значения
    private int MAX_VALUE_OSCARS_COUNT = 1; // Значение поля не меньше этого значения

    /**
     * Основной конструктор
     * @param id уникальный номер
     * @param name название
     * @param coordinates координаты
     * @param creationDate дата создания
     * @param oscarsCount количество Оскаров
     * @param tagline слоган
     * @param genre жанр
     * @param mpaaRating рейтинг Американской киноассоциации (рейтинг MPAA)
     * @param screenwriter сценарист
     */
    public Movie(Integer id, String name, Coordinates coordinates, ZonedDateTime creationDate, int oscarsCount, String tagline, MovieGenre genre, MpaaRating mpaaRating, Person screenwriter) {
        this.id = id;
        this.name = name;
        this.coordinates = coordinates;
        this.creationDate = creationDate;
        this.oscarsCount = oscarsCount;
        this.tagline = tagline;
        this.genre = genre;
        this.mpaaRating = mpaaRating;
        this.screenwriter = screenwriter;
    }

    /**
     * @param array массив строк, по которому строится объект класса Movie
     * @return Объект класса Movie построенному по array
     */
    public static Movie fromArray(String[] array) {
        int id;
        String name;
        Coordinates coordinates;
        ZonedDateTime creationDate;
        int oscarsCount;
        String tagline;
        MovieGenre genre;
        MpaaRating mpaaRating;
        Person screenwriter;

        try{
            try{
                id = Integer.parseInt(array[0]);
            } catch (NumberFormatException e){
                id = Integer.parseInt(null);
            }

            name = array[1];

            coordinates = new Coordinates(array[2]);

            try{
                creationDate = ZonedDateTime.parse(array[3]);
            } catch (DateTimeParseException e){
                creationDate = null;
            }

            try{
                oscarsCount = Integer.parseInt(array[4]);
            } catch (NumberFormatException  e){
                oscarsCount = 0;
            }

            tagline = array[5];

            try {
                genre = MovieGenre.valueOf(array[6]);
            } catch (IllegalArgumentException e){
                genre = null;
            }

            try{
                mpaaRating = MpaaRating.valueOf(array[7]);
            } catch (IllegalArgumentException e){
                mpaaRating = null;
            }

            screenwriter = new Person(array[8]);

            return new Movie(id, name, coordinates, creationDate, oscarsCount, tagline,genre, mpaaRating, screenwriter);

        } catch (ArrayIndexOutOfBoundsException e){}
        return null;
    }

    /**
     * Перевод объекта класса Movie в объект класса String
     *
     * @param movie объект класса Movie
     * @return объект класса String[]
     */
    public static String[] toArray(Movie movie) {
        List<String> list = new ArrayList<String>();
        list.add(Integer.toString(movie.getId()));
        list.add(movie.getName());
        list.add(movie.getCoordinates().toString());
        list.add(movie.getCreationDate().toString());
        list.add(Integer.toString(movie.getOscarsCount()));
        list.add(movie.getTagline());
        list.add(movie.getGenre() == null ? "null" : movie.getGenre().toString());
        list.add(movie.getMpaaRating().toString());
        list.add(movie.getScreenwriter().toString());

        return list.toArray(new String[0]);
    }

    /**
     * @return возвращает id объекта
     */
    @Override
    public int getId() {
        return id;
    }

    /**
     * @return возвращает имя объекта
     */
    public String getName() {
        return name;
    }

    /**
     * @return возвращает координаты объекта
     */
    public Coordinates getCoordinates() {
        return coordinates;
    }

    /**
     * @return возвращает дату создания объекта
     */
    public ZonedDateTime getCreationDate() {
        return creationDate;
    }

    /**
     * @return возвращает количество оскаров, полученных объектом
     */
    public int getOscarsCount() {
        return oscarsCount;
    }

    /**
     * @return возвращает слоган объекта
     */
    public String getTagline() {
        return tagline;
    }

    /**
     * @return возвращает жанр объекта
     */
    public MovieGenre getGenre() {
        return genre;
    }

    /**
     * @return возвращает рейтинг объекта
     */
    public MpaaRating getMpaaRating() {
        return mpaaRating;
    }

    /**
     * @return возвращает сценариста объекта
     */
    public Person getScreenwriter() {
        return screenwriter;
    }

    /**
     * Проверяет на валидность объект
     *
     * @return true, если объект валиден
     */
    @Override
    public boolean isValid() {
        if (id == null || id < MIN_VALUE_ID) return false;
        if (name == null ||  name.isEmpty()) return false;
        if (coordinates == null) return false;
        if (creationDate == null) return false;
        if (oscarsCount < MAX_VALUE_OSCARS_COUNT) return false;
        if (mpaaRating == null) return false;
        return true;
    }

    /**
     * @param element объект для сравнения
     * @return возвращает разницу между кол-во Оскаров двух разных фильмов
     */
    @Override
    public int compareTo(Element element) {
        return (int) (oscarsCount - ((Movie) element).oscarsCount);
    }

    /**
     * @return возвращает объект в строковом представлении
     */
    @Override
    public String toString() {
        return "Movie{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", coordinates=" + coordinates +
                ", creationDate=" + creationDate +
                ", oscarsCount=" + oscarsCount +
                ", tagline='" + tagline + '\'' +
                ", genre=" + (genre == null ? "null" : genre) +
                ", mpaaRating=" + mpaaRating +
                ", screenwriter=" + screenwriter +
                '}';
    }

    /**
     * Переопределение сравнения двух объектов класса Movie
     *
     * @param o с чем сравниваем наш объект
     * @return true, если объекты эквивалентны
     */
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Movie movie = (Movie) o;
        return id.equals(movie.id);
    }

    /**
     * @return возвращает Hash-код объекта
     */
    @Override
    public int hashCode() {
        return Objects.hash(id, name, coordinates, creationDate, oscarsCount, tagline, genre, mpaaRating, screenwriter);
    }
}
