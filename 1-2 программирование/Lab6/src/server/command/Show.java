package server.command;

import common.command.Container;
import common.utillity.ExecutionResponse;
import server.managers.CollectionManager;

public class Show extends Command {
    private final CollectionManager manager;

    public Show(CollectionManager manager) {
        super("show", "вывести в стандартный поток вывода все элементы коллекции в строковом представлении");
        this.manager = manager;
    }

    @Override
    public Container apply(Container container) {
        return new Container(new ExecutionResponse(manager.toString()));
    }
}
