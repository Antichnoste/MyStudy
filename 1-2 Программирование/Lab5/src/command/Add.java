package command;

import managers.Ask;
import managers.CollectionManager;
import managers.CommandManager;
import models.Movie;
import utility.Console;
import utility.ExecutionResponse;

public class Add extends Command {
    private final Console console;
    private final CollectionManager manager;

    /**
     * Конструктор
     * @param console консоль
     * @param manager менеджер коллекции
     */
    public Add(Console console, CollectionManager manager) {
        super("add {element}", "добавить новый элемент в коллекцию");
        this.console = console;
        this.manager = manager;
    }

    /**
     * Исполнение командны
     *
     * @param arguments массив с аргументами
     * @return возвращает результат о выполнении команды
     */
    @Override
    public ExecutionResponse apply(String[] arguments) {
        if (!arguments[1].isEmpty()) {
            return new ExecutionResponse(false, "Неправильное кол-во аргументов \nИспользование: '" + getName() + "'");
        }
        try {
            console.println("Создание нового фильма...");
            Movie movie = Ask.askMovie(console, manager.getFreeId());

            if (movie != null && movie.isValid()) {
                manager.add(movie);
                return new ExecutionResponse(true, "Фильм успешно создан!");
            } else {
                return new ExecutionResponse(false, "Входные данные не валидны! Фильм не создан!");
            }

        } catch (Ask.AskBreak e){
            return new ExecutionResponse(false, "Ошибка...");
        }
    }
}
