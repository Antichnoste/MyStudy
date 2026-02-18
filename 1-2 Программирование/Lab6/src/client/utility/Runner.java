package client.utility;

import client.command.Command;
import client.command.ExecuteScript;
import client.command.Exit;
import client.managers.Network;
import common.command.CommandTypes;
import common.command.Container;
import common.utillity.Console;
import common.utillity.ExecutionResponse;

import java.io.File;
import java.io.FileNotFoundException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

/**
 * Класс исполениния программы
 */
public class Runner {
    private Console console;
    private final Map<CommandTypes, Command> commands;
    private final List<String> scriptStack = new ArrayList<>();
    private Network network;
    private int lengthRecursion = -1;


    public Runner(Network network, Console console, Map<CommandTypes, Command> commands) {
        this.network = network;
        this.console = console;
        this.commands = commands;
    }

    /**
     * Интерактивный режим
     */
    public void interactiveMode(){
        try{
            ExecutionResponse commandStatus;
            String[] userCommand = {"", ""};

            console.println("Добро пожаловать!\nВведите help для вывода доступных команд");

            while(true){
                console.prompt();
                userCommand = (console.readln().trim() + " ").split(" ",2);
                userCommand[1] = userCommand[1].trim();

                if (!userCommand[0].isEmpty()){
                    network.sendData(new Container(CommandTypes.Add_to_history, null, userCommand[0]));
                    network.receiveData(); // Это нужно чтобы освободить канал
                }

                commandStatus = launchCommand(userCommand);

                if (commandStatus.getMessage().equals(Exit.Key4exit.toString())){
                    console.print(commandStatus.getMessage());
                    break;
                }
                console.println(commandStatus.getMessage());

            }
        } catch (NoSuchElementException e){
            console.printError("Пользовательский ввод не обнаружен");
        } catch (IllegalStateException e){
            console.printError("Непредвиденная ошибка");
        }
    }

    /**
     * Функция загрузки команды
     * @param userCommand загружаемая команда
     * @return результат об успешности
     */
    private ExecutionResponse launchCommand(String[] userCommand){
        if(userCommand[0].isEmpty()){
            return new ExecutionResponse(false, "Команда '" + userCommand[0] + "' не найден. Введите 'help' для справки");
        }

        CommandTypes commandType = CommandTypes.getByString(userCommand[0]);
        Command command = commands.get(commandType);

        if (!commands.containsKey(commandType)){
            return new ExecutionResponse(false, "Команда '" + userCommand[0] + "' не найден. Введите 'help' для справки");
        }

        switch (userCommand[0]){
            case "execute_script" -> {
                ExecutionResponse tmp = new ExecuteScript(console).apply(userCommand);
                if (!tmp.getExitCode()){
                    return tmp;
                }
                ExecutionResponse tmp2 = scriptMode(userCommand[1]);
                return new ExecutionResponse(tmp2.getExitCode(), tmp.getMessage() + "\n" + tmp2.getMessage().trim());
            }
            default -> {
                return command.apply(userCommand);
            }
        }
    }

    /**
     * Запуск скрипта
     * @param argument имя файла
     * @return сообщение об успешности
     */
    private ExecutionResponse scriptMode(String argument) {
        String[] userCommand = {"", ""};
        StringBuilder executionOutput = new StringBuilder();

        if (!new File(argument).exists()) return new ExecutionResponse(false, "Файл не существует!");
        if (!Files.isReadable(Paths.get(argument))) return new ExecutionResponse(false, "Прав для чтения нет!");

        scriptStack.add(argument);
        try (Scanner scriptScanner = new Scanner(new File(argument))) {

            ExecutionResponse commandStatus;

            if (!scriptScanner.hasNext()) throw new NoSuchElementException();
            console.selectFileScanner(scriptScanner);
            do {
                userCommand = (console.readln().trim() + " ").split(" ", 2);
                userCommand[1] = userCommand[1].trim();
                while (console.isCanReadln() && userCommand[0].isEmpty()) {
                    userCommand = (console.readln().trim() + " ").split(" ", 2);
                    userCommand[1] = userCommand[1].trim();
                }
                executionOutput.append(console.getPrompt() + String.join(" ", userCommand) + "\n");

                boolean needLaunch = true;
                if (userCommand[0].equals("execute_script")) {
                    needLaunch = checkRecursion(userCommand[1], scriptScanner);
                }

                commandStatus = needLaunch ? launchCommand(userCommand) : new ExecutionResponse("Была замечена рекурсия. Выхожу из режима выполнения скрипта...");

                if (userCommand[0].equals("execute_script")) {
                    console.selectFileScanner(scriptScanner);
                }

                executionOutput.append(commandStatus.getMessage()+"\n");
            } while (commandStatus.getExitCode() && !commandStatus.getMessage().equals(Exit.Key4exit.toString()) && console.isCanReadln());

            console.selectConsoleScanner();
            if (!commandStatus.getExitCode() && !(userCommand[0].equals("execute_script") && !userCommand[1].isEmpty())) {
                executionOutput.append("Проверьте скрипт на корректность введенных данных!\n");
            }

            return new ExecutionResponse(commandStatus.getExitCode(), executionOutput.toString());
        } catch (FileNotFoundException exception) {
            return new ExecutionResponse(false, "Файл со скриптом не найден!");
        } catch (NoSuchElementException exception) {
            return new ExecutionResponse(false, "Файл со скриптом пуст!");
        } catch (IllegalStateException exception) {
            console.printError("Непредвиденная ошибка!");
            System.exit(0);
        } finally {
            scriptStack.remove(scriptStack.size() - 1);
        }
        return new ExecutionResponse("");
    }

    /**
     * Функция проверки скрипта на рекурсию
     *
     * @param args имя запускаемого скрипта
     * @param scriptScanner сканер скрипта
     * @return True если скрипт можно запускать
     */
    private boolean checkRecursion(String args, Scanner scriptScanner){

        for (String script : scriptStack){
            if (args.equals(script)){
                return false;
            }
        }
        return true;
    }
}
