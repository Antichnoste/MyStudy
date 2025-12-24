package server.command;

import common.command.Container;
import common.utillity.ExecutionResponse;
import server.managers.CollectionManager;

/**
 * Команда для очистки коллекции
 */
public class Clear extends Command {

    private final CollectionManager collectionManager;

    public Clear(CollectionManager collectionManager) {
        super("clear", "очистить коллекцию");
        this.collectionManager = collectionManager;
    }

    @Override
    public Container apply(Container container) {

        collectionManager.getCollection().clear();
        collectionManager.sort();

        return new Container(null, new ExecutionResponse(true, "Коллекция очищена!"), null);
    }
}
