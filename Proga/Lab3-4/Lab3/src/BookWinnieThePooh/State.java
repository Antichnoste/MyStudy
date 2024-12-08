package BookWinnieThePooh;

public enum State {
    Default("ничего"),
    Fear("страх"),
    Joy("радость"),
    Surprise("удивление");

    private final String description;

    State(String description) {
        this.description = description;
    }

    public String getDescription() {
        return description;
    }
}
