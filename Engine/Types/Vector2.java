package Engine.Types;

public class Vector2{
    public float x;
    public float y;

    public Vector2() {
        this.x = 0;
        this.y = 0;
    }

    public Vector2(float x, float y) {
        this.x = x;
        this.y = y;
    }

    public Vector3 ToVector3() {
        return new Vector3(this.x, this.y, 0);
    }
}