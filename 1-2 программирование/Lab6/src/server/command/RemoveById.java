package server.command;

import common.command.Container;
import common.utillity.ExecutionResponse;
import server.managers.CollectionManager;

public class RemoveById extends Command {
    private final CollectionManager manager;

    public RemoveById(CollectionManager manager) {
        super("remove_by_id id", "удалить элемент из коллекции по его id");
        this.manager = manager;
    }

    @Override
    public Container apply(Container container) {

        int id = (int) container.getObj();

        if (manager.getById(id) == null || !manager.getCollection().contains(manager.getById(id))){
            return new Container(new ExecutionResponse(false, "Не существующий ID"));
        }
        manager.remove(id);
        manager.sort();

        return new Container( new ExecutionResponse("Фильм успешно удалён!"));
    }
}
