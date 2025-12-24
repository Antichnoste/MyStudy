package server.command;

import common.command.Container;
import common.models.Movie;
import common.utillity.ExecutionResponse;
import server.managers.CollectionManager;

public class Add extends Command {
    private final CollectionManager manager;

    public Add(CollectionManager manager) {
        super("add {element}", "добавить новый элемент в коллекцию");
        this.manager = manager;
    }

    /**
     * Исполнение командны
     *
     * @param container объек который надо добавить
     * @return возвращает результат о выполнении команды
     */
    @Override
    public Container apply(Container container) {
        Movie movie = (Movie) container.getObj();

        movie.setId(manager.getFreeId());
        manager.add(movie);

        return new Container(new ExecutionResponse("Фильм успешно создан!"));
    }
}
