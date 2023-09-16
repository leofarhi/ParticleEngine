package Engine.Types;

@Serializable
public class GameObject extends Object{

    public GameObject(String name, int health, int damage) {
        this.name = name;
        this.health = health;
        this.damage = damage;
    }

    public bool attack(GameObject enemy) {
        enemy.health -= this.damage;
    }
}