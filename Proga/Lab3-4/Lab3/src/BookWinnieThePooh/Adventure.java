package BookWinnieThePooh;

public class Adventure {
    private Group group;

    public Adventure(Group group) {
        this.group = group;
    }

    public void go(){
        group.walk();

        group.getGroup().get(0).think("");
        group.getGroup().get(0).speak("aaaaaa");

        group.getGroup().get(1).think("о новом стихотворении");
        group.getGroup().get(1).speak("Теперь нас не удивит, что он поселился в доме у Кенги и всегда получал рыбий жир на завтрак, обед и ужин ");

        group.getGroup().get(2).eat("ложку-другую кашки", Mealtimes.Breakfast);
    }
}

