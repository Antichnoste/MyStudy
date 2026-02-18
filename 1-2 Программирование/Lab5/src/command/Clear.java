package command;

import managers.CollectionManager;
import models.Movie;
import utility.Console;
import utility.ExecutionResponse;

import java.util.Iterator;

/**
 * Команда для очистки коллекции
 */
public class Clear extends Command {
    private final Console console;
    private final CollectionManager manager;

    /**
     * Конструктор
     * @param console консоль
     * @param manager менеджер коллекции
     */
    public Clear(Console console, CollectionManager manager) {
        super("clear", "очистить коллекцию");
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
        if(!arguments[1].isEmpty()) {
            return new ExecutionResponse(false, "Неправильное кол-во аргументов \nИспользование: '" + getName() + "'");
        }

//        Iterator<Movie> iterator = manager.getCollection().iterator();
//
//        while(iterator.hasNext()) {
//            Movie movie = iterator.next();
//            manager.getCollection().remove(movie);
//        }
//
//        manager.sort();

        manager.getCollection().clear();
        manager.sort();
        return new ExecutionResponse(true, "Коллекция очищена!");
    }
}
