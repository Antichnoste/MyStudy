package server.command;

import common.command.Container;
import common.utillity.ExecutionResponse;
import server.managers.CommandManager;

public class History extends Command {
    private final CommandManager manager;

    public History(CommandManager manager) {
        super("history", "вывести последние 15 команд (без их аргументов)");
        this.manager = manager;
    }

    @Override
    public Container apply(Container container) {

        StringBuilder commandsHistory = new StringBuilder();

        manager.getCommandHistory().stream()
                .skip(Math.max(0, manager.getCommandHistory().size() - 15))
                .forEach(command -> commandsHistory.append(" ").append(command).append("\n"));

//        if (manager.getCommandHistory().size() < 15){
//            for (String command : manager.getCommandHistory()){
//                commandsHistory.append(" ").append(command).append("\n");
//            }
//        } else {
//            for (int i = manager.getCommandHistory().size()-15; i < manager.getCommandHistory().size(); i++) {
//                commandsHistory.append(" ").append(manager.getCommandHistory().get(i)).append("\n");
//            }
//        }


        return new Container( new ExecutionResponse(commandsHistory.toString()));

    }
}
