package command;

import managers.CommandManager;
import utility.Console;
import utility.ExecutionResponse;

//Если CommandManager больше нигде не пригодиться кроме как в Help, то его надо заменить на CollectionManager

/**
 * Команда по выводу справки по доступным командам
 */
public class Help extends Command {
    private final Console console;
    private final CommandManager manager;

    /**
     * Конструктор
     * @param console консоль
     * @param manager менеджер команд
     */
    public Help(Console console, CommandManager manager) {
        super("help", "вывести справку по доступным командам");
        this.console = console;
        this.manager = manager;
    }

    /**
     * Исполнение командны
     *
     * @param arguments массив с аргументами
     * @return возвращает результат о выполнении команды
     */
    @Override
    public ExecutionResponse apply(String[] arguments) {
        if (!arguments[1].isEmpty()) {
            return new ExecutionResponse(false, "Неправильное кол-во аргументов \nИспользование: '" + getName() + "'");
        }

        StringBuilder sb = new StringBuilder();
        for (Command command : manager.getCommands().values()) {
            sb.append(String.format(" %-35s%-1s%n", command.getName(), command.getDescription()));
        }
        return new ExecutionResponse(sb.toString());
    }
}
