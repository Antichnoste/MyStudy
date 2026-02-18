package client.command;

import common.command.CommandTypes;
import common.command.Container;
import common.utillity.Console;
import common.utillity.ExecutionResponse;
import client.managers.Network;

public class FilterContainsName extends Command {
    private final Console console;
    private final Network network;

    public FilterContainsName(Console console, Network network) {
        super("filter_contains_name name", "вывести элементы, значение поля name которых содержит заданную подстроку");
        this.console = console;
        this.network = network;
    }

    /**
     * Исполнение команды
     * @param arguments массив с аргументами
     * @return результат выполнения команды
     */
    @Override
    public ExecutionResponse apply(String[] arguments) {

        network.sendData(new Container(CommandTypes.Filter_contains_name, null, arguments[1]));
        Container response = network.receiveData();

        return response.getExecutionResponse();
    }
}
