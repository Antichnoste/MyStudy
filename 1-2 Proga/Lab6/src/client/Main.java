package client;

import client.command.*;
import client.managers.*;
import client.utility.Runner;
import common.command.CommandTypes;
import common.utillity.StandartConsole;
import client.command.ExecuteScript;

import java.util.HashMap;
import java.util.Map;

public class Main {

    private static StandartConsole console = new StandartConsole();
    private static int PORT = 12345;
    private static String HOST = "localhost";

    public static void main(String[] args) {

        requestHost();
        requestPort();

        Network network = new Network(HOST, PORT);

        Map<CommandTypes, Command> commands = new HashMap<>(){
            {
                put(CommandTypes.Add, new Add(console, network));
                put(CommandTypes.Help, new Help(console, this));
                put(CommandTypes.Exit, new Exit(console));
                put(CommandTypes.Average_of_oscars_count, new AverageOfOscarsCount(console, network));
                put(CommandTypes.Clear, new Clear(console, network));
                put(CommandTypes.Execute_script, new ExecuteScript(console));
                put(CommandTypes.Filter_contains_name, new FilterContainsName(console, network));
                put(CommandTypes.History, new History(console, network));
                put(CommandTypes.Filter_starts_with_tagline, new FilterStartsWithTagline(console, network));
                put(CommandTypes.Info, new Info(console, network));
                put(CommandTypes.Remove_by_id, new RemoveById(console,network ));
                put(CommandTypes.Remove_first, new RemoveFirst(console, network));
                put(CommandTypes.Remove_greater, new RemoveGreater(console, network));
                put(CommandTypes.Show, new Show(console, network));
                put(CommandTypes.Update, new UpdateID(console, network));
            }
        };


        new Runner(network, console, commands).interactiveMode();
    }


    private static void requestPort() {
        console.print("Введите порт: ");

        String reader = console.readln();

        if (reader == null) {
            console.printError("Поле не может быть пусто");
            requestPort();
        }
        if (!isValidPort(reader)) {
            console.printError("Некорректный port");
            requestPort();
        } else {
            PORT = Integer.parseInt(reader);
        }
    }

    private static boolean isValidPort(String stringPort) {
        try {
            int portNumber = Integer.parseInt(stringPort);
            if (portNumber >= 0 && portNumber <= 65535) {
                PORT = portNumber;
                return true;
            } else {
                return false;
            }
        } catch (NumberFormatException e) {
            return false;
        }
    }

    private static void requestHost() {
        console.print("Введите хост: ");
        HOST = console.readln();

        if (HOST == null) {
            console.println("Хост не может быть пуст");
            requestHost();
        }

        if (HOST.equals("localhost")) {
            return;
        }

        if (!isValidIpAddress(HOST)) {
            console.printError("Некорректный host");
            requestHost();
        }
    }

    private static boolean isValidIpAddress(String ip) {
        String ipv4Pattern = "^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$";

        String ipv6Pattern = "^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$";

        return ip.matches(ipv4Pattern) || ip.matches(ipv6Pattern);
    }

}