package server.command;

import common.command.Container;
/**
 * Интерфейс для исполняемых команд
 */
public interface Executable {
    Container apply(Container container);
}
