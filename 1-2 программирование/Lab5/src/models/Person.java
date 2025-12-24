package models;

import utility.Validatable;

import java.util.Objects;

public class Person implements Validatable {
    private String name; //Поле не может быть null, Строка не может быть пустой
    private Float height; //Поле может быть null, Значение поля должно быть больше 0
    private Float weight; //Поле не может быть null, Значение поля должно быть больше 0
    private Color eyeColor; //Поле может быть null

    private final float MIN_VALUE_HEIGHT = 0; // Значение должно быть строго больше MIN_VALUE_HEIGHT
    private final float MIN_VALUE_WEIGHT = 0; // Значение должно быть строго больше MIN_VALUE_WEIGHT

    /**
     * Конструктор класс Person
     * @param name имя
     * @param height рост
     * @param weight вес
     * @param eyeColor цвет глаз
     */
    public Person(String name, Float height, Float weight, Color eyeColor) {
        this.name = name;
        this.height = height;
        this.weight = weight;
        this.eyeColor = eyeColor;
    }

    /**
     * Конструктор класс Person по строке, формат которой должен задаваться как в команде Person.toString()
     * @param s строка по которой будет создан объект класса Person
     */
    public Person (String s){
        try{
            this.name = s.split(" ; ")[0];

            try{
                this.height = Float.parseFloat(s.split(" ; ")[1]);
            } catch (NumberFormatException e){
                this.height = null;
            }

            try{
                this.weight = Float.parseFloat(s.split(" ; ")[2]);
            } catch (NumberFormatException e){
                return;
            }

            try{
                eyeColor = Color.valueOf(s.split(" ; ")[3]);
            } catch (NullPointerException | IllegalArgumentException e){
                eyeColor = null;
            }
        } catch (ArrayIndexOutOfBoundsException e){}
    }

    @Override
    public boolean isValid() {
        if (name == null || name.isEmpty()) return false;
        if (height == null || height <= MIN_VALUE_HEIGHT) return false;
        if (weight == null || weight <= MIN_VALUE_WEIGHT) return false;
        return eyeColor != null;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Float getHeight() {
        return height;
    }

    public void setHeight(Float height) {
        this.height = height;
    }

    public Float getWeight() {
        return weight;
    }

    public void setWeight(Float weight) {
        this.weight = weight;
    }

    public Color getEyeColor() {
        return eyeColor;
    }

    public void setEyeColor(Color eyeColor) {
        this.eyeColor = eyeColor;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Person person = (Person) o;
        return name.equals(person.name) && height.equals(person.height) && weight.equals(person.weight) && eyeColor.equals(person.eyeColor);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name, height, weight, eyeColor);
    }

    @Override
    public String toString() {
        return name + " ; " + height + " ; " + weight + " ; " + (eyeColor == null ? "null" : eyeColor);
    }
}
