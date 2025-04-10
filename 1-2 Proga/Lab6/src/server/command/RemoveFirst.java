package server.command;

import common.command.Container;
import common.models.Movie;
import common.utillity.ExecutionResponse;
import server.managers.CollectionManager;

/**
 * Команда, которая удаляет первый элемент коллекции
 */
public class RemoveFirst extends Command {
    private final CollectionManager manager;

    public RemoveFirst(CollectionManager manager) {
        super("remove_first","удалить первый элемент из коллекции");
        this.manager = manager;
    }

    @Override
    public Container apply(Container container) {
        Movie cur = manager.getCollection().getFirst();
        manager.remove(cur.getId());
        manager.sort();

        return new Container(new ExecutionResponse("Первый фильм успешно удалён!"));
    }
}
