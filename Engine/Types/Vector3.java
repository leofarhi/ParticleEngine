package Engine.Types;

@Serializable
public class Vector3{
    public float x;
    public float y;
    public float z;

    public Vector3() {
        this.x = 0;
        this.y = 0;
        this.z = 0;
    }

    public Vector3(float x, float y, float z) {
        this.x = x;
        this.y = y;
        this.z = z;
    }

    public Vector2 ToVector2() {
        return new Vector2(this.x, this.y);
    }
}