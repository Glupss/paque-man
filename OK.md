# Liste des Fonctions Autorisées (Pygame-CE -> MLX)

Tu as tout à fait raison ! Le wrapper Python de la MLX (PyMLX) expose beaucoup plus de fonctions que la version C de base. Puisque tu as accès à toutes ces fonctions MLX, cela débloque leurs équivalents stricts dans Pygame-CE !

Voici la liste complète et mise à jour de ce que tu as le droit d'utiliser dans Pygame-CE, mappé exactement sur la liste MLX que tu as fournie :

| Category | Function | Returns | Description |
| :--- | :--- | :--- | :--- |
| **INIT** | `pygame.init()` | `tuple` | Initialise Pygame (Équivalent: `mlx.Mlx()` / `mlx_init()`) |
| **INIT** | `pygame.quit()` | `None` | Ferme l'affichage et libère les ressources (Équivalent: `mlx_release()`) |
| **WINDOW** | `pygame.display.set_mode((w, h))` | `Surface` | Crée la fenêtre (Équivalent: `mlx_new_window()`) |
| **WINDOW** | `screen.fill((0, 0, 0))` | `Rect` | Remplit la surface/fenêtre de noir (Équivalent: `mlx_clear_window()`) |
| **WINDOW** | `pygame.display.quit()` | `None` | Ferme et détruit la fenêtre (Équivalent: `mlx_destroy_window()`) |
| **DRAW** | `screen.set_at((x, y), color)` | `None` | Dessine un pixel (Équivalent: `mlx_pixel_put()`) |
| **DRAW** | `font.render(text, ...)` + `blit` | `Surface` | Dessine du texte via un buffer (Équivalent: `mlx_string_put()`) |
| **IMAGE** | `pygame.Surface((w, h))` | `Surface` | Alloue un buffer de pixels hors-écran (Équivalent: `mlx_new_image()`) |
| **IMAGE** | `pygame.PixelArray(surface)` | `PixelArray` | Accès direct à la mémoire brute des pixels (Équivalent: `mlx_get_data_addr()`) |
| **IMAGE** | `screen.blit(surface, (x, y))` | `Rect` | Pousse le buffer d'image sur la fenêtre (Équivalent: `mlx_put_image_to_window()`) |
| **IMAGE** | `del surface` | `None` | Libère la mémoire (géré par le Garbage Collector Python) (Équivalent: `mlx_destroy_image()`) |
| **IMAGE** | `pygame.image.load(filename)` | `Surface` | Charge une image (PNG, JPG, etc.) (Équivalent: `mlx_png_file_to_image()` / `mlx_xpm_file_to_image()`) |
| **IMAGE** | `pygame.image.frombuffer(...)` | `Surface` | Crée une image depuis des données en mémoire (Équivalent: `mlx_xpm_to_image()`) |
| **EVENT** | `while True:` | `None` | Lance la boucle d'événements (Équivalent: `mlx_loop()`) |
| **EVENT** | `break` (sortie de boucle) | `None` | Quitte la boucle d'événements (Équivalent: `mlx_loop_exit()`) |
| **EVENT** | Code de votre boucle principale | `None` | Logique appelée à chaque frame (Équivalent: `mlx_loop_hook()`) |
| **EVENT** | `pygame.event.get()` | `list[Event]` | Récupère tous les événements X11/Système (Équivalent: `mlx_hook()`) |
| **EVENT** | `event.type == pygame.KEYUP` | `bool` | Détecte le relâchement d'une touche (Équivalent: `mlx_key_hook()`) |
| **EVENT** | `event.type == pygame.MOUSEBUTTONDOWN`| `bool` | Détecte un clic souris (Équivalent: `mlx_mouse_hook()`) |
| **EVENT** | `event.type == pygame.WINDOWEXPOSED` | `bool` | Détecte quand la fenêtre doit être redessinée (Équivalent: `mlx_expose_hook()`) |
| **MOUSE** | `pygame.mouse.set_visible(True)` | `bool` | Rend le curseur visible (Équivalent: `mlx_mouse_show()`) |
| **MOUSE** | `pygame.mouse.set_visible(False)` | `bool` | Cache le curseur (Équivalent: `mlx_mouse_hide()`) |
| **MOUSE** | `pygame.mouse.set_pos([x, y])` | `None` | Déplace le curseur à (x, y) (Équivalent: `mlx_mouse_move()`) |
| **MOUSE** | `pygame.mouse.get_pos()` | `(x, y)` | Retourne la position actuelle du curseur (Équivalent: `mlx_mouse_get_pos()`) |
| **KEYBOARD**| `pygame.key.set_repeat(delay, int)` | `None` | Active l'auto-repeat des touches (Équivalent: `mlx_do_key_autorepeaton()`) |
| **KEYBOARD**| `pygame.key.set_repeat(0)` | `None` | Désactive l'auto-repeat des touches (Équivalent: `mlx_do_key_autorepeatoff()`) |
| **INFO** | `pygame.display.Info().current_w` | `int` | Retourne la taille de l'écran du moniteur (Équivalent: `mlx_get_screen_size()`) |
| **SYNC** | `pygame.display.update()` / `flip()` | `None` | Pousse toutes les commandes de dessin à l'écran (Équivalent: `mlx_do_sync()` / `mlx_sync()`) |

---

**Ce qui reste formellement interdit (car absent de ta liste MLX) :**
- `pygame.sprite` (Groupes, Sprites)
- `pygame.Rect.colliderect` (et la physique)
- `pygame.transform` (Scale, rotate)
- `pygame.draw.circle` / `pygame.draw.polygon` (seul `set_at`/`pixel_put` est justifié, ou `fill` pour nettoyer).
