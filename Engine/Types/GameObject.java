package Engine.Types;

import java.util.ArrayList;
import Engine.Components.Transform;


public class GameObject extends Object{
    public String name;
    public Tag tag;
    public Layer layer;
    public Transform transform;
    public ArrayList<Component> components;
    public boolean activeInHierarchy;
    public boolean activeSelf;
    public boolean isStatic;
    
}