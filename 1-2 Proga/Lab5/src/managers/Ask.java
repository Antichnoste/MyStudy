package managers;

import utility.*;
import models.*;

import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.NoSuchElementException;

/**
 * Класс менеджера по считыванию данных из консоли
 */
public class Ask {
    /**
     * Исключение для выхода из цикла опроса
     */
    public static class AskBreak extends Exception {}

    /**
     * Функция считывания объекта класса Movie из консоли
     *
     * @param console консоль
     * @param id уникальный номер учебной группы
     * @return возвращает считанный объект класса Movie
     * @throws AskBreak исключение, которые происходит при принудительной остановки обработки
     */
    public static Movie askMovie (Console console, int id) throws AskBreak{
        try {
            String name;
            while(true){
                console.print("Movie's name: ");
                name = console.readln().trim();
                if (name.equals("exit")) {
                    throw new AskBreak();
                }

                if (!name.isEmpty()) {
                    break;
                } else{
                    console.println("Название фильма не может быть пустым!");
                }

            }

            Coordinates coordinates = askCoordinate(console);

            ZonedDateTime creationDate = ZonedDateTime.now();
            creationDate = ZonedDateTime.parse(creationDate.format(DateTimeFormatter.ISO_DATE_TIME));

            int oscarsCount;
            while (true){
                    console.print("OscarsCount: ");
                    String line = console.readln().trim();
                    if (line.equals("exit")) {throw new AskBreak();}
                    if (!line.isEmpty()){
                        try{
                            oscarsCount = Integer.parseInt(line);
                            if (oscarsCount > 0) {
                                break;
                            } else {
                                console.println("Значение этого поля должно быть положительным!");
                            }
                        } catch (NumberFormatException e) {
                            console.println("Введенное нецелое число");
                        }
                    } else{
                        console.println("Количество оскаров не должно быть пустым!");
                    }
            }

            String tagline;
            while (true){
                console.print("Tagline: ");
                tagline = console.readln().trim();
                if (tagline.equals("exit")) {throw new AskBreak();}
                if (!tagline.isEmpty()){
                    break;
                } else{
                    console.println("Слоган фильма не может быть пустым!");
                }
            }

            MovieGenre genre = askMovieGenre(console);

            MpaaRating mpaaRatin = askMpaaRating(console);

            Person person = askPerson(console);

            return new Movie(id, name, coordinates, creationDate,oscarsCount, tagline, genre, mpaaRatin, person);

        } catch (NoSuchElementException | IllegalStateException e){
            console.printError("Ошибка чтения");
            return null;
        }
    }

    /**
     * Функция считывания объекта класса Coordinates из консоли
     *
     * @param console консоль
     * @return возвращает считанный объект класса Coordinates
     * @throws AskBreak исключение, которые происходит при принудительной остановки обработки
     */
    public static Coordinates askCoordinate (Console console) throws AskBreak {
        try {
            Double x;
            while (true) {
                console.print("Coordinates x: ");
                String line = console.readln().trim();
                if (line.equals("exit")) {throw new AskBreak();}
                if (!line.isEmpty()) {
                    try {
                        x = Double.parseDouble(line);
                        break;
                    } catch (NumberFormatException e) {
                        console.println("Введите число");
                        if (line.contains(",")) console.println("Используйте '.' вместо ',' для ввода номера");
                    }
                } else{
                    console.println("Координаты не могут быть пустыми!");
                }
            }

            double y;
            while (true) {
                console.print("Coordinates y: ");
                String line = console.readln().trim();
                if (line.equals("exit")) { throw new AskBreak();}
                if (!line.isEmpty()) {
                    try {
                        y = Double.parseDouble(line);
                        if (y > -708) {
                            break;
                        } else{
                           console.println("Значение этого поля должно быть больше -708");
                        }
                    } catch (NumberFormatException e) {
                        console.println("Введите число");
                        if (line.contains(",")) console.println("Используйте '.' вместо ',' для ввода номера");
                    }
                } else{
                    console.println("Координаты не могут быть пустыми!");
                }
            }
            return new Coordinates(x, y);

        } catch (NoSuchElementException | IllegalStateException e) {
            console.printError("Ошибка чтения");
            return null;
        }
    }

    /**
     * Функция считывания объекта класса Person из консоли
     *
     * @param console консоль
     * @return возвращает считанный объект класса Person
     * @throws AskBreak исключение, которые происходит при принудительной остановки обработки
     */
    public static Person askPerson (Console console) throws AskBreak {
        try{
            String name;

            while(true){
                console.print("Screenwriter's name: ");
                name = console.readln().trim();
                if (name.equals("exit")) {throw new AskBreak();}
                if (!name.isEmpty()){
                    break;
                } else{
                    console.println("Имя сценариста не может быть пустым!");
                }
            }

            Float height;
            while (true) {
                console.print("Screenwriter's Height: ");
                String line = console.readln().trim();
                if (line.equals("exit")) {
                    throw new AskBreak();
                }

                if (!line.isEmpty()) {
                    try {
                        height = Float.parseFloat(line);
                        if (height > 0) {
                            break;
                        } else {
                            console.println("Значение этого поля должно быть положительным");
                        }
                    } catch (NumberFormatException e) {
                        console.println("Введите число");
                        if (line.contains(",")) console.println("Используйте '.' вместо ',' для ввода номера");
                    }
                } else{
                    height = null;
                    break;
                }
            }

            Float weight;
            while (true){
                console.print("Screenwriter's Weight: ");
                String line = console.readln().trim();
                if (line.equals("exit")) {throw new AskBreak();}
                if (!line.isEmpty()){
                    try{
                        weight = Float.parseFloat(line);
                        if (weight > 0){
                            break;
                        } else {
                            console.println("Значение этого поля должно быть положительным");
                        }
                    } catch (NumberFormatException e) {
                        console.println("Введите число");
                        if (line.contains(",")) console.println("Используйте '.' вместо ',' для ввода номера");
                    }
                } else{
                    console.println("Вес сценариста не может быть пустым!");
                }
            }

            Color eyeColor = askColor(console);

            return new Person(name, height, weight, eyeColor);
        } catch (NoSuchElementException | IllegalStateException e) {
            console.printError("Ошибка чтения");
            return null;
        }

    }

    /**
     * Функция считывания объекта класса MovieGenre из консоли
     *
     * @param console консоль
     * @return возвращает считанный объект класса MovieGenre
     * @throws AskBreak исключение, которые происходит при принудительной остановки обработки
     */
    public static MovieGenre askMovieGenre (Console console) throws AskBreak {
        try{
            MovieGenre genre;
            while (true){
                console.print("Genre ("+ MovieGenre.names() +"): ");
                String line = console.readln().trim();
                if (line.equals("exit")) {throw new AskBreak();}
                if (!line.isEmpty()) {
                    try{
                        genre = MovieGenre.valueOf(line);
                        break;
                    } catch (NullPointerException | IllegalArgumentException  e) {
                        console.println("Недопустимый жанр");
                    }
                } else {
                    genre = null;
                    break;
                }
            }
            return genre;
        } catch (NoSuchElementException | IllegalStateException e){
            console.printError("Ошибка чтения");
            return null;
        }


    }

    /**
     * Функция считывания объекта класса MpaaRating из консоли
     *
     * @param console консоль
     * @return возвращает считанный объект класса MpaaRating
     * @throws AskBreak исключение, которые происходит при принудительной остановки обработки
     */
    public static MpaaRating  askMpaaRating  (Console console) throws AskBreak {
        try{
            MpaaRating rating;
            while (true){
                console.print("Rating ("+ MpaaRating.names() +"): ");
                String line = console.readln().trim();
                if (line.equals("exit")) {throw new AskBreak();}
                if (!line.isEmpty()) {
                    try{
                        rating = MpaaRating.valueOf(line);
                        break;
                    } catch (NullPointerException | IllegalArgumentException  e) {
                        console.println("Недопустимый формат рейтинга");
                    }
                } else{
                    console.println("Рейтинг не может быть пустым!");
                }
            }
            return rating;
        } catch (NoSuchElementException | IllegalStateException e){
            console.printError("Ошибка чтения");
            return null;
        }
    }

    /**
     * Функция считывания объекта класса Color из консоли
     *
     * @param console консоль
     * @return возвращает считанный объект класса Color
     * @throws AskBreak исключение, которые происходит при принудительной остановки обработки
     */
    public static Color askColor (Console console) throws AskBreak{
        try{
            Color color;
            while (true){
                console.print("Screenwriter Eye Color ("+ Color.names() +"): ");
                String line = console.readln().trim();
                if (line.equals("exit")) {throw new AskBreak();}
                if (!line.isEmpty()) {
                    try{
                        color = Color.valueOf(line);
                        break;
                    } catch (NullPointerException | IllegalArgumentException  e) {
                        console.println("Недопустимый цветовой формат");
                    }
                } else {
                    color = null;
                }
            }
            return color;
        } catch (NoSuchElementException | IllegalStateException e){
            console.printError("Ошибка чтения");
            return null;
        }
    }
}