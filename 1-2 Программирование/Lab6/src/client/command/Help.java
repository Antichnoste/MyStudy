package client.command;

import common.command.CommandTypes;
import common.utillity.Console;
import common.utillity.ExecutionResponse;

import java.util.Map;

/**
 * Команда по выводу справки по доступным командам
 */
public class Help extends Command {
    private final Console console;
    private final Map<CommandTypes, Command> commands;

    public Help(Console console, Map<CommandTypes, Command> commands) {
        super("help", "вывести справку по доступным командам");
        this.console = console;
        this.commands = commands;
    }

    /**
     * Исполнение командны
     *
     * @param arguments массив с аргументами
     * @return возвращает результат о выполнении команды
     */
    public ExecutionResponse apply(String[] arguments) {
        if (!arguments[1].isEmpty()) {
            return new ExecutionResponse(false, "Неправильное кол-во аргументов \nИспользование: '" + getName() + "'");
        }

        StringBuilder sb = new StringBuilder();
        for (Command command : commands.values()) {
            sb.append(String.format(" %-35s%-1s%n", command.getName(), command.getDescription()));
        }
        return new ExecutionResponse(sb.toString());
    }
}
