package server.managers;

import common.command.Container;
import common.utillity.ExecutionResponse;
import org.apache.logging.log4j.Logger;
import server.Main;
import server.command.Command;

import java.io.*;
import java.net.*;
import java.nio.ByteBuffer;
import java.nio.channels.DatagramChannel;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;

/**
 * Менеждер сети в Сервере
 */
public class Network {
    private int PORT;
    private static final int BUFFER_SIZE = 10000;

    private DatagramChannel channel;
    private ByteBuffer buffer;

    public static final Logger logger = Main.logger;

    public Network(int port){
        this.PORT = port;
    }

    public Network(){
        this.PORT = 12345;
    }

    public boolean init(){
        try {
            // 1. Открываем канал в неблокирующем режиме
            this.channel = DatagramChannel.open();
            channel.bind(new InetSocketAddress(PORT));
            channel.configureBlocking(false);

            logger.info("Сервер запущен. IP: " + InetAddress.getLocalHost().getHostAddress() +", порт: " + PORT);

            this.buffer = ByteBuffer.allocate(BUFFER_SIZE);
            return true;
        } catch (IOException e) {
            logger.error(e.getMessage());
            return false;
        }

    }

    public void run(CommandManager commandManager){

        try{
            while (true) {
                buffer.clear();
                SocketAddress clientAddress = channel.receive(buffer); // Не блокируется

                if (clientAddress != null) {
                    buffer.flip();
                    Container response = deserialize(buffer.array());
                    //System.out.println("Получено" + response.toString());

                    if (response != null) {
                        Command command = commandManager.getCommands().get(response.getCommandType().Type());

                        if (command == null) {
                            response = new Container(null, new ExecutionResponse(false, "Команда '" + response.getCommandType().Type() + "' не найдена. Наберите 'help' для справки"), null);
                            logger.info("Команда не найдена");
                        } else {
                            logger.info("Команда " + response.getCommandType().Type() + " выполнена!");
                            response = command.apply(response);
                        }

                        buffer.clear();
                        buffer.put(serializer(response));
                        buffer.flip();
                        channel.send(buffer, clientAddress);

                        logger.info("Отправлен ответ серверу!");
                    } else {
                        logger.info("Получен пустая команда!");
                    }
                }

                Thread.sleep(100); // Чтобы не грузить CPU
            }
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }


//        try{
//            while(true){
//                selector.select(); // Ждём событий
//                for (SelectionKey key : selector.selectedKeys()) {
//                    if (key.isReadable()) {
//                        buffer.clear();
//                        InetSocketAddress clientAddress = (InetSocketAddress) channel.receive(buffer);
//
//                        if (clientAddress != null) {
//                            buffer.flip();
//                            Container response = deserialize(buffer.array());
//
//                            if (response != null) {
//                                Command command = commandManager.getCommands().get(response.getCommandType().Type());
//
//                                if (command == null) {
//                                    response = new Container(null, new ExecutionResponse(false, "Команда '" + response.getCommandType().Type() + "' не найдена. Наберите 'help' для справки"), null);
//                                    logger.info("Команда не найдена");
//                                } else {
//                                    logger.info("Команда " + response.getCommandType().Type() + " выполнена!");
//                                    response = command.apply(response);
//                                }
//
//                                buffer.clear();
//                                buffer.put(serializer(response));
//                                buffer.flip();
//                                channel.send(buffer, clientAddress);
//
//                                logger.info("Отправлен ответ серверу!");
//                            }
//                        }
//                    }
//                }
//                selector.selectedKeys().clear(); // Очищаем обработанные события
//            }
//        } catch (IOException e) {
//            logger.error(e.getMessage());
//        }
    }

    public byte[] serializer(Container response ){
        try {
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            ObjectOutputStream oos = new ObjectOutputStream(baos);
            oos.writeObject(response);
            oos.flush();
            oos.close();

            logger.info("Ответ успешно сериализован!");
            return baos.toByteArray();
        }
        catch (IOException e) {
            return null;
        }
    }

    public Container deserialize(byte[] bytes){
        if (bytes == null || bytes.length == 0) {
            return null;
        }

        InputStream is = new ByteArrayInputStream(bytes);

        try (ObjectInputStream ois = new ObjectInputStream(is)) {
            logger.info("Команда успешно десериализована!");
            return (Container) ois.readObject();
        } catch (IOException e) {
            logger.error("Не удалось десереализовать объект");
            return null;
        } catch (ClassNotFoundException e) {
            logger.error("Не удалось десереализовать объект");
            return null;
        }
    }

}
