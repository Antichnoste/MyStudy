package BookWinnieThePooh;

import java.util.List;
import java.util.ArrayList;

public class Group implements Walking{
    private String name;
    private Location location;
    private List <Animal> group = new ArrayList<>();

    public Group() {
        this("noname",new Location("где-то"));
    }

    public Group(Location location) {
        this("noname", location);
    }

    public Group(String name) {
        this("noname",new Location(name));
    }

    public Group(String name, Location location) {
        this.name = "noname";
        this.location = location;
    }

    public String namesAll(){
        String ans = "";

        for (int i = 0; i < group.size(); i++) {
            if (i == group.size() - 1){
                ans += group.get(i).getName();
            } else{
                ans += group.get(i).getName() + ", ";
            }
        }

        return ans;
    }

    public void addMember(Animal member){
        this.group.add(member);
    }

    public void addMember(Animal... members){
        for (Animal member : members)
            this.group.add(member);
    }

    public void removeMembers(Animal member) {
        this.group.remove(member);
    }

    public void size(){
        System.out.println(this.group.size());
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Location getLocation() {
        return location;
    }

    public void setLocation(Location location) {
        this.location = location;
    }

    public List<Animal> getGroup() {
        return group;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Group group = (Group) obj;
        return getName() == group.getName();
    }

    @Override
    public int hashCode() {
        return this.getName().hashCode();
    }

    @Override
    public String toString() {
        return "Группа " + getName();
    }

    @Override
    public void walk(Location location) {
        System.out.println(namesAll() + " перешли из " + this.location.where() + " в " + location);
        this.location = location;
    }

    public void walk() {
        System.out.println(namesAll() + " идут по " + this.location.where());
    }
}
