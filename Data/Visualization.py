import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from Generator import generate_bin_packing_data
import seaborn as sns

def plot_boxes(items):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Create a color palette for items
    colors = sns.color_palette("Set3", len(items))
    
    for i, (origin, item) in enumerate(items):
        x0, y0, z0 = origin
        dx, dy, dz = item
        color = colors[i % len(colors)]
        plot_box(ax, x0, y0, z0, dx, dy, dz, color)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    # Set limits for the axes
    ax.set_xlim([0, 120])
    ax.set_ylim([0, 120])
    ax.set_zlim([0, 120])
    
    plt.show()

def plot_box(ax, x0, y0, z0, dx, dy, dz, color):
    vertices = [
        [x0, y0, z0], [x0 + dx, y0, z0], [x0 + dx, y0 + dy, z0], [x0, y0 + dy, z0],
        [x0, y0, z0 + dz], [x0 + dx, y0, z0 + dz], [x0 + dx, y0 + dy, z0 + dz], [x0, y0 + dy, z0 + dz]
    ]
    
    faces = [
        [vertices[j] for j in [0, 1, 5, 4]],
        [vertices[j] for j in [7, 6, 2, 3]],
        [vertices[j] for j in [0, 3, 7, 4]],
        [vertices[j] for j in [1, 2, 6, 5]],
        [vertices[j] for j in [0, 1, 2, 3]],
        [vertices[j] for j in [4, 5, 6, 7]]
    ]
    
    ax.add_collection3d(Poly3DCollection(faces, facecolors=color, linewidths=1, edgecolors='b', alpha=.75))

# Example of plotting boxes
items = generate_bin_packing_data(100, 1)
plot_boxes(items)
