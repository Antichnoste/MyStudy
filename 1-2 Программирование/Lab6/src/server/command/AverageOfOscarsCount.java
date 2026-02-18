package server.command;

import common.command.Container;
import common.models.Movie;
import common.utillity.ExecutionResponse;
import server.managers.CollectionManager;

import java.util.Objects;

/**
 * Команды для подсчёта среднего кол-ва Оскаров в коллекции
 */
public class AverageOfOscarsCount extends Command {
    private final CollectionManager manager;

    public AverageOfOscarsCount(CollectionManager manager) {
        super("average_of_oscars_count", "вывести среднее значение поля oscarsCount для всех элементов коллекции");
        this.manager = manager;
    }

    @Override
    public Container apply(Container container) {

        if (manager.getCollection().isEmpty()){
            return new Container(null, new ExecutionResponse(false, "Коллекция пуста!"), null);
        }

        int CountOfMovie = manager.getCollection().size();

        float sumOfOscars = manager.getCollection().stream()
                .filter(Objects::nonNull)  // фильтрация null значений
                .mapToInt(Movie::getOscarsCount)
                .sum();

        return new Container(null, new ExecutionResponse("Среднее кол-во Оскаров в коллекции: " + Float.toString(sumOfOscars / CountOfMovie)), null);

    }
}
