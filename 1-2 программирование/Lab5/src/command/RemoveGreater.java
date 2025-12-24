package command;

import managers.Ask;
import managers.CollectionManager;
import models.Movie;
import utility.Console;
import utility.ExecutionResponse;

/**
 * Команда, которая удаляет самый все элементы больше введённого
 * compareTo написано по полю oscarsCount
 */
public class RemoveGreater extends Command {
    private final Console console;
    private final CollectionManager manager;

    public RemoveGreater(Console console, CollectionManager manager) {
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

            for (int i = 0; i < manager.getCollection().size(); i++){
                if (manager.getCollection().get(i).compareTo(cur) > 0) {
                    manager.remove(manager.getCollection().get(i).getId());
                    manager.sort();
                    i--;
                }
            }

            return new ExecutionResponse("Из коллекции успешно удалены все фильмы, кол-во Оскаров которых больше " + cur.getOscarsCount() + "!");
        } catch (Ask.AskBreak e){
            return new ExecutionResponse(false, "Поля Фильма не валидны! Команда не сработала");
        }
    }
}
