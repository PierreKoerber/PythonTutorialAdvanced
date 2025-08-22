import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from datetime import datetime
import json, csv, threading, re

def scan_dir(path: str) -> list[dict]:
    p = Path(path)
    out = []
    for f in p.rglob("*"):
        if f.is_file():
            st = f.stat()
            out.append({
                "path": str(f),
                "name": f.name,
                "ext": f.suffix.lower(),
                "size": st.st_size,
                "mtime": datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds"),
            })
    return out

def filter_sort(rows, ext="", pattern="", min_size="", sort_key="size", desc=False):
    res = rows
    if ext:
        e = ext.lower().strip()
        if not e.startswith("."): e = "." + e
        res = [x for x in res if x["ext"] == e]
    if pattern:
        pat = re.compile(pattern, re.IGNORECASE)
        res = [x for x in res if pat.search(x["name"])]
    if min_size:
        try:
            ms = int(min_size)
            res = [x for x in res if x["size"] >= ms]
        except ValueError:
            pass
    return sorted(res, key=lambda x: x.get(sort_key, ""), reverse=bool(desc))

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Data Explorer (GUI)")
        self.geometry("820x520")

        # Top controls
        top = ttk.Frame(self); top.pack(fill="x", padx=8, pady=6)
        self.path_var = tk.StringVar(value=str(Path.cwd()))
        ttk.Entry(top, textvariable=self.path_var, width=60).pack(side="left", padx=4)
        ttk.Button(top, text="Choisir dossier", command=self.choose_dir).pack(side="left")
        ttk.Button(top, text="Scanner", command=self.scan_async).pack(side="left", padx=4)

        # Filters
        filt = ttk.Frame(self); filt.pack(fill="x", padx=8, pady=4)
        self.ext_var = tk.StringVar()
        self.pattern_var = tk.StringVar()
        self.min_size_var = tk.StringVar()
        ttk.Label(filt, text="Ext:").pack(side="left"); ttk.Entry(filt, textvariable=self.ext_var, width=8).pack(side="left", padx=4)
        ttk.Label(filt, text="Motif:").pack(side="left"); ttk.Entry(filt, textvariable=self.pattern_var, width=18).pack(side="left", padx=4)
        ttk.Label(filt, text="Min (octets):").pack(side="left"); ttk.Entry(filt, textvariable=self.min_size_var, width=10).pack(side="left", padx=4)
        ttk.Button(filt, text="Appliquer filtres", command=self.apply_filters).pack(side="left", padx=6)

        # Sort
        sortf = ttk.Frame(self); sortf.pack(fill="x", padx=8, pady=4)
        self.sort_key = tk.StringVar(value="size")
        self.sort_desc = tk.BooleanVar(value=True)
        ttk.Label(sortf, text="Trier par:").pack(side="left")
        ttk.Combobox(sortf, textvariable=self.sort_key, values=["name","size","ext","mtime"], width=8, state="readonly").pack(side="left", padx=4)
        ttk.Checkbutton(sortf, text="Décroissant", variable=self.sort_desc).pack(side="left", padx=6)
        ttk.Button(sortf, text="Trier", command=self.apply_filters).pack(side="left", padx=6)

        # Treeview
        cols = ("name","ext","size","mtime","path")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, anchor="w", width=120 if c!="path" else 360)
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)

        # Bottom actions
        bottom = ttk.Frame(self); bottom.pack(fill="x", padx=8, pady=6)
        ttk.Button(bottom, text="Exporter JSON", command=self.export_json).pack(side="left")
        ttk.Button(bottom, text="Exporter CSV", command=self.export_csv).pack(side="left", padx=6)
        self.status = tk.StringVar(value="Prêt.")
        ttk.Label(bottom, textvariable=self.status).pack(side="right")

        self._index = []   # données brutes scannées
        self._view = []    # données filtrées/triées (affichées)

    def choose_dir(self):
        d = filedialog.askdirectory(initialdir=self.path_var.get() or ".")
        if d:
            self.path_var.set(d)

    def scan_async(self):
        d = self.path_var.get().strip() or "."
        self.status.set("Scan en cours…")
        self.tree.delete(*self.tree.get_children())
        threading.Thread(target=self._scan_thread, args=(d,), daemon=True).start()

    def _scan_thread(self, d):
        try:
            rows = scan_dir(d)
            self._index = rows
            self._view = rows
            self.after(0, lambda: (self.fill_tree(self._view), self.status.set(f"{len(rows)} fichiers trouvés.")))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Erreur", str(e)))

    def apply_filters(self):
        self._view = filter_sort(self._index, self.ext_var.get(), self.pattern_var.get(),
                                 self.min_size_var.get(), self.sort_key.get(), self.sort_desc.get())
        self.fill_tree(self._view)
        self.status.set(f"{len(self._view)} affichés (sur {len(self._index)})")

    def fill_tree(self, rows):
        self.tree.delete(*self.tree.get_children())
        for x in rows[:5000]:  # garde l’UI fluide si énorme dossier
            self.tree.insert("", "end", values=(x["name"], x["ext"], x["size"], x["mtime"], x["path"]))

    def export_json(self):
        if not self._view:
            messagebox.showinfo("Info", "Rien à exporter.")
            return
        f = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON","*.json")], initialfile="index.json")
        if not f: return
        with open(f, "w", encoding="utf-8") as out:
            json.dump(self._view, out, indent=2, ensure_ascii=False)
        self.status.set(f"Export JSON: {f}")

    def export_csv(self):
        if not self._view:
            messagebox.showinfo("Info", "Rien à exporter.")
            return
        f = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")], initialfile="index.csv")
        if not f: return
        with open(f, "w", newline="", encoding="utf-8") as out:
            w = csv.DictWriter(out, fieldnames=["path","name","ext","size","mtime"])
            w.writeheader(); w.writerows(self._view)
        self.status.set(f"Export CSV: {f}")

if __name__ == "__main__":
    App().mainloop()