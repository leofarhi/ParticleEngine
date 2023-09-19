package Engine.Components;

import java.util.ArrayList;
import Engine.Types.Vector3;
import Engine.Types.GameObject;
import Engine.Types.Vector2;
import Engine.Types.Component;

public class Transform extends Component{
    public Vector3 position;
    public Vector3 rotation;
    public Vector3 scale;

    @HideInInspector
    public Transform parent;
    @HideInInspector
    public ArrayList<Transform> children;
}
