# So ersetzt du das bestehende GitHub-Repository

**Ziel:** https://github.com/eyetracking-data/Steps_Order

1. ZIP lokal entpacken. Im Ordner `Steps_Order` liegen alle Dateien und Unterordner für das neue Repository.
2. Das bestehende Repository zur Sicherheit klonen (z. B. mit GitHub Desktop). Der Verlauf ist deine zusätzliche Sicherung.
3. Im **lokalen Repository** alle bisherigen Dateien und Ordner entfernen, **aber den versteckten `.git`-Ordner nicht löschen**.
4. Den **Inhalt** des neu entpackten Ordners `Steps_Order/` in dieses lokale Repository kopieren (nicht den äußeren Ordner selbst).
5. Vorher optional `python -m pip install -r requirements.txt` und `python validate_results.py` ausführen.
6. In GitHub Desktop Änderungen prüfen, Commit z. B. `Replace historical order comparison with reproducible paired experiment` erstellen und pushen.

**Wichtig:** Ein ZIP direkt auf die GitHub-Webseite hochzuladen, packt GitHub nicht automatisch aus. Lade die entpackten Dateien hoch oder nutze GitHub Desktop. Alte Root-Dateien werden nur wirklich entfernt, wenn du sie im geklonten Repository vorher löschst.

Die bisherigen Experimentartefakte sind innerhalb des neuen Pakets unter `legacy/` zur wissenschaftlichen Nachvollziehbarkeit erhalten. `results/` enthält die korrigierten Ergebnisse.
