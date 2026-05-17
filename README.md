# Ant Colony Optimization — Traveling Salesman Problem

A Python implementation of **Ant Colony Optimization (ACO)** applied to the **Traveling Salesman Problem (TSP)**, with an interactive graphical interface to visualize the algorithm in action.

Developed as a two-person team project at **Centrale Lyon** (2023–2024).

## What It Does

Given a set of cities placed on a canvas, the algorithm finds a near-optimal tour that visits every city exactly once and returns to the starting point — the classic TSP. The solution method is inspired by the foraging behavior of real ants:

- Ants explore the graph and deposit **pheromones** on the edges they travel
- Shorter paths accumulate more pheromone (evaporation penalizes long routes)
- Over successive iterations, ants converge toward the shortest tour found

## Algorithm

The ACO implementation follows the Ant System (AS) model:

- **Probabilistic path selection** — each ant chooses its next city based on pheromone intensity (α) and inverse distance (β)
- **Pheromone evaporation** — after each iteration, all edges lose a fraction of their pheromone
- **Pheromone deposit** — ants reinforce edges proportionally to the quality of their tour (Q / tour length)
- **Taboo list** — prevents revisiting already-visited cities within a single tour

## Interface

The Tkinter GUI lets you:

- Place cities interactively on the canvas by clicking
- Adjust ACO parameters (number of ants, α, β, evaporation rate, Q)
- Watch the algorithm converge in real time
- View the evolution of the best tour length across iterations

## Tech Stack

- **Python** — core algorithm
- **Tkinter** — interactive GUI
- **NetworkX** — graph representation
- **Matplotlib** — convergence charts and visualization

## Run

```bash
pip install networkx matplotlib
python Interface.py
```

## Team

Carl-Henri Gegout · Clément Guilhaumon
