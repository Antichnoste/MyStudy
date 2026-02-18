package client.command;

import common.utillity.Console;
import common.utillity.ExecutionResponse;

/**
 * Команда для выхода из интерактивного режима без сохранения
 */
public class Exit extends Command {
    private Console console;
    public static StringBuilder Key4exit = new StringBuilder();

    static {
        Key4exit.append("""
                  ╱|、 \s
                 (˚ˎ 。7   "Прощай, жестокий мир!" \s
                 |、˜〵    \s
                 じしˍ,)ノ \s
                """);
    }
//          sb.append("""
//                      ✧   /\\_/\\   ✧ \s
//                     ✦  ( ≖‿≖ )  ✦ \s
//                    ✧~~/ ︶︶  \\~~✧ \s
//                      /   ︶   \\ \s
//                     / ︶    ︶  \\ \s
//                    ✧¯¯¯¯¯¯¯¯¯¯✧ \s
//                  "Спокойной ночи, кодёр!"
//
//                """);

    /**
     * Конструктор
     * @param console консоль
     */
    public Exit(Console console) {
        super("exit","завершить программу (без сохранения в файл)");
        this.console = console;
    }

    /**
     * Выполнение команды
     * @param arguments массив с аргументами
     * @return результат выполения команды
     */
    public ExecutionResponse apply(String[] arguments) {
        if (!arguments[1].isEmpty()) {
            return new ExecutionResponse(false, "Неправильное кол-во аргументов \nИспользование: '" + getName() + "'");
        }


        return new ExecutionResponse(Key4exit.toString());
    }
}
