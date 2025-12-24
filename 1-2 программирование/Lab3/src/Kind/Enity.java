package Kind;

public abstract class Enity {
    private String name;

    public Enity(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }

    public abstract void getInfo();
}
