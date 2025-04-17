#Korean Chess (Janggi)

A digital version of the traditional Korean board game *Janggi*, featuring:
- Local single-player mode
- AI opponent with multiple difficulties
- Online multiplayer functionality

---

## Dependencies

Make sure the following are installed on your machine:

- Python 3  
- Pygame  
- NumPy  

---

## 🛠️ How to Run the Game

### 1. Install Python

- Visit [python.org/downloads](https://www.python.org/downloads/)
- Download and install the latest version for your OS (Windows/macOS/Linux)

#### Windows:
- Check **"Add Python to PATH"** during installation

#### macOS:
- You may need to install [Homebrew](https://brew.sh/) if not already installed:
  ```bash
  brew install python3
  ```

#### Verify Installation:
```bash
python --version
```
> On macOS/Linux, you may need to use `python3`.

---

### 2. Install Dependencies

#### Pygame:
```bash
pip install pygame
```

#### NumPy:
```bash
pip install numpy
```
> Use `pip3` if you're on macOS/Linux and `pip` doesn't work.

---

### 3. Install and Run the Game

- Download the project as a `.zip` file from your desired branch
- Unzip it into your preferred directory
- Open terminal and navigate to the project folder:
  ```bash
  cd path/to/project
  ```
- Run the game:
  ```bash
  python main.py
  ```
  > Or `python3 main.py` depending on your system.

---

## 🎮 Game Modes

### 🔹 Single Player
- Control both sides of the board
- Great for practice, setting up scenarios, or playing in-person with someone

### 🔸 Play Against AI
- Battle the powerful **Stockfish** AI engine
- Choose between:
  - Easy
  - Medium
  - Hard

### 🔷 Multiplayer
- Play over a network connection with a friend
- Two roles:
  - **Host**: Starts the game and sees their IP displayed
  - **Client**: Inputs host's IP to connect
- Once connected, enjoy a head-to-head match!

---

## 🔧 Updates (Jan 2025 – May 2025)

- Full **UI overhaul**
  - See additional README files in `Resizing-Style1` and `Resizing-Style2`
- **macOS Support**
  - Creation of a native Stockfish executable for Mac
- **Multiplayer mode** added
- General **documentation improvements**

