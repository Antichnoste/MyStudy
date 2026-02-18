package client.command;

import client.managers.Network;
import common.command.CommandTypes;
import common.command.Container;
import common.utillity.Console;
import common.utillity.ExecutionResponse;

public class RemoveById extends Command {
    private final Console console;
    private final Network manager;

    public RemoveById(Console console, Network manager) {
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

        manager.sendData(new Container(CommandTypes.Remove_by_id, id));
        Container response = manager.receiveData();

        return response.getExecutionResponse();
    }
}
