package command;

import managers.CollectionManager;
import utility.Console;
import utility.ExecutionResponse;

import java.time.LocalDateTime;

public class Info  extends Command {
    private final Console console;
    private final CollectionManager manager;

    /**
     * Конструктор
     * @param console консоль
     * @param manager менеджер коллекции
     */
    public Info(Console console, CollectionManager manager) {
        super("info", "вывести в стандартный поток вывода информацию о коллекции (тип, дата инициализации, количество элементов и т.д.)");
        this.console = console;
        this.manager = manager;
    }

    /**
     * Исполнение команды
     * @param arguments массив с аргументами
     * @return возвращает результат выполнения команды
     */
    @Override
    public ExecutionResponse apply(String[] arguments) {
        if (!arguments[1].isEmpty()) {
            return new ExecutionResponse(false, "Неправильное кол-во аргументов \nИспользование: '" + getName() + "'");
        }

        LocalDateTime lastInitTime = manager.getLastInitTime();
        String lastInitTimeString = (lastInitTime == null) ? "в данной сессии инициализации еще не происходило" :
                lastInitTime.toLocalDate().toString() + " " + lastInitTime.toLocalTime().toString();

        LocalDateTime lastSaveTime = manager.getLastSaveTime();
        String lastSaveTimeString = (lastSaveTime == null) ? "в данной сессии сохранения еще не происходило" :
                lastSaveTime.toLocalDate().toString() + " " + lastSaveTime.toLocalTime().toString();

        String s="Сведения о коллекции:\n";
        s+=" Тип: " + manager.getCollection().getClass().toString()+"\n";
        s+=" Количество элементов: " + manager.getCollection().size()+"\n";
        s+=" Дата последнего сохранения: " + lastSaveTimeString+"\n";
        s+=" Дата последней инициализации: " + lastInitTimeString;
        return new ExecutionResponse(s);
    }
}
