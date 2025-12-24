package models;

public enum MovieGenre {
    WESTERN,
    TRAGEDY,
    FANTASY;

    public static String names(){
        StringBuilder names = new StringBuilder();
        for (MovieGenre colorType : values()) {
            names.append(colorType.name()).append(", ");
        }
        return names.substring(0, names.length() - 2);
    }
}
