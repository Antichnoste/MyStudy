package BookWinnieThePooh;

public class Animal extends Enity implements Eating, Speaking, Thinking, Walking {
    private Location location;
    private State state;
    private boolean AbilitySpeak = false;
    private int age;

    public Animal(){
        this("noname", new Location("где-то"), State.Default, -1);
    }

    public  Animal(String name, int age){
        this(name, new Location("где-то"), State.Default, age);
    }

    public Animal(String name){
        this(name, new Location("где-то"), State.Default,-1);
    }

    public Animal(String name, Location location){
        this(name, location , State.Default, -1);
    }

    public Animal(String name, Location location, State state, int age){
        super(name);
        this.location = location;
        this.state = state;
        this.AbilitySpeak = false;
        this.age = age;
    }

    public void FeelEmotion(){
        System.out.println("испытывает" + state.getDescription());
    }

    @Override
    public void eat(String food, Mealtimes time) {
        System.out.println(getName() + " кушает "  + food + " на " + time.getDescription());
    }

    @Override
    public void speak(String speech) {
        if (isAbilitySpeak()){
            System.out.println(getName() + " может говорить, так как уже обдумал : " + speech);
        } else{
            System.out.println(getName() + " ничего не говорит, потому что не о чем не думает ");
        }
    }

    @Override
    public void think(String thoughts) {
        AbilitySpeak = !thoughts.isEmpty();

        if (AbilitySpeak){
            System.out.println(getName() + " думает " + thoughts);
        } else {
            System.out.println(getName() + " ни о чём не думает ");
        }

    }

    @Override
    public void walk(Location location) {
        System.out.println(getName() + " идёт из " + this.location.where() + " в " + location);
        this.location = location;
    }

    @Override
    public void getInfo() {
        System.out.println("Имя: " + getName() + "; Возраст: " + getAge() + "; Текущая геолокация: " + getLocation() + "; Текущее состояние: " + getState());
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Animal animal = (Animal) obj;
        return getName() == animal.getName();
    }

    @Override
    public int hashCode() {
        return this.getName().hashCode();
    }

    @Override
    public String toString() {
        return "Животное " + getName();
    }

    public State getState() {
        return state;
    }

    public void setState(State state) {
        this.state = state;
    }

    public Location getLocation() {
        return location;
    }

    public void setLocation(Location location) {
        this.location = location;
    }

    public boolean isAbilitySpeak() {
        return AbilitySpeak;
    }

    public void setAge(int age) throws InvalidAge {
        this.age = age;
    }
    public int getAge() {
        return age;
    }
}
