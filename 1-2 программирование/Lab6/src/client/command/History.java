package client.command;

import client.managers.Network;
import common.command.CommandTypes;
import common.command.Container;
import common.utillity.Console;
import common.utillity.ExecutionResponse;

public class History extends Command {
    private final Console console;
    private final Network network;

    public History(Console console, Network network) {
        super("history", "вывести последние 15 команд (без их аргументов)");
        this.console = console;
        this.network = network;
    }


    @Override
    public ExecutionResponse apply(String[] arguments) {
        if (!arguments[1].isEmpty()) {
            return new ExecutionResponse(false, "Неправильное кол-во аргументов \nИспользование: '" + getName() + "'");
        }

        network.sendData(new Container(CommandTypes.History));
        Container container = network.receiveData();

        return container.getExecutionResponse();

    }
}
