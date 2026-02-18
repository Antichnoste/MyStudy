package common.models;

import java.io.Serializable;

public enum MovieGenre implements Serializable {
    WESTERN,
    TRAGEDY,
    FANTASY;

    private static final long serialVersionUID = 8L;

    public static String names(){
        StringBuilder names = new StringBuilder();
        for (MovieGenre colorType : values()) {
            names.append(colorType.name()).append(", ");
        }
        return names.substring(0, names.length() - 2);
    }
}
