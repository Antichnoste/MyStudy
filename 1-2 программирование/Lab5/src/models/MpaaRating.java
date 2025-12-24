package models;

public enum MpaaRating {
    G,
    PG,
    NC_17;

    public static String names(){
        StringBuilder names = new StringBuilder();
        for (MpaaRating colorType : values()) {
            names.append(colorType.name()).append(", ");
        }
        return names.substring(0, names.length() - 2);
    }
}
