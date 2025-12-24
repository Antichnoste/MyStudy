package Status;

import ru.ifmo.se.pokemon.*;

public class Growl extends StatusMove{
    public Growl() {
        super(Type.NORMAL,0,100);
    }

    @Override
    protected void applyOppEffects(Pokemon pokemon){
        pokemon.setMod(Stat.ATTACK,-1);
    }

    @Override
    protected String describe(){
        return "рычит";
    }
}
