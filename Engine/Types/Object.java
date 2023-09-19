package Engine.Types;

public class Object{
    
    @HideInInspector
    public String UUID;

    public Object() {
        this.UUID = ParticuleEngine.GenerateUUID();
    }

    public Object(String UUID) {
        this.UUID = UUID;
    }
}