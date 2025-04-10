package client.command;

import client.managers.Network;
import common.command.CommandTypes;
import common.command.Container;
import common.utillity.Console;
import common.utillity.ExecutionResponse;

public class Show extends Command {
    private final Console console;
    private final Network manager;



    public Show(Console console, Network manager) {
        super("show", "вывести в стандартный поток вывода все элементы коллекции в строковом представлении");
        this.console = console;
        this.manager = manager;
    }

    @Override
    public ExecutionResponse apply(String[] arguments) {
        if (!arguments[1].isEmpty()) {
            return new ExecutionResponse(false, "Неправильное кол-во аргументов \nИспользование: '" + getName() + "'");
        }

        manager.sendData(new Container(CommandTypes.Show, null, null));
        Container response = manager.receiveData();

        return response.getExecutionResponse();
    }
}
