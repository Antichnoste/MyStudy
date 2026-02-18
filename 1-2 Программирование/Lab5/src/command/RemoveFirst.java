package command;

import managers.CollectionManager;
import models.Movie;
import utility.Console;
import utility.ExecutionResponse;

import java.util.Scanner;

/**
 * Команда, которая удаляет первый элемент коллекции
 */
public class RemoveFirst extends Command {
    private final Console console;
    private final CollectionManager manager;

    public RemoveFirst(Console console, CollectionManager manager) {
        super("remove_first","удалить первый элемент из коллекции");
        this.console = console;
        this.manager = manager;
    }

    @Override
    public ExecutionResponse apply(String[] arguments) {
        if(!arguments[1].isEmpty()) {
            return new ExecutionResponse(false, "Неправильное кол-во аргументов \nИспользование: '" + getName() + "'");
        }

        Movie cur = manager.getCollection().getFirst();
        manager.remove(cur.getId());
        manager.sort();

        return new ExecutionResponse("Первый фильм успешно удалён!");
    }
}
