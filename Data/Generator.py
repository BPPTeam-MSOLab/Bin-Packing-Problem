import random
import matplotlib.pyplot as plt
import seaborn as sns
import os
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class Generator:
    def __init__(self, n_items, seed=0, bin_size=[100, 100, 100]):
        self.n_items = n_items
        self.seed = seed
        self.bin_size = bin_size
        self.items = []
        self.volume = bin_size[0] * bin_size[1] * bin_size[2]

        self.n_samples = n_items // 10

    def generate(self):
        if self.n_items < 10 or self.n_items > 1000:
            raise ValueError('Number of items must be between 10 and 1000')
        
        random.seed(self.seed)

        # Initialize items with a single bin
        self.items = [([0, 0, 0], self.bin_size)]
        
        while len(self.items) < self.n_items + self.n_samples:
            (origin, item) = self.items.pop()
            
            # Choose the dimension with the largest size to split
            dimension = item.index(max(item))
            size = item[dimension]
            
            if size == 1:
                self.items.append((origin, item))
                continue
            
            # Randomly choose a cut point
            cut_point = random.randint(1, size - 1)
            
            # Create 2 new items after cutting
            new_item1 = item[:]
            new_item2 = item[:]
            new_item1[dimension] = cut_point
            new_item2[dimension] = size - cut_point
            
            # Create 2 new origins (that is coordinates of the left-bottom-back corner)
            new_origin1 = origin[:]
            new_origin2 = origin[:]
            new_origin2[dimension] += cut_point
            
            # Add new items to the list
            self.items.append((new_origin1, new_item1))
            self.items.append((new_origin2, new_item2))
            self.items.sort(key=lambda x: x[1][0] * x[1][1] * x[1][2])

        # Sort items by height to remove some topmost items
        self.items.sort(key=lambda x: x[0][2])
        residual = len(self.items) - self.n_items
        for _ in range(residual):
            item = self.items.pop()
            self.volume -= item[1][0] * item[1][1] * item[1][2]
        
        # Reorder items randomly
        random.shuffle(self.items)
        
        # Write data to file
        filename = f'Data/Dataset/{self.n_items}.{self.seed}.dat'
        with open(filename, 'w') as file:
            file.write(f'Bin size: {self.bin_size[0]} {self.bin_size[1]} {self.bin_size[2]}\n')
            file.write(f'Number of items: {self.n_items}\n')
            file.write(f'Total volume of items: {self.volume}\n')
            file.write('Items:\n')
            for (origin, item) in self.items:  # Chỉ lấy đúng số lượng vật phẩm cần thiết
                file.write(f'{item[0]} {item[1]} {item[2]}\n')
    
    def visualize(self):
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
            
            ax.add_collection3d(Poly3DCollection(faces, facecolors=color, linewidths=.5, edgecolors='k', alpha=.75))

        if not self.items:
            raise ValueError('Items have not been generated yet')

        fig = plt.figure(figsize=(9, 5))
        ax = fig.add_subplot(111, projection='3d')

        # Create a color palette for items
        colors = sns.color_palette("Set3", len(self.items))

        for i, (origin, item) in enumerate(self.items):
            x0, y0, z0 = origin
            dx, dy, dz = item
            color = colors[i % len(colors)]
            plot_box(ax, x0, y0, z0, dx, dy, dz, color)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # Set limits for the axes
        ax.set_xlim([0, self.bin_size[0]])
        ax.set_ylim([0, self.bin_size[1]])
        ax.set_zlim([0, self.bin_size[2]])

        ax.title.set_text(f'3D Bin Packing Visualization')
        ax.set_box_aspect(self.bin_size)
        
        # Add a legend with information
        info_text = (
            f'Bin size: {self.bin_size}\n'
            f'Number of items: {self.n_items}\n'
            f'Volume: {self.volume}'
        )
        plt.figtext(.75, .5, info_text, fontsize=8, ha='left', va='center', bbox=dict(facecolor='white', edgecolor='black'))

        plt.show()

    def delete(self):
        filename = f'Data/Dataset/{self.n_items}.{self.seed}.dat'
        os.remove(filename)

# Example of using the Generator class
generator = Generator(200, 1, bin_size=[100, 200, 150])
generator.generate()
generator.visualize()
generator.delete()

for i in range(100):
    generator = Generator(100, i, bin_size=[100, 100, 100])
    generator.generate()
