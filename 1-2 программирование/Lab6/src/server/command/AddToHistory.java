package server.command;

import common.command.Container;
import common.utillity.ExecutionResponse;
import server.managers.CommandManager;

public class AddToHistory extends Command {
    private final CommandManager manager;

    public AddToHistory(CommandManager manager) {
        super("","");
        this.manager = manager;
    }

    @Override
    public Container apply(Container container) {

        manager.addToHistory(container.getObj().toString());

        return new Container(new ExecutionResponse(""));
    }
}
