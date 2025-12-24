package common.models;

import java.io.Serializable;

public enum MpaaRating implements Serializable {
    G,
    PG,
    NC_17;

    private static final long serialVersionUID = 9L;

    public static String names(){
        StringBuilder names = new StringBuilder();
        for (MpaaRating colorType : values()) {
            names.append(colorType.name()).append(", ");
        }
        return names.substring(0, names.length() - 2);
    }
}
