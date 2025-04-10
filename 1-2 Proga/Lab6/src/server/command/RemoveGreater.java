package server.command;

import common.command.Container;
import common.models.Movie;
import common.utillity.ExecutionResponse;
import server.managers.CollectionManager;

/**
 * Команда, которая удаляет самый все элементы больше введённого
 * compareTo написано по полю oscarsCount
 */
public class RemoveGreater extends Command {
    private final CollectionManager manager;

    public RemoveGreater(CollectionManager manager) {
        super("remove_greater {element}", "удалить из коллекции все элементы, превышающие заданный");
        this.manager = manager;
    }

    @Override
    public Container apply(Container container) {

        Movie cur = (Movie) container.getObj();

        manager.getCollection().removeIf(movie -> movie.compareTo(cur) > 0);
        manager.sort();

        return new Container(new ExecutionResponse("Из коллекции успешно удалены все фильмы, кол-во Оскаров которых больше " + cur.getOscarsCount() + "!"));
    }
}
