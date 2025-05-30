package client.command;

import common.utillity.ExecutionResponse;

/**
 * Интерфейс для исполняемых команд
 */
public interface Executable {
    /**
     * Исполнение команды
     * @param arguments массив с аргументами
     * @return возвращает результат о выполнении команды
     */
    ExecutionResponse apply(String[] arguments);
}
