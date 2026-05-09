"""Tree packing optimization with simulated annealing."""
import json, random, numpy as np, argparse
from pathlib import Path
random.seed(42); np.random.seed(42)

def energy(positions, n_trees):
    """Compute packing density (lower is better)."""
    total_area = sum(np.pi * (0.5 + i*0.02)**2 for i in range(n_trees))
    bounding = max(p[0]+1 for p in positions) * max(p[1]+1 for p in positions)
    return bounding / (total_area + 1e-8)

def simulated_annealing(n_trees=20, n_steps=5000):
    positions = [(random.uniform(0, 10), random.uniform(0, 10)) for _ in range(n_trees)]
    best_e = energy(positions, n_trees); best_pos = positions[:]
    T = 10.0; history = []
    for step in range(n_steps):
        T *= 0.999
        i = random.randint(0, n_trees-1)
        new_pos = positions[:]; new_pos[i] = (positions[i][0]+random.gauss(0,T*0.1), positions[i][1]+random.gauss(0,T*0.1))
        new_e = energy(new_pos, n_trees)
        if new_e < best_e or random.random() < np.exp(-(new_e-best_e)/max(T,0.01)):
            positions = new_pos; best_e = min(best_e, new_e); best_pos = new_pos[:]
        if step % 500 == 0: history.append({"step": step, "energy": round(best_e, 4), "temp": round(T, 4)})
    return best_e, history

def main():
    p = argparse.ArgumentParser(); p.add_argument("--output_dir", default="outputs"); a = p.parse_args()
    out = Path(a.output_dir); out.mkdir(parents=True, exist_ok=True)
    best, hist = simulated_annealing()
    with open(out / "optimization_log.json", "w") as f: json.dump(hist, f, indent=2)
    print(f"\u2705 Packing Optimization")
    for h in hist: print(f"  Step {h['step']:5d}: energy={h['energy']:.4f} T={h['temp']:.4f}")
    print(f"\n  Final energy: {best:.4f}")

if __name__ == "__main__": main()
