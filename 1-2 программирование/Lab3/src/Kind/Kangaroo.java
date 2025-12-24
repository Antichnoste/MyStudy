package Kind;

import Exceptions.InvalidAge;
import Record.Location;
import Enum.State;

public class Kangaroo extends Animal {
    private Location location;
    private State state;
    private boolean AbilitySpeak = false;
    private int age;

    public Kangaroo() {
        super("noname", new Location("где-то"), State.Default, -1);
    }

    public Kangaroo(String name, int age) throws InvalidAge {
        super(name, new Location("где-то"), State.Default, age);

        if (age < 0 || age > 25){
            throw new InvalidAge("Кенгуру столько не живут");
        }
    }

    public Kangaroo(String name) {
        super(name, new Location("где-то"), State.Default,-1);
    }

    public Kangaroo(String name, Location location) {
        super(name, location , State.Default, -1);
    }

    public Kangaroo(String name, Location location, State state, int age) throws InvalidAge{
        super(name, location, state,age);
        this.AbilitySpeak = false;

        if (age < 0 || age > 25){
            throw new InvalidAge("Кенгуру столько не живут");
        }
    }

    @Override
    public void setAge(int age) throws InvalidAge{
        // Должно быть от 0 до 25
        if (age < 0 || age > 25){
            throw new InvalidAge("Кенгуру столько не живут");
        }
        else {
            this.age = age;
        }
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Kangaroo kangaroo = (Kangaroo) obj;
        return getName() == kangaroo.getName();
    }

    @Override
    public String toString() {
        return "Кенгуру " + getName();
    }
}
