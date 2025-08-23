Tu as plusieurs options selon l’OS et tes besoins. Vu que tu es sous Linux Mint, voici les plus simples → plus avancées :

### 1) Ultra‑simple sous Linux (utilitaire système)

```python
import subprocess
subprocess.run(["aplay", "/chemin/son.wav"])  # ou "paplay" selon ta distrib
```

---

### 2) Cross‑platform léger: `simpleaudio` (recommandé)

```bash
pip install simpleaudio
```

```python
import simpleaudio as sa

wave_obj = sa.WaveObject.from_wave_file("/chemin/son.wav")
play_obj = wave_obj.play()   # non bloquant
play_obj.wait_done()         # bloquant (optionnel)
# pour couper avant la fin: play_obj.stop()
```

---

### 3) Avec `pygame` (si tu l’utilises déjà)

```bash
pip install pygame
```

```python
import pygame
pygame.mixer.init()
snd = pygame.mixer.Sound("/chemin/son.wav")
snd.play()           # non bloquant
pygame.time.delay(2000)  # attendre 2s, sinon ton script peut se terminer
```

---

### 4) Windows uniquement: `winsound` (standard library)

```python
import winsound
winsound.PlaySound(r"C:\chemin\son.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
```

---

#### Bonus : petite fonction utilitaire (essaie `aplay`, sinon `simpleaudio`)

```python
import shutil, subprocess

def play_wav(path):
    if shutil.which("aplay"):
        subprocess.run(["aplay", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        import simpleaudio as sa
        sa.WaveObject.from_wave_file(path).play().wait_done()
```

Tu veux le déclencher sans bloquer ta boucle (genre UI ou jeu) et pouvoir l’arrêter ? Pars sur `simpleaudio` : `play_obj = wave_obj.play()` puis `play_obj.stop()`. Si tu veux gérer le volume, on peut charger en `numpy` et ajuster les amplitudes avant lecture.
