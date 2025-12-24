package server.managers;

import au.com.bytecode.opencsv.CSVReader;
import au.com.bytecode.opencsv.CSVWriter;

import common.models.*;
import org.apache.logging.log4j.Logger;
import server.Main;

import java.io.*;
import java.nio.file.AccessDeniedException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Collection;
import java.util.LinkedList;
import java.util.Scanner;

/**
 * Класс файлового менеджера по сериализации/десереализации из коллекции в CSV
 */
public class DumpManager {
    private static final long serialVersionUID = 4L;
    public static final Logger logger = Main.logger;

    private final String fileName;

    public DumpManager(String fileName) {
        this.fileName = fileName;
    }

    /**
     * Переводит массив объектов класса Movie в CSV-строку
     * @param collection массив объектов класса Movie
     * @return строка
     */
    private String collection2CSV(Collection <Movie> collection){
        try{
            StringWriter sw = new StringWriter();
            CSVWriter writer = new CSVWriter(sw, ';');
            for (Movie movie: collection){
                writer.writeNext(Movie.toArray(movie));
            }
            String csv = sw.toString();
            return csv;
        } catch (Exception e){
            //console.printError("Ошибка сериализации");
            logger.error("Ошибка сериализации", e);
            return null;
        }
    }

    /**
     * Записывает массив объектов класса Movie в CSV-файл
     * @param collection массив объектов класса Movie
     */
    public void writeCollection(Collection <Movie> collection){
        OutputStreamWriter writer = null;
        try{
            String csv = collection2CSV(collection);
            if (csv == null) return;
            writer = new OutputStreamWriter(new FileOutputStream(fileName));
            try{
                writer.write(csv);
                writer.flush();
                //console.println("Коллекция успешно сохранена в файл!");
                logger.info("Коллекция успешно сохранена в файл!");
            } catch (IOException e) {
                //console.printError("Ошибка сохранения");
                logger.error("Ошибка сохранения",e);
            }
        } catch (FileNotFoundException e) {
            //console.printError("Файл не найден\nУкажите корректный путь в FILE_NAME");
            logger.error("Файл не найден\nУкажите корректный путь в FILE_NAME", e);
            System.exit(1);
        } finally {
            try {
                writer.close();
            } catch (IOException e) {
                //console.printError("Ошибка закрытия файла");
                logger.error("Ошибка закрытия файла",e);
            }
        }
    }

    /**
     * Переводит CSV-строку в коллекцию
     * @param s строка
     * @return CSV-строка
     */
    private LinkedList<Movie> CSV2collection (String s){
        try{
            StringReader sr = new StringReader(s);
            CSVReader reader = new CSVReader(sr, ';');
            LinkedList<Movie> collection = new LinkedList<>();
            String[] record;

            while((record = reader.readNext()) != null){
                Movie movie = Movie.fromArray(record);
                if (movie.isValid()){
                    collection.add(movie);
                } else {
                    //console.printError("Файл содержит некорректные данные");
                    logger.error("Файл содержит некорректные данные");
                }
            }

            reader.close();
            return collection;
        } catch (IOException e) {
            //console.println("Ошибка десериализации");
            logger.error("Ошибка десериализации", e);
            return null;
        }
    }

    /**
     * Функция чтения из файла
     * @param collection коллекция, в которую будут записаны данные файла
     */
    public void readCollection(Collection <Movie> collection){

        if (fileName != null && !fileName.isEmpty()){


            try (Scanner fileReader = new Scanner(new File(fileName))) {
                StringBuilder s = new StringBuilder();

                while (fileReader.hasNextLine()){
                    s.append(fileReader.nextLine());
                    s.append("\n");
                }
                collection.clear();

                for (Movie e : CSV2collection(s.toString())){
                    collection.add(e);
                }

                if (!collection.isEmpty()){
                    logger.info("----------------------------------------");
                    logger.info("Файл успешно считан, коллекция загружена");
                    logger.info("----------------------------------------");
                    return;
                } else {
                    logger.error("--------------------------------------------------------");
                    logger.error("В загрузочном файле не обнаружена необходимая коллекция!");
                    logger.error("--------------------------------------------------------");
                }
            } catch (FileNotFoundException e) {
                if (new File(fileName).exists()){
                    logger.error("-----------------------");
                    logger.error("Ошибка доступа к файлу");
                    logger.error("-----------------------");
                } else {
                    logger.error("-----------------------");
                    logger.error("Ошибка нахождения файла");
                    logger.error("-----------------------");
                }
            } catch (IllegalStateException e){
                logger.error("--------------------------");
                logger.error("Неправильный формат данных");
                logger.error("--------------------------");
                System.exit(0);
            }
        } else {
            logger.error("-----------------------------------------------------");
            logger.error("Переменная окружения с загрузочным файлом не найдена!");
            logger.error("-----------------------------------------------------");
        }
    }
}
