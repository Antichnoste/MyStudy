package server;

import server.managers.CommandManager;
import server.managers.Network;
import org.apache.logging.log4j.Logger;
import org.apache.logging.log4j.LogManager;
import server.managers.CollectionManager;
import server.managers.DumpManager;
import server.command.*;

import java.net.DatagramSocket;
import java.net.SocketException;
import java.nio.channels.DatagramChannel;

public class Main {
    public static final Logger logger = LogManager.getLogger("Server");

    public static void main(String[] args) {

        String fileName = System.getenv("FILE_NAME");
        if (fileName == null) {
            System.out.println("Переменная окружения FILE_NAME не задана");
            System.exit(1);
        }

        DumpManager dumpManager = new DumpManager(fileName);
        CollectionManager collectionManager = new CollectionManager(dumpManager);

        if (!collectionManager.loadCollection()) {
            logger.info("Не удалось загрузить коллекцию.");
            System.exit(1);
        }
        collectionManager.sort();

        Network network = new Network(12345);

        while(!network.init()){
            logger.error("Пытаюсь подключиться...");
        }


        CommandManager commandManager = new CommandManager() {
            {
                register("add", new Add(collectionManager));
                register("average_of_oscars_count", new AverageOfOscarsCount(collectionManager));
                register("clear", new Clear(collectionManager));
                register("filter_contains_name", new FilterContainsName(collectionManager));
                register("history", new History(this));
                register("filter_starts_with_tagline", new FilterStartsWithTagline(collectionManager));
                register("info", new Info(collectionManager));
                register("remove_by_id", new RemoveById(collectionManager ));
                register("remove_first", new RemoveFirst(collectionManager));
                register("remove_greater", new RemoveGreater(collectionManager));
                register("save", new Save(collectionManager));
                register("show", new Show(collectionManager));
                register("update", new UpdateID(collectionManager));
                register("add_to_history", new AddToHistory(this));
            }
        };

        network.run(commandManager);



        //FILE_NAME=C:\\Users\\karag\\OneDrive\\Рабочий стол\\Прога\\ex.csv
    }
}
