package client.command;

import client.managers.Network;
import common.command.CommandTypes;
import common.command.Container;
import common.utillity.Console;
import common.utillity.ExecutionResponse;

/**
 * Команда для очистки коллекции
 */
public class Clear extends Command {
    private final Console console;
    private final Network network;

    public Clear(Console console, Network network) {
        super("clear", "очистить коллекцию");
        this.console = console;
        this.network = network;
    }

    @Override
    public ExecutionResponse apply(String[] arguments) {
        if(!arguments[1].isEmpty()) {
            return new ExecutionResponse(false, "Неправильное кол-во аргументов \nИспользование: '" + getName() + "'");
        }

        network.sendData(new Container(CommandTypes.Clear, null, null));
        Container response = network.receiveData();

        return response.getExecutionResponse();
    }
}
