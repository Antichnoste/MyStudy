package client.command;

import client.managers.Network;
import common.command.CommandTypes;
import common.command.Container;
import common.utillity.Console;
import common.utillity.ExecutionResponse;
import common.utillity.StandartConsole;

/**
 * Команды для подсчёта среднего кол-ва Оскаров в коллекции
 */
public class AverageOfOscarsCount extends Command {
    private final Console console;
    private final Network manager;

    /**
     * Конструктор
     * @param console консоль
     * @param manager менеджер коллекции
     */
    public AverageOfOscarsCount(StandartConsole console, Network manager) {
        super("average_of_oscars_count", "вывести среднее значение поля oscarsCount для всех элементов коллекции");
        this.console = console;
        this.manager = manager;
    }


    /**
     * Исполение команды
     * @param arguments массив с аргументами
     * @return среднее значение кол-ва оскаров у фильмов
     */
    @Override
    public ExecutionResponse apply(String[] arguments) {

        if (!arguments[1].isEmpty()) {
            return new ExecutionResponse(false, "Неправильное кол-во аргументов \nИспользование: '" + getName() + "'");
        }

        console.println("Считаем среднее кол-во оскаров в коллекции...");

        manager.sendData(new Container(CommandTypes.Average_of_oscars_count, null, null));
        Container command = manager.receiveData();

        return command.getExecutionResponse();

    }
}
