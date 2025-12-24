package client.command;

import client.managers.Network;
import common.command.CommandTypes;
import common.command.Container;
import common.utillity.Console;
import common.utillity.ExecutionResponse;

import java.time.format.DateTimeFormatter;

/**
 * Команда по выводу всех фильмов, у которых слоган начинается с определённой строки
 */
public class FilterStartsWithTagline extends Command {
    private final Console console;
    private final Network network;

    public FilterStartsWithTagline(Console console, Network network) {
        super("filter_starts_with_tagline tagline", "вывести элементы, значение поля tagline которых начинается с заданной подстроки");
        this.console = console;
        this.network = network;
    }

    @Override
    public ExecutionResponse apply(String[] arguments) {

        network.sendData(new Container(CommandTypes.Filter_starts_with_tagline, null, arguments[1]));
        Container container = network.receiveData();

        return container.getExecutionResponse();
    }
}
