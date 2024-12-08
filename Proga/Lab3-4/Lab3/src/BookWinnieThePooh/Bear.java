package BookWinnieThePooh;

public class Bear extends Animal{
    private Location location;
    private State state;
    private boolean AbilitySpeak = false;
    private int age;

    public Bear() throws InvalidAge{
        super("noname", new Location("где-то"), State.Default, -1);
    }

    public Bear(String name, int age) throws InvalidAge {
        super(name, new Location("где-то"), State.Default, age);

        if (age < 0 || age > 30){
            throw new InvalidAge("Медведи столько не живут, перезадайте возраст медведю!");
        }
    }

    public Bear(String name){
        super(name, new Location("где-то"), State.Default,-1);
    }

    public Bear(String name, Location location){
        super(name, location , State.Default, -1);
    }

    public Bear(String name, Location location, State state, int age) throws InvalidAge{
        super(name, location, state,age);
        this.AbilitySpeak = false;

        if (age < 0 || age > 30){
            throw new InvalidAge("Медведи столько не живут, перезадайте возраст медведю!");
        }
    }

    @Override
    public void setAge(int age) throws InvalidAge {
        // Должно быть от 0 до 30
        if (age < 0 || age > 30){
            throw new InvalidAge("Медведи столько не живут");
        }
        else {
            this.age = age;
        }
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Bear bear = (Bear) obj;
        return getName() == bear.getName();
    }

    @Override
    public String toString() {
        return "Медведь " + getName();
    }
}
