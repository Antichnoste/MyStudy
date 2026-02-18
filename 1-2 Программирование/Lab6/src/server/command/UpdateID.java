package server.command;

import common.command.Container;
import common.models.Movie;
import common.utillity.ExecutionResponse;
import server.managers.CollectionManager;

/**
 * Команда по обновлению элемента в коллекции
 */
public class UpdateID extends Command {
    private final CollectionManager manager;

    public UpdateID(CollectionManager manager) {
        super("update id {element}", "обновить значение элемента коллекции, id которого равен заданному");
        this.manager = manager;
    }

    @Override
    public Container apply(Container container) {

        Movie cur = (Movie) container.getObj();
        int id = cur.getId();

        Movie old = manager.getById(id);
        if (old == null || !manager.getCollection().contains(old)){
            return new Container(new ExecutionResponse(false, "По такому ID не существует фильма!"));
        }

        manager.remove(old.getId());
        manager.add(cur);
        manager.sort();
        return new Container(new ExecutionResponse("Обновлено!"));
    }
}
