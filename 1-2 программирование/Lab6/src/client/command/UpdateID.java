package client.command;

import client.managers.Ask;
import client.managers.Network;
import common.command.CommandTypes;
import common.command.Container;
import common.utillity.Console;
import common.utillity.ExecutionResponse;
import common.models.Movie;

/**
 * Команда по обновлению элемента в коллекции
 */
public class UpdateID extends Command {
    private final Console console;
    private final Network manager;

    public UpdateID(Console console, Network manager) {
        super("update id {element}", "обновить значение элемента коллекции, id которого равен заданному");
        this.console = console;
        this.manager = manager;
    }

    @Override
    public ExecutionResponse apply(String[] arguments) {
        try {
            if (arguments[1].isEmpty()) {
                return new ExecutionResponse(false, "Неправильное количество аргументов!\nИспользование: '" + getName() + "'");
            }

            int id = -1;
            try {
                id = Integer.parseInt(arguments[1]);
            } catch (NumberFormatException e) {
                return new ExecutionResponse(false, "ID не распознан");
            }

            console.println("* Создание нового Фильма ...");
            Movie cur = Ask.askMovie(console, id);

            if (cur != null && cur.isValid()){
                manager.sendData(new Container(CommandTypes.Update, cur));
                Container container =manager.receiveData();

                return container.getExecutionResponse();
            } else{
                return new ExecutionResponse(false, "Поля Фильма не валидны! Фильм не обновлён");
            }


        } catch (Ask.AskBreak e){
            return new ExecutionResponse(false, "Поля Фильма не валидны! Фильм не обновлён");
        }
    }
}
