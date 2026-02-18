package client.command;

import client.managers.Network;
import common.command.CommandTypes;
import common.command.Container;
import common.utillity.Console;
import common.utillity.ExecutionResponse;


/**
 * Команда, которая удаляет первый элемент коллекции
 */
public class RemoveFirst extends Command {
    private final Console console;
    private final Network manager;

    public RemoveFirst(Console console, Network manager) {
        super("remove_first","удалить первый элемент из коллекции");
        this.console = console;
        this.manager = manager;
    }

    @Override
    public ExecutionResponse apply(String[] arguments) {
        if(!arguments[1].isEmpty()) {
            return new ExecutionResponse(false, "Неправильное кол-во аргументов \nИспользование: '" + getName() + "'");
        }

        manager.sendData(new Container(CommandTypes.Remove_first));
        Container container = manager.receiveData();

        return container.getExecutionResponse();
    }
}
