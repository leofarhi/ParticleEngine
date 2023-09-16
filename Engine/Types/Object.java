package Engine.Types;

public class Object{
    public String UUID;

    public Object() {
        this.UUID = ParticleEngine.GenerateUUID();
    }

    public Object(String UUID) {
        this.UUID = UUID;
    }
}