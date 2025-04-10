package server.command;

import common.command.Container;
import common.utillity.ExecutionResponse;
import server.managers.CollectionManager;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Optional;

public class Info  extends Command {
    private final CollectionManager manager;

    public Info(CollectionManager manager) {
        super("info", "вывести в стандартный поток вывода информацию о коллекции (тип, дата инициализации, количество элементов и т.д.)");
        this.manager = manager;
    }

    @Override
    public Container apply(Container container) {

        String s = String.format(
                "Сведения о коллекции:%n" +
                        " Тип: %s%n" +
                        " Количество элементов: %d%n" +
                        " Дата последнего сохранения: %s%n" +
                        " Дата последней инициализации: %s",
                manager.getCollection().getClass(),
                manager.getCollection().size(),
                Optional.ofNullable(manager.getLastSaveTime())
                        .map(dt -> dt.format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")))
                        .orElse("в данной сессии сохранения еще не происходило"),
                Optional.ofNullable(manager.getLastInitTime())
                        .map(dt -> dt.format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")))
                        .orElse("в данной сессии инициализации еще не происходило")
        );

        return new Container(new ExecutionResponse(s));
    }
}
