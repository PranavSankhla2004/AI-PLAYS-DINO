# 🦖 Dino AI - NEAT Algorithm Implementation

![Dino Game Screenshot](screenshot.png) *(Replace with your screenshot)*  
*Figure 1: Dino AI in action*

![Debug Mode Screenshot](debug_screenshot.png) *(Replace with bounding boxes screenshot)*  
*Figure 2: Debug mode showing collision boxes and neural network inputs*

## 🚀 Overview

This project implements an AI agent that plays the Chrome Dino game using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm. The AI learns to jump over cacti and duck under birds through evolutionary algorithms, demonstrating the power of neuroevolution in game playing.

## ✨ Features

- **Complete Dino Game Implementation** with physics, collisions, and animations
- **NEAT AI Trainer** that evolves neural networks over generations
- **Human Playable Mode** with keyboard controls
- **Debug Visualization** showing decision-making inputs
- **Multiple Obstacle Types** (cacti and birds)
- **Configurable Parameters** for tuning the AI behavior

## 🧠 NEAT Algorithm Explained

NEAT (NeuroEvolution of Augmenting Topologies) is a genetic algorithm for evolving artificial neural networks. Key aspects:

1. **Evolutionary Approach**: Starts with simple networks and complexifies them
2. **Speciation**: Protects innovation through species formation
3. **Historical Marking**: Tracks genes through innovation numbers
4. **Minimal Initial Structure**: Begins with only input/output nodes

In this project, NEAT evolves networks that take game state as input and output jump/duck decisions.

## 🛠️ Technical Implementation

### Game Architecture

```python
class Dinosaur:
    # Handles dino physics, animations, and state
    # Implements jumping and ducking mechanics

class Obstacle:
    # Manages different obstacle types (cacti/birds)
    # Handles movement and collisions

class Game:
    # Main game loop controller
    # Manages both human and AI modes