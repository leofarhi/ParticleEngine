package com.example.helloworld;
import java.util.ArrayList;
import java.util.List;

public class HelloWorld {

    public HelloWorld() {
    }
    public static void main(String[] args) {
        System.out.println("Hello, World");
        List<String> list = new ArrayList<>();
    }
}

@Serializable
public class Player {
    private String name = "Player";
    private int health;
    private int damage;

    public Player(String name, int health, int damage) {
        this.name = name;
        this.health = health;
        this.damage = damage;
    }

    public bool attack(Player enemy) {
        enemy.health -= this.damage;
    }
}

public class Enemy extends Player {
    public Enemy(String name, int health, int damage) {
        super(name, health, damage);
    }
}
