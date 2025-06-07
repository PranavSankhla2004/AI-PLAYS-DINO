# 🦖 Dino Game with NEAT AI

A Python-based clone of the Chrome Dino Game where an AI trained with [NEAT (NeuroEvolution of Augmenting Topologies)](https://neat-python.readthedocs.io/en/latest/) learns to play and survive obstacles. Built using `pygame`, this project supports both manual and AI modes, with real-time debugging visuals and evolving intelligence.

## 🎯 Project Vision

The goal of this project was to recreate the classic offline Chrome Dino Game and train an AI agent using evolutionary neural networks to learn how to play it autonomously. The AI is built using the NEAT algorithm and is capable of improving over generations by adjusting its neural network based on survival performance.

This project serves as a hands-on demonstration of:
- Game development using Pygame.
- Artificial intelligence using NEAT.
- Real-time simulation and debugging visualization.

---

## 📽️ Screenshots

> 🖼️ Add these after running the game:
- Normal game mode screenshot
- Bounding box debug mode screenshot (press `D` during gameplay)

---


---

## 🔧 Game Features

- **Manual Play Mode** – Control the dinosaur with `Up`, `Down`, and `Space` keys.
- **AI Play Mode** – NEAT algorithm trains a population of dinos to survive.
- **Obstacles** – Includes small & large cacti, and birds.
- **Animations** – Smooth run, jump, and duck animations.
- **Scrolling Background** – Creates illusion of motion with looping track.
- **Clouds** – Moving clouds add depth and realism.
- **Score System** – Points increase with time and are displayed in-game.
- **Debug Mode** – Bounding boxes and AI stats shown by pressing `D`.

---

## 🧠 NEAT AI Learning Inputs

Each AI-controlled dino receives the following inputs to make decisions:
1. Distance to nearest obstacle
2. Width of the obstacle
3. Height of the obstacle
4. Dino's vertical position
5. Game speed

Outputs from the neural network:
- Jump if output[0] > 0.5
- Duck if output[1] > 0.5

---

## 🚶 Development Steps

### 1. **Set Up the Game Screen**
- Initialized `pygame` and set up the screen size, title, and FPS.

### 2. **Create Scrolling Background**
- Loaded background image and used two blits with changing `x` position to create a seamless scrolling effect.

### 3. **Add the Dinosaur**
- Created a `Dinosaur` class with states: running, jumping, ducking.
- Added animation frames for running and ducking.
- Controlled jump physics using velocity and gravity simulation.

### 4. **Obstacle System**
- Defined `Obstacle` base class and subclasses: `SmallCactus`, `LargeCactus`, `Bird`.
- Randomly spawned obstacles at runtime.
- Used `pygame.Rect` for bounding boxes.

### 5. **Clouds and Environment**
- Added randomly placed moving clouds to improve visual appeal.

### 6. **Collision Detection**
- Used `pygame.mask` to handle pixel-perfect collision between dino and obstacles.

### 7. **Score Tracking**
- Implemented a counter that increases with time and displays on screen.

### 8. **Human Gameplay Loop**
- Created a loop that processes user input (`UP`, `DOWN`, `SPACE`) and handles collision, score, and restart.

### 9. **NEAT AI Integration**
- Configured NEAT using `neat-config.txt`.
- Created and evolved generations of dinos.
- Fed each dino input parameters from the environment.
- Adjusted fitness based on survival time and penalty on collision.

### 10. **Debug Mode**
- Toggled with `D` key during gameplay.
- Shows green rectangles for dinos and red rectangles for obstacles.
- Also displays generation count, remaining dinos, and the AI's goal.

