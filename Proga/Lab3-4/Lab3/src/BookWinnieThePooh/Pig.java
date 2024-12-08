package BookWinnieThePooh;

public class Pig extends Animal{
    private Location location;
    private State state;
    private boolean AbilitySpeak = false;
    private int age;

    public Pig() {
        super("noname", new Location("где-то"), State.Default, -1);
    }

    public Pig(String name, int age){
        super(name, new Location("где-то"), State.Default, age);
    }

    public Pig(String name) {
        super(name, new Location("где-то"), State.Default,-1);
    }

    public Pig(String name, Location location) {
        super(name, location , State.Default, -1);
    }

    public Pig(String name, Location location, State state, int age) {
        super(name, location, state,age);
        this.AbilitySpeak = false;
    }

    @Override
    public void setAge(int age) throws InvalidAge{
        // Должно быть от 0 до 20
        if (age < 0 || age > 20){
            throw new InvalidAge("Свиньи столько не живут");
        }
        else {
            this.age = age;
        }
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Pig pig = (Pig) obj;
        return getName() == pig.getName();
    }

    @Override
    public String toString() {
        return "Поросёнок " + getName();
    }
}
