import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random


# Simple Reflex Rule: Sirf current percept (ghost_here) dekh kar turant action
def pac_reflex_rule(ghost_here: bool) -> str:
    if ghost_here:
        return "DODGE_GHOST"   # Ghost dikha -> turant dodge / evade step lo
    return "PATROL_SAFE"     # Ghost nahi hai -> normal patrol karo


plt.ion()
fig, ax = plt.subplots(figsize=(6, 4.5))

# 4 zones: (x, y, name, ghost_present)
zones = [
    (0.0, 0.5, "ZoneA", False),
    (0.5, 0.5, "ZoneB", True),
    (0.0, 0.0, "ZoneC", False),
    (0.5, 0.0, "ZoneD", False),
]

idx = 0
for step in range(1, 15):
    # Har step mein randomly kisi zone mein ghost aa sakta hai ya hat sakta hai
    for i in range(4):
        x, y, name, _ = zones[i]
        ghost_now = random.random() < 0.35
        zones[i] = (x, y, name, ghost_now)

    # Pac-Bot agli zone check karta hai aur wahi ke current ghost percept par reflex action leta hai
    idx = (idx + 1) % 4
    x, y, name, ghost = zones[idx]
    action = pac_reflex_rule(ghost)

    if action == "DODGE_GHOST":
        # Safe neighbor zone mein turant dodge karke shift ho jaata hai
        safe_indices = [i for i, z in enumerate(zones) if not z[3] and i != idx]
        if safe_indices:
            idx = safe_indices[0]
            x, y, name, ghost = zones[idx]
        status_label = f"Step {step} — Ghost! Dodged to {name}"
    else:
        status_label = f"Step {step} — {name}: Safe -> Patrolling"

    ax.clear()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])

    for zx, zy, zname, zghost in zones:
        color = "#dc2626" if zghost else "#15803d"  # Red = Ghost, Green = Safe
        ax.add_patch(
            patches.Rectangle(
                (zx, zy), 0.5, 0.5, facecolor=color, edgecolor="black", linewidth=1.5
            )
        )
        tag = "GHOST!" if zghost else "SAFE"
        ax.text(
            zx + 0.25,
            zy + 0.25,
            f"{zname}\n[{tag}]",
            color="white",
            ha="center",
            va="center",
            fontsize=10,
        )

    # Blue circle = Ghost Dodge Pac-Bot Agent
    ax.add_patch(
        patches.Circle(
            (x + 0.25, y + 0.25),
            0.06,
            facecolor="#1d4ed8",
            edgecolor="white",
            linewidth=1.5,
        )
    )
    ax.set_title(status_label, fontsize=10)
    print(f"[Step {step}] {status_label}")

    plt.draw()
    plt.pause(1.2)

plt.ioff()
plt.show()
