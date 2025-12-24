package models;

public enum Color {
    RED,
    BLACK,
    YELLOW,
    ORANGE,
    BROWN;

    public static String names(){
        StringBuilder names = new StringBuilder();
        for (Color colorType : values()) {
            names.append(colorType.name()).append(", ");
        }
        return names.substring(0, names.length() - 2);
    }
}
