package client.command;

import client.managers.Ask;
import client.managers.Network;
import common.command.CommandTypes;
import common.command.Container;
import common.models.Movie;
import common.utillity.Console;
import common.utillity.ExecutionResponse;

public class Add extends Command {
    private final Console console;
    private final Network manager;

    /**
     * Конструктор
     * @param console консоль
     * @param manager менеджер коллекции
     */
    public Add(Console console, Network manager) {
        super("add {element}", "добавить новый элемент в коллекцию");
        this.console = console;
        this.manager = manager;
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

        try {
            console.println("Создание нового фильма...");
            Movie movie = Ask.askMovie(console, 100);

            if (movie != null && movie.isValid()) {

                manager.sendData(new Container(CommandTypes.Add, null, movie));
                Container command = manager.receiveData();

                return command.getExecutionResponse();
            } else {
                return new ExecutionResponse(false, "Входные данные не валидны! Фильм не создан!");
            }

        } catch (Ask.AskBreak e){
            return new ExecutionResponse(false, "Ошибка...");
        }
    }
}
