# 🧩 Fillomino Puzzle Game

Fillomino is a logic puzzle where the goal is to divide a grid into **polyominoes** — connected groups of cells — such that:
- Each group contains exactly as many cells as the number it displays.
- No two polyominoes of the same size touch side-by-side.

This app provides an interactive way to play Fillomino puzzles, with boards generated using a SAT solver to ensure each puzzle has a **unique solution**.

---

## 📖 About the Application

This Fillomino puzzle game generates boards by encoding the puzzle rules into logical formulas solved by a SAT solver. The solver finds valid solutions that satisfy all puzzle constraints, ensuring each generated board has a unique and correct solution.

To handle complex shapes—especially large polyominoes—some patterns were precomputed and saved in a file (`polyominos.txt`). During board generation, these precomputed shapes are loaded from the file and reused, which avoids costly recomputation and speeds up the process.

---

## 🎮 How to Play

1. **Start Screen**  
   - Select the **board size** and **maximum polyomino size** from dropdown menus (default values are smallest possible).  
   - Press **Start** to generate a new puzzle.  
   - Press **Exit** to close the app.
     
   <img width="300" height="330" alt="main_menu" src="https://github.com/user-attachments/assets/09347a43-083a-4fa2-97de-6d5567f02c0f" />


2. **Puzzle Screen**  
   - After generation, a partially filled board appears.
     
   <img width="342" height="451" alt="empty board" src="https://github.com/user-attachments/assets/b15b4f63-86de-4abb-b4ee-f9bf29d3b34c" />
   
   - Use the mouse or keyboard to select values to fill the board. The available numbers correspond to the maximum polyomino size chosen.  
   - Correct polyominoes are highlighted in different colors.  
   - Incorrect polyominoes are highlighted in red.
     
   <img width="342" height="451" alt="wrong board" src="https://github.com/user-attachments/assets/2f7ae836-7f96-4f83-ab8d-218bc728a4a5" />


3. **Completion**  
   - Once the board is correctly completed, you will see a success message with the time taken to solve the puzzle.
     
   <img width="342" height="450" alt="end" src="https://github.com/user-attachments/assets/276f7407-abcd-4ae5-8a16-a5d74d95fbae" />
   
   - You can then return to the main menu.

