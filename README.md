
# ❄️ Frostfire 🔥

**Frostfire** è un gioco sviluppato in Python utilizzando la libreria Pygame. L'obiettivo è sopravvivere e segnare più punti possibili evitando bombe 💣 e raccogliendo XP ✨.

## ⚙️ Requisiti
- 🐍 **Python 3.x**
- 🎮 **Pygame**

## 🚀 Installazione
1. Clona il repository:
   ```bash
   git clone https://github.com/tuo_utente/frostfire.git
   ```
2. Naviga nella directory del progetto:
   ```bash
   cd frostfire
   ```
3. Installa Pygame:
   ```bash
   pip install pygame
   ```

## 🎮 Utilizzo
Per avviare il gioco, esegui:
```bash
python frostfire.py
```

## 🕹️ Controlli
- **Mouse**: per mirare e sparare ai bersagli.
- **Click sinistro del mouse**: spara un proiettile.
- **Tasto sinistro del mouse durante Game Over**: clicca su **Retry** per ricominciare.

## 🌟 Funzionalità
- **Sistema di punteggio 🏆 e highscore**: Il punteggio corrente viene mostrato sullo schermo, e l'highscore è memorizzato in `highscore.json`.
- **Spawn di oggetti casuali 🎲**: Ogni secondo spawna un nuovo oggetto (XP o bomba) con diverse caratteristiche.
- **Barra di caricamento 🔫**: Mostra il numero di colpi rimasti.
- **Invulnerabilità temporanea 🛡️**: Dopo aver subito un danno, il giocatore è invulnerabile per un breve periodo.

## 🔍 Dettagli del Codice
Il gioco è composto dalle seguenti classi e funzioni principali:
- **Bullet**: Gestisce la creazione e il movimento dei proiettili.
- **Ball**: Rappresenta gli oggetti pericolosi (bombe) e non pericolosi (XP).
- **calculate_angle** e **draw_arrow**: Calcolano e disegnano una freccia per la direzione del proiettile.
- **check_collision** e **check_player_collision**: Verificano le collisioni tra proiettili e oggetti o tra il giocatore e le bombe.
- **draw_button**: Disegna i pulsanti, utilizzato per il bottone Retry.

## 🎨 Grafica e Risorse
- **Immagini**: Il gioco utilizza immagini di sfondo, giocatore, bombe, e XP (`bg.jpg`, `player.png`, `bomb.png`, `xp.png`).
- **Colori**: Il gioco usa colori predefiniti per rappresentare elementi grafici (WHITE, YELLOW, RED, GREEN, GRAY).

## 🖼️ Schermata di Gioco
- **Barra di vite ❤️**: Mostra le vite rimanenti del giocatore.
- **Schermata di Game Over 💀**: Mostra il punteggio finale e offre un'opzione per ricominciare.

## 🏅 Highscore
L'highscore è salvato in un file `highscore.json` ed è aggiornato automaticamente se il nuovo punteggio supera il precedente record.

## 📜 License
MIT License

## 📬 Contatti
Per qualsiasi domanda, contattami su [tuo_email@example.com](mailto:tuo_email@example.com).
