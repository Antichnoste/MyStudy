package client.command;

import client.managers.Ask;
import common.command.CommandTypes;
import common.command.Container;
import common.utillity.Console;
import common.utillity.ExecutionResponse;
import common.models.Movie;
import client.managers.Network;

/**
 * Команда, которая удаляет самый все элементы больше введённого
 * compareTo написано по полю oscarsCount
 */
public class RemoveGreater extends Command {
    private final Console console;
    private final Network manager;

    public RemoveGreater(Console console, Network manager) {
        super("remove_greater {element}", "удалить из коллекции все элементы, превышающие заданный");
        this.console = console;
        this.manager = manager;
    }

    @Override
    public ExecutionResponse apply(String[] arguments) {
        try{
            if (!arguments[1].isEmpty()){
                return new ExecutionResponse(false, "Неправильное количество аргументов!\nИспользование: '" + getName() + "'");
            }

            Movie cur = Ask.askMovie(console, 0);

            manager.sendData(new Container(CommandTypes.Remove_greater, cur));
            Container container = manager.receiveData();

            return container.getExecutionResponse();
        } catch (Ask.AskBreak e){
            return new ExecutionResponse(false, "Поля Фильма не валидны! Команда не сработала");
        }
    }
}
