package server.command;

import common.command.Container;
import common.utillity.ExecutionResponse;
import server.managers.CollectionManager;

public class Save extends Command {
    private final CollectionManager manager;

    public Save(CollectionManager manager) {
        super("save", "сохранить коллекцию в файл");
        this.manager = manager;
    }


    @Override
    public Container apply(Container container) {

        manager.saveCollection();
        return new Container(new ExecutionResponse(""));
    }
}
