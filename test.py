import matplotlib.pyplot as plt
import numpy as np

# --- Sample data --- 
# We have 2 groups (Group1 and Group2), each with 3 bars, and each bar has 2 stacked segments
group_labels = ["Group 1", "Group 2"]  # only 2 groups
bars_per_group = 3

# Each bar has 2 segments
group1_data = [
    (3, 2),   # Bar 1 in Group 1: Segment1=3, Segment2=2
    (4, 1),   # Bar 2 in Group 1
    (2, 3),   # Bar 3 in Group 1
]
group2_data = [
    (5, 2),   # Bar 1 in Group 2
    (3, 4),   # Bar 2 in Group 2
    (6, 1),   # Bar 3 in Group 2
]

# We'll store these in a list of lists for convenience
all_group_data = [group1_data, group2_data]

# Segment labels and colors (for stacked segments)
segment_labels = ["Segment A", "Segment B"]
segment_colors = ["blue", "green"]

# --- Plot configuration ---
bar_width = 0.5
gap_between_groups = 1.0  # horizontal gap between the last bar of one group and first bar of the next

# We'll compute x positions for each group
x_positions = []  # will hold the x for each bar in each group

current_x = 0
for _ in range(len(group_labels)):
    # For each group, the bars will occupy 'bars_per_group' x positions
    positions_for_this_group = np.arange(current_x, current_x + bars_per_group)
    x_positions.append(positions_for_this_group)
    # Move current_x to the right by 'bars_per_group' plus the gap
    current_x += bars_per_group + gap_between_groups

# x_positions is now a list of arrays,
# e.g. [ array([0,1,2]), array([4,5,6]) ] if gap=1.0 and bars_per_group=3

# --- Drawing the bars ---
plt.figure(figsize=(8, 5))  # optional, just to size the figure nicely

for group_idx, group_data in enumerate(all_group_data):
    positions_for_group = x_positions[group_idx]
    for bar_idx, (seg1, seg2) in enumerate(group_data):
        x_center = positions_for_group[bar_idx]
        
        # Plot first segment
        plt.bar(
            x_center,
            seg1,
            width=bar_width,
            color=segment_colors[0],
            label=segment_labels[0] if (group_idx == 0 and bar_idx == 0) else None
        )
        # Plot second segment (stacked on top)
        plt.bar(
            x_center,
            seg2,
            width=bar_width,
            bottom=seg1,
            color=segment_colors[1],
            label=segment_labels[1] if (group_idx == 0 and bar_idx == 0) else None
        )

# To label the center of each group, we can place an xtick in the middle of the group
group_centers = []
for positions_for_group in x_positions:
    # The center of the group is the average of the leftmost and rightmost bar positions
    leftmost = positions_for_group[0]
    rightmost = positions_for_group[-1]
    center = (leftmost + rightmost) / 2
    group_centers.append(center)

plt.xticks(group_centers, group_labels)

plt.title("Multiple Groups of Bars with Gaps")
plt.xlabel("Groups")
plt.ylabel("Value")
plt.legend()
plt.show()
