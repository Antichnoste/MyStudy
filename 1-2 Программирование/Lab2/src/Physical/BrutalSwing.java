package Physical;

import ru.ifmo.se.pokemon.*;

public class BrutalSwing extends PhysicalMove {
    public BrutalSwing() {
        super(Type.DARK, 60,100);
    }

    @Override
    protected String describe(){
        return "яростно размахивает своим телом, чтобы нанести урон всему, что находиться поблизости";
    }
}
