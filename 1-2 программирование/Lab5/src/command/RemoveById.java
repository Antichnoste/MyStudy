package command;

import managers.CollectionManager;
import utility.Console;
import utility.ExecutionResponse;

import java.util.Collection;

public class RemoveById extends Command {
    private final Console console;
    private final CollectionManager manager;

    public RemoveById(Console console, CollectionManager manager) {
        super("remove_by_id id", "удалить элемент из коллекции по его id");
        this.console = console;
        this.manager = manager;
    }

    @Override
    public ExecutionResponse apply(String[] arguments) {
        if (arguments[1].isEmpty()) {
            return new ExecutionResponse(false, "Неправильное количество аргументов!\nИспользование: '" + getName() + "'");
        }

        int id = -1;
        try {
            id = Integer.parseInt(arguments[1].trim());
        } catch (NumberFormatException e) {
            return new ExecutionResponse(false, "ID не распознан");
        }

        if (manager.getById(id) == null || !manager.getCollection().contains(manager.getById(id))){
            return new ExecutionResponse(false, "Не существующий ID");
        }
        manager.remove(id);
        manager.sort();
        return new ExecutionResponse("Фильм успешно удалён!");
    }
}
