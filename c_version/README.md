# Jeu Mancala à 16 Trous - Version C++

## Compilation

### C++ Bot

Compilez le bot C++ avec g++:

```bash
cd c_version
g++ -o build/bot.exe bot.cpp -std=c++17 -O2
```

### Java Arbitre

Compilez les fichiers Java:

```bash
javac Arbitre.java
javac JoueurExterne.java
```

### Main Game (Optional)

Pour compiler le jeu principal avec g++ (MinGW sur Windows ou GCC sur Linux/Mac):

```bash
cd c_version
g++ -std=c++17 -O2 -o mancala main.cpp
```

## Exécution

### Lancer une partie avec l'arbitre

```bash
java Arbitre
```

L'arbitre lancera automatiquement les deux bots et gérera la partie.

### Configuration des bots

Dans `Arbitre.java`, les bots sont configurés ainsi:

- Joueur A: `c_version\bot.exe` (votre bot C++)
- Joueur B: `kacem.exe` (bot adverse)

#### Comment changer les joueurs

Pour jouer contre un autre bot, modifiez les lignes 11-12 dans `Arbitre.java`:

```java
// Ligne 11: Joueur 1 (trous impairs)
Process A = Runtime.getRuntime().exec(new String[]{"c_version\\bot.exe", "JoueurA"});

// Ligne 12: Joueur 2 (trous pairs)
Process B = Runtime.getRuntime().exec(new String[]{"kacem.exe", "JoueurB"});
```

Exemples de configuration:

- **Bot C++ vs Bot Kacem**: `{"c_version\\bot.exe", "JoueurA"}` vs `{"kacem.exe", "JoueurB"}`
- **Bot C++ vs autre bot**: `{"c_version\\bot.exe", "JoueurA"}` vs `{"chemin\\vers\\autre_bot.exe", "JoueurB"}`
- **Deux bots différents**: Remplacez les chemins par ceux de vos bots

**Note**: Les bots doivent accepter un argument (JoueurA ou JoueurB) et suivre le protocole de communication de l'arbitre.

## Structure des fichiers

### C++ Bot

- `bot.cpp` - Bot principal utilisant MinMax avec iterative deepening
- `ai_algorithms.h` - Algorithmes d'IA (MinMax, Alpha-Beta)
- `game_engine.h` - Moteur de jeu (exécution des coups, captures)
- `game_rules.h` - Règles du jeu et état du plateau
- `game_manager.h` - Gestionnaire de parties
- `config.h` - Configuration du jeu
- `main.cpp` - Jeu standalone avec interface utilisateur

### Java Arbitre

- `Arbitre.java` - Arbitre gérant les parties entre deux bots
- `JoueurExterne.java` - Interface pour joueurs externes
