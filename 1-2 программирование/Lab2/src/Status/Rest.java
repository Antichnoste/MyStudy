package Status;

import ru.ifmo.se.pokemon.*;

public class Rest extends StatusMove {
    public Rest() {
        super(Type.PSYCHIC, 0,0);
    }

    @Override
    protected void applyOppEffects(Pokemon pokemon){
        pokemon.addEffect(new Effect().turns(2).condition(Status.SLEEP));
        pokemon.restore();
    }

    @Override
    protected String describe(){
        return "засыпает";
    }

}
