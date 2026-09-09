# Liste des Fonctions Autorisées (Pygame-CE -> MLX)

Conformément à la règle stipulant que toute fonction utilisée doit avoir un équivalent strict dans la **MiniLibX (MLX)**, voici la liste exhaustive des fonctions Pygame-CE que tu as le droit d'utiliser. Tout ce qui n'est pas dans cette liste (sprites, rect.colliderect, draw.circle, etc.) est à proscrire ou à recoder à la main.

| Category | Function | Returns | Description |
| :--- | :--- | :--- | :--- |
| **INIT** | `pygame.init()` | `tuple` | Initialise les modules Pygame (Équivalent: `mlx_init()`) |
| **INIT** | `pygame.display.set_mode((width, height))` | `Surface` | Ouvre une nouvelle fenêtre de rendu (Équivalent: `mlx_new_window()`) |
| **DISPLAY** | `pygame.display.update()` / `.flip()` | `None` | Rafraîchit l'affichage de la fenêtre pour montrer les derniers dessins (Équivalent du rafraîchissement interne de MLX) |
| **SURFACE** | `pygame.Surface((width, height))` | `Surface` | Crée un buffer/image vide en mémoire (Équivalent: `mlx_new_image()`) |
| **SURFACE** | `pygame.image.load(filepath)` | `Surface` | Charge une image (ex: PNG/XPM) depuis un fichier (Équivalent: `mlx_xpm_file_to_image()`) |
| **SURFACE** | `Surface.blit(source, (x, y))` | `Rect` | Dessine (colle) une surface source sur une autre surface ou sur l'écran (Équivalent: `mlx_put_image_to_window()`) |
| **SURFACE** | `Surface.set_at((x, y), color)` | `None` | Modifie la couleur d'un pixel précis sur la surface (Équivalent: `mlx_pixel_put()` ou modification manuelle du buffer image) |
| **EVENTS** | `pygame.event.get()` | `list[Event]` | Récupère la liste des événements (clavier, souris, fermeture) (Équivalent: `mlx_hook()` / `mlx_key_hook()`) |
| **TEXT** | `pygame.font.SysFont(name, size)` | `Font` | Charge une police d'écriture système |
| **TEXT** | `Font.render(text, antialias, color)` | `Surface` | Transforme un texte en une image/Surface affichable avec `blit` (Équivalent: `mlx_string_put()`) |
| **TIME** | `pygame.time.Clock()` | `Clock` | Crée une horloge pour gérer le temps (Nécessaire pour simuler le comportement fluide de `mlx_loop_hook()`) |
| **TIME** | `Clock.tick(framerate)` | `int` | Met en pause le programme pour bloquer le jeu au nombre de FPS défini |

---

**Note importante :** 
En MLX, la boucle principale est lancée via `mlx_loop()`. En Pygame, tu devras faire un équivalent manuel avec une boucle infinie classique :
```python
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Quit (mlx destroy window)
```
