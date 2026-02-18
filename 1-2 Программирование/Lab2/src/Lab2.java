import Pokemons.*;
import Physical.*;
import Special.*;
import Status.*;
import ru.ifmo.se.pokemon.*;

public class Lab2{
    public static void main (String[] args){

        Battle b = new Battle();

        Pinsir pinsir = new Pinsir("Рогатый", 1);
        Feebas feebas = new Feebas("Рыбка", 1);
        Clefable clefable = new Clefable("Лапочка_3", 3);
        Clefairy clefairy = new Clefairy("Лапочка_2", 2);
        Cleffa cleffa = new Cleffa("Лапочка_1", 1);

        b.addAlly(pinsir);
        b.addFoe(feebas);

//        b.addFoe(clefable);
//        b.addFoe(cleffa);
//        b.addFoe(clefairy);

        b.go();
    }
}