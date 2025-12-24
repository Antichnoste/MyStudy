package client.command;

import common.utillity.Console;
import common.utillity.ExecutionResponse;

/**
 * Команда выполнения скрипта из файла
 */
public class ExecuteScript extends Command {
    private final Console console;

    public ExecuteScript(Console console) {
        super("execute_script <file_name>", "выполнить скрипт из файла");
        this.console = console;
    }


    /**
     * Исполнение команды
     * @param arguments массив с аргументами
     * @return
     */
    public ExecutionResponse apply(String[] arguments) {
        if(arguments[1].isEmpty()) {
            return new ExecutionResponse(false, "Неправильное кол-во аргументов \nИспользование: '" + getName() + "'");
        }


        return new ExecutionResponse("Выполнение скрипта '" + arguments[1] + "'...");
    }
}
