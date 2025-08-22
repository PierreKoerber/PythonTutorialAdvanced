Voici un **mini–tutoriel Tkinter** qui va droit au but, avec juste assez de sauce pour être utile rapidement. On part de zéro ➜ petite app propre ➜ patterns pro ➜ emballage.

---

# 0) Pré-requis

- **Linux Mint** : `sudo apt install python3-tk`
- **Windows/macOS** : rien à installer en plus (Tk est livré avec Python officiel).
- Test rapide :

  ```bash
  python -m tkinter
  ```

  Si une petite fenêtre “Tk” s’ouvre, c’est bon.

---

# 1) Hello world (et les bases)

```python
import tkinter as tk

root = tk.Tk()
root.title("Hello Tk")
root.geometry("300x150")  # largeur x hauteur

label = tk.Label(root, text="Bonjour 👋")
label.pack(pady=20)

btn = tk.Button(root, text="Fermer", command=root.destroy)
btn.pack()

root.mainloop()
```

À savoir :

- `Tk()` = fenêtre principale.
- `mainloop()` = boucle évènementielle (ne bloque pas l’UI si vous ne faites pas de longues tâches dedans).
- Gestionnaires de géométrie : `pack`, `grid`, `place`. Utilisez **grid** pour du layout sérieux.

---

# 2) Version “TTK” (widgets modernes)

```python
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("TTK quickstart")

frm = ttk.Frame(root, padding=12)
frm.grid(sticky="nsew")           # cadre principal
root.columnconfigure(0, weight=1) # rendre redimensionnable
root.rowconfigure(0, weight=1)

ttk.Label(frm, text="Nom:").grid(row=0, column=0, sticky="w")
name = tk.StringVar()
ttk.Entry(frm, textvariable=name, width=30).grid(row=0, column=1, sticky="ew")

def hello():
    ttk.Label(frm, text=f"Salut {name.get()} !").grid(row=2, column=0, columnspan=2, pady=8)

ttk.Button(frm, text="Dire bonjour", command=hello).grid(row=1, column=0, columnspan=2, pady=8)

frm.columnconfigure(1, weight=1)
root.mainloop()
```

Points clés :

- **`ttk`** = widgets thémables + plus jolis.
- **Variables Tk** (`StringVar`, `IntVar`, etc.) lient champs ↔︎ état.

---

# 3) Événements et bindings

```python
def on_enter(event):
    print("Entrée pressée:", entry.get())

entry = ttk.Entry(frm)
entry.grid(row=0, column=0, sticky="ew")
entry.bind("<Return>", on_enter)
```

- Exemples d’événements : `<Button-1>`, `<KeyPress>`, `<Control-s>`, `<Configure>` (resize).

---

# 4) Menus, boîtes de dialogue, fichiers

```python
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

root = tk.Tk()
menubar = tk.Menu(root)
root.config(menu=menubar)

def open_file():
    path = filedialog.askopenfilename(filetypes=[("Text", "*.txt"), ("Tous", "*.*")])
    if path:
        messagebox.showinfo("Fichier choisi", path)

filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Ouvrir…", command=open_file)
filemenu.add_separator()
filemenu.add_command(label="Quitter", command=root.destroy)
menubar.add_cascade(label="Fichier", menu=filemenu)

ttk.Label(root, text="Menu en haut, dialogues prêts.").pack(padx=12, pady=12)
root.mainloop()
```

---

# 5) Canvas, images, icônes

```python
import tkinter as tk

root = tk.Tk()
cv = tk.Canvas(root, width=300, height=150, bg="white")
cv.pack(fill="both", expand=True)
cv.create_rectangle(20, 20, 120, 80, outline="blue", width=2)
cv.create_text(160, 50, text="Canvas 😎")

# Icône fenêtre (PNG/ICO)
# root.iconphoto(True, tk.PhotoImage(file="icon.png"))

root.mainloop()
```

- Pour afficher des images : `PhotoImage` (PNG, GIF). Pour JPEG/plus ➜ **Pillow** (`pip install pillow`, `from PIL import Image, ImageTk`).

---

# 6) Structure “propre” (classe Application)

```python
import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Todo minimal")
        self.geometry("360x280")

        self.tasks = []

        container = ttk.Frame(self, padding=12)
        container.pack(fill="both", expand=True)

        self.var = tk.StringVar()
        ent = ttk.Entry(container, textvariable=self.var)
        ent.pack(fill="x")

        ttk.Button(container, text="Ajouter", command=self.add_task).pack(pady=6)

        self.listbox = tk.Listbox(container, height=8)
        self.listbox.pack(fill="both", expand=True)

        ttk.Button(container, text="Supprimer sélection", command=self.remove_selected).pack(pady=6)

    def add_task(self):
        text = self.var.get().strip()
        if not text:
            return
        self.tasks.append(text)
        self.listbox.insert("end", text)
        self.var.set("")

    def remove_selected(self):
        for i in reversed(self.listbox.curselection()):
            self.listbox.delete(i)
            del self.tasks[i]

if __name__ == "__main__":
    App().mainloop()
```

- Avantages : état encapsulé, testabilité, lisible.
- Pour du layout avancé, créez des Frames spécialisées (écran login, écran “docs”, etc.).

---

# 7) Concurrence, tâches longues, `after`

**Ne bloquez jamais l’UI**. Deux options :

### a) `after` (boucle planifiée)

```python
def tick():
    # faire un petit boulot
    progress.step(1)
    if progress["value"] < 100:
        root.after(50, tick)

root.after(0, tick)
```

### b) Thread + file queue

```python
import threading, queue
q = queue.Queue()

def worker():
    # tache longue
    for i in range(1000000):
        if i % 100000 == 0:
            q.put(i)

def poll_queue():
    while not q.empty():
        value = q.get_nowait()
        label["text"] = f"Progress: {value}"
    root.after(100, poll_queue)

threading.Thread(target=worker, daemon=True).start()
root.after(100, poll_queue)
```

- **Jamais** d’accès direct aux widgets depuis un thread secondaire : passez par la queue + `after`.

---

# 8) Styles TTK (propre et cohérent)

```python
from tkinter import ttk

style = ttk.Style()
# style.theme_use("clam")  # selon OS
style.configure("TButton", padding=6)
style.configure("Danger.TButton", foreground="white", background="#d9534f")
# usage : ttk.Button(root, text="Supprimer", style="Danger.TButton")
```

- Sur macOS/Windows, les thèmes varient. Pour un look identique partout, utilisez un thème ttk cohérent (clam, alt, etc.).

---

# 9) Widgets utiles à connaître

- `ttk.Treeview` : tableaux/listes hiérarchiques (avec **Scrollbars**).
- `ttk.Notebook` : onglets.
- `ttk.Spinbox`, `ttk.Combobox` : sélections contrôlées.
- `Toplevel` : fenêtres secondaires (modales via `grab_set()`).
- Validation d’Entry : `validate`, `validatecommand`.
- `StringVar.trace_add("write", callback)` pour réagir aux changements.

---

# 10) Packaging (PyInstaller)

1. Installer :

```bash
pip install pyinstaller
```

2. Construire :

```bash
pyinstaller --onefile --windowed votre_app.py
```

- Linux : nécessite que la machine cible ait les libs graphiques (Tk). Pour du “vraiment portable”, regardez **AppImage**/Flatpak/Snap.
- Windows/macOS : l’exe/app embarque ce qu’il faut.

---

# 11) Débogage express

- Rien ne s’affiche ? → Vérifiez que **`mainloop()`** est bien appelé.
- Freeze UI ? → Vous faites un gros calcul dans le thread GUI. Passez par `after()` ou un thread + queue.
- TTK pas “beau” ? → Testez un autre thème (`style.theme_use("clam")`).
- `ModuleNotFoundError: _tkinter` ? → Installez `python3-tk` (Linux) / réinstallez Python officiel (Win/macOS).

---

# 12) Exercices rapides

1. **Compteur** : bouton “+1”, “-1”, “Reset”, affichage dynamique.
2. **Chrono** : start/stop/reset avec `after`.
3. **Bloc-notes** : zone texte + “Ouvrir/Enregistrer” (filedialog) + “Ctrl+S”.
4. **Mini dashboard** : 3 cartes (ttk.Frame) disposées en `grid`, responsive.

---

Si tu veux, je te prépare un **squelette d’app** “propre” (structure de fichiers, thème, barre de menu, status bar, gestion des écrans) que tu pourras forker pour tes projets Tkinter. Tu me dis ton besoin (monofenêtre simple, multi-écrans, petit CRUD local…) et je te le monte.
