package command;

import managers.CommandManager;
import utility.Console;
import utility.ExecutionResponse;

import java.util.List;

public class History extends Command {
    private final Console console;
    private final CommandManager manager;

    public History(Console console, CommandManager manager) {
        super("history", "вывести последние 15 команд (без их аргументов)");
        this.console = console;
        this.manager = manager;
    }


    /**
     * Исполнение команды
     * @param arguments массив с аргументами
     * @return возвращает результат выполнения команды
     */
    @Override
    public ExecutionResponse apply(String[] arguments) {
        if (!arguments[1].isEmpty()) {
            return new ExecutionResponse(false, "Неправильное кол-во аргументов \nИспользование: '" + getName() + "'");
        }

        StringBuilder commandsHistory = new StringBuilder();

        if (manager.getCommandHistory().size() < 15){
            for (String command : manager.getCommandHistory()){
                commandsHistory.append(" ").append(command).append("\n");
            }
        } else {
            for (int i = manager.getCommandHistory().size()-15; i < manager.getCommandHistory().size(); i++) {
                commandsHistory.append(" ").append(manager.getCommandHistory().get(i)).append("\n");
            }
        }


        return new ExecutionResponse(commandsHistory.toString());

    }
}
