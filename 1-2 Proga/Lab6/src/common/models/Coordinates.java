package common.models;

import common.utillity.Validatable;

import java.io.Serializable;
import java.util.Objects;

/**
 * Класс координат
 */
public class Coordinates implements Validatable, Serializable {
    private static final long serialVersionUID = 6L;
    private Double x; //Поле не может быть null
    private double y; //Значение поля должно быть больше -708

    private final Double MIN_VALUE_Y = -708.0; // Не включительно

    /** Конструктор
     *
     * @param x координата x
     * @param y координата y
     */
    public Coordinates(Double x, double y) {
        this.x = x;
        this.y = y;
    }

    /**
     * Конструктор по строке
     *
     * @param s строка, по которой будет создан объект
     */
    public Coordinates(String s) {
        try{
            try{
                x = Double.parseDouble(s.split(";")[0]);
            } catch (NumberFormatException e) {}
            try{
                x = Double.parseDouble(s.split(";")[1]);
            } catch (NumberFormatException e){}

        } catch (ArrayIndexOutOfBoundsException e){}
    }

    public Double getX() {
        return x;
    }

    public void setX(Double x) {
        this.x = x;
    }

    public Double getY() {
        return y;
    }

    public void setY(Double y) {
        this.y = y;
    }

    @Override
    public boolean isValid() {
        if ((x == null) || (y <= MIN_VALUE_Y)) return false;
        return true;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Coordinates that = (Coordinates) o;
        return Double.compare(y, that.y) == 0 && Objects.equals(x, that.x);
    }

    @Override
    public int hashCode() {
        return Objects.hash(x, y);
    }

    @Override
    public String toString() {
        return x + ";" + y;
    }
}
