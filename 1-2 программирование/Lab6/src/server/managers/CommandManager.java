package server.managers;

import server.command.Command;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Класс менеджера коллекции
 */
public class CommandManager implements Serializable {
    /**
     * Словарь для хранения команд и их названий
     */
    private final Map<String, Command> commands = new LinkedHashMap<>();
    private final List<String> commandHistory = new ArrayList<>();

    /**
     * Функия получения всех добеленных команд
     * @return команды, хранящиеся в менеджере
     */
    public Map<String, Command> getCommands() {
        return commands;
    }

    /**
     * @return историю команд
     */
    public List<String> getCommandHistory() {
        return commandHistory;
    }

    /**
     * Добовляет команды в историю
     * @param command команда
     */
    public void addToHistory(String command) {
        commandHistory.add(command);
    }

    /**
     * Функция регистрации команды в менеджере команд
     *
     * @param commandName
     * @param command
     */
    public void register(String commandName, Command command) {
        commands.put(commandName, command);
    }

}
