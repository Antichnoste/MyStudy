import Adventure.*;
import Exceptions.*;
import Kind.*;
import Record.*;
import Enum.*;

public  class Main {
    public static void main(String[] args){
        try{
            Group group = new Group(new Location("дорога"));

            Bear bear = new Bear("Винни Пух", new Location("дорога"), State.Default, 5);
            Animal somebody = new Animal();
            Pig pig = new Pig("Пяточок", new Location("дорога"), State.Default,5);

            group.addMember(pig,bear, somebody);

            Adventure adventure = new Adventure(group);
            adventure.go();

        } catch (InvalidAge e){
            System.out.println(e.getMessage());
        }

    }
}