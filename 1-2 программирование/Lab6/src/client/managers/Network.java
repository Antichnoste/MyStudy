package client.managers;

import common.command.Container;
import common.utillity.ExecutionResponse;

import java.io.*;
import java.net.*;
import java.nio.ByteBuffer;
import java.nio.channels.DatagramChannel;


/**
 * Менеджер сети в Клиенте
 */

public class Network { ;
    private static String SERVER_HOST = "localhost";
    private static int SERVER_PORT = 12345;
    private static final int BUFFER_SIZE = 10000;
    private static final int WAIT_TIME_MC = 3000;

    private DatagramChannel channel;
    private InetSocketAddress serverAddress;
    private ByteBuffer buffer;

    public Network (String host, int port){
        try{
            this.channel = DatagramChannel.open();
            this.channel.configureBlocking(false);
            this.serverAddress = new InetSocketAddress(host, port);
            this.buffer = ByteBuffer.allocate(BUFFER_SIZE);
        } catch (UnknownHostException e) {
            System.out.println("Unknown host: " + e.getMessage());
        } catch (SocketException e) {
            System.out.println("Socket exception: " + e.getMessage());
        } catch (IOException e) {
            System.out.println("IO exception: " + e.getMessage());
        }
    }

    public Network (){
        try{
            this.channel = DatagramChannel.open();
            this.channel.configureBlocking(false);
            this.serverAddress = new InetSocketAddress("localhost", 12345);
            this.buffer = ByteBuffer.allocate(BUFFER_SIZE);
        } catch (UnknownHostException e) {
            System.out.println("Unknown host: " + e.getMessage());
        } catch (SocketException e) {
            System.out.println("Socket exception: " + e.getMessage());
        } catch (IOException e) {
            System.out.println("IO exception: " + e.getMessage());
        }
    }

    public ExecutionResponse sendData(Container container) {
        try {
            buffer.clear();
            buffer.put(serializer(container));
            buffer.flip();
            channel.send(buffer, serverAddress);
            return new ExecutionResponse("");

        } catch (UnknownHostException e) {
            return new ExecutionResponse(false, "Unknown host: " + e.getMessage());
        } catch (IOException e) {
            return new ExecutionResponse(false, "I/O exception: " + e.getMessage());
        }
    }

    public static byte[] serializer(Object obj) {
        try {
            ByteArrayOutputStream bos = new ByteArrayOutputStream();
            ObjectOutputStream oos = new ObjectOutputStream(bos);
            oos.writeObject(obj);
            oos.close();
            byte[] objBytes = bos.toByteArray();
            return objBytes;
        } catch (IOException e) {
            return null;
        }
    }

    public static Container deserialize(byte[] bytes) {
        if (bytes == null) return new Container(null, new ExecutionResponse(false, "Ответ от сервера не получен, выполнение отменено!"));
        InputStream is = new ByteArrayInputStream(bytes);
        try (ObjectInputStream ois = new ObjectInputStream(is)) {
            return (Container) ois.readObject();
        } catch (IOException | ClassNotFoundException e) {
            throw new RuntimeException(e);
        }
    }

    public Container receiveData() {

        try {
            buffer.clear();
            long startTime = System.currentTimeMillis();

            while (System.currentTimeMillis() - startTime < WAIT_TIME_MC){
                InetSocketAddress sender = (InetSocketAddress) channel.receive(buffer);
                if (sender != null) {
                    buffer.flip();
                    byte[] receivedData = new byte[buffer.remaining()];
                    buffer.get(receivedData);
                    //System.out.println("Получено " + receivedData.length + " байт");
                    return deserialize(receivedData);
                }
            }
            return new Container(new ExecutionResponse(false,"Сервер не отвечает"));
        } catch (IOException e) {
            System.out.println("IO exception: " + e.getMessage());
        }
        return new Container(new ExecutionResponse(false, "Сервер не отвечает"));
    }
}

