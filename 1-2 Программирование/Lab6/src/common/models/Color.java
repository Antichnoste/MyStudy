package common.models;

import java.io.Serializable;

public enum Color implements Serializable {
    RED,
    BLACK,
    YELLOW,
    ORANGE,
    BROWN;

    private static final long serialVersionUID = 5L;

    public static String names(){
        StringBuilder names = new StringBuilder();
        for (Color colorType : values()) {
            names.append(colorType.name()).append(", ");
        }
        return names.substring(0, names.length() - 2);
    }
}
