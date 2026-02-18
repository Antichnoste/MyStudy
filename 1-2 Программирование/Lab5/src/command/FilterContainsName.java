package command;

import managers.CollectionManager;
import models.Movie;
import utility.Console;
import utility.ExecutionResponse;

import java.time.format.DateTimeFormatter;

public class FilterContainsName extends Command {
    private final Console console;
    private final CollectionManager manager;

    /**
     * Конструктор
     * @param console консоль
     * @param manager менеджер коллекции
     */
    public FilterContainsName(Console console, CollectionManager manager) {
        super("filter_contains_name name", "вывести элементы, значение поля name которых содержит заданную подстроку");
        this.console = console;
        this.manager = manager;
    }

    /**
     * Исполнение команды
     * @param arguments массив с аргументами
     * @return результат выполнения команды
     */
    @Override
    public ExecutionResponse apply(String[] arguments) {
        StringBuilder elements = new StringBuilder();

        elements.append("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n");

        elements.append(String.format("|%5s%s%5s", "", "ID", "") + //12
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

        elements.append("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n");



        for (Movie movie : manager.getCollection()){
            if (movie.getName().contains(arguments[1])){
                elements.append(String.format("|%" + ((12 - Integer.valueOf(movie.getId()).toString().length() + 1) / 2) + "s%s%" + ((12 - Integer.valueOf(movie.getId()).toString().length()) / 2 ) + "s", "", movie.getId(), "") + //12
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
        }

        elements.append("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n");


        return new ExecutionResponse(elements.toString());
    }
}
