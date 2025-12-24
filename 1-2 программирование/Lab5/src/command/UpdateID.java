package command;

import managers.Ask;
import managers.CollectionManager;
import models.Movie;
import utility.Console;
import utility.ExecutionResponse;

/**
 * Команда по обновлению элемента в коллекции
 */
public class UpdateID extends Command {
    private final Console console;
    private final CollectionManager manager;

    public UpdateID(Console console, CollectionManager manager) {
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

            Movie old = manager.getById(id);
            if (old == null || !manager.getCollection().contains(old)){
                return new ExecutionResponse(false, "По такому ID не существует фильма!");
            }

            console.println("* Создание нового Фильма ...");
            Movie cur = Ask.askMovie(console, old.getId());

            if (cur != null && cur.isValid()){
                manager.remove(old.getId());
                manager.add(cur);
                manager.sort();
                return new ExecutionResponse("Обновлено!");
            } else{
                return new ExecutionResponse(false, "Поля Фильма не валидны! Фильм не обновлён");
            }


        } catch (Ask.AskBreak e){
            return new ExecutionResponse(false, "Поля Фильма не валидны! Фильм не обновлён");
        }
    }
}
