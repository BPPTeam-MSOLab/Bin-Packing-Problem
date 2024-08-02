import os
import random
import matplotlib.pyplot as plt
import seaborn as sns

from typing import List, Tuple
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class Generator:
    def __init__(self, n_items: int, n_bins: int = 1, seed: int = 0, bin_size: List[int] = [100, 100, 100], **kwargs):
        """
        Parameters:
        :param n_items: Number of items to generate for each bin
        :param n_bins: Number of bins to generate
        :param seed: Seed for random number generator
        :param bin_size: Size of the bin in 3 dimensions
        :param n_samples: Number of samples to generate

        Note:
        - We will generate n_items + n_samples items for each bin and then remove n_samples topmost items
        - The remaining n_items items will be randomly reordered
        """
        self.n_items: int = n_items
        self.n_bins: int = n_bins
        self.seed: int = seed
        self.bin_size: List[int] = bin_size
        self.items: List[List[Tuple[List[int], List[int]]]] = []
        self.flat_items: List[Tuple[List[int], List[int]]] = None
        self.total_volume: int = 0

        if 'n_samples' in kwargs:
            self.n_samples: int = kwargs['n_samples']
            # Check if the number of samples is integer and between 0 and n_items
            if not isinstance(self.n_samples, int) or self.n_samples < 0 or self.n_samples > n_items:
                raise ValueError('Number of samples must be an integer between 0 and n_items')
        else:
            self.n_samples: int = n_items // 10

        if 'filename' in kwargs:
            self.filename: str = kwargs['filename']
        else:
            self.filename: str = f'Data/Dataset/{self.n_items}_{self.n_bins}_{self.seed}.dat'

    def generate(self) -> None:
        """
        Generate random items for all bins and write them to a file.
        """
        def generate_for_bin(bin_origin: List[int]) -> List[Tuple[List[int], List[int]]]:
            """
            Generate random items for a single bin.
            - We will generate items by recursively splitting the bin into 2 parts along the largest dimension.
            - We also keep track of the origin of each item (coordinates of the left-bottom-back corner) for visualization.
            """
            items = [(bin_origin, self.bin_size[:])]
            bin_volume = self.bin_size[0] * self.bin_size[1] * self.bin_size[2]

            for _ in range(self.n_items + self.n_samples - 1):
                (origin, item) = items.pop()
                
                # Choose the dimension with the largest size to split
                dimension: int = item.index(max(item))
                size: int = item[dimension]
                
                if size == 1:
                    items.append((origin, item))
                    continue
                
                # Randomly choose a cut point
                cut_point: int = random.randint(1, size - 1)
                
                # Create 2 new items after cutting
                new_item1: List[int] = item[:]
                new_item2: List[int] = item[:]
                new_item1[dimension] = cut_point
                new_item2[dimension] = size - cut_point
                
                # Create 2 new origins (coordinates of the left-bottom-back corner)
                new_origin1: List[int] = origin[:]
                new_origin2: List[int] = origin[:]
                new_origin2[dimension] += cut_point
                
                # Add new items to the list
                items.append((new_origin1, new_item1))
                items.append((new_origin2, new_item2))
                items.sort(key=lambda x: x[1][0] * x[1][1] * x[1][2])

            # Sort items by height to remove some topmost items
            items.sort(key=lambda x: x[0][2])
            for _ in range(self.n_samples):
                item = items.pop()
                bin_volume -= item[1][0] * item[1][1] * item[1][2]

            self.total_volume += bin_volume
            return items

        if self.n_items < 10 or self.n_items > 1000:
            raise ValueError('Number of items must be between 10 and 1000')
        
        random.seed(self.seed)

        self.items = []
        self.total_volume = 0

        for bin_index in range(self.n_bins):
            bin_origin = [bin_index * self.bin_size[0], 0, 0]
            bin_items = generate_for_bin(bin_origin)
            self.items.append(bin_items)
        
        # Flatten the list of items and reorder randomly
        self.flat_items = [item for bin_items in self.items for item in bin_items]
        random.shuffle(self.flat_items)
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(f'Data/Dataset/'), exist_ok=True)

        # Write data to file
        with open(self.filename, 'w') as file:
            file.write(f'Bin size: {self.bin_size[0]} {self.bin_size[1]} {self.bin_size[2]}\n')
            file.write(f'Number of bins: {self.n_bins}\n')
            file.write(f'Number of items per bin: {self.n_items}\n')
            file.write(f'Total volume of items: {self.total_volume}\n')
            file.write('Items:\n')
            for (_, item) in self.flat_items:
                sample = random.sample(item, 3)
                file.write(f'{sample[0]} {sample[1]} {sample[2]}\n')
    
    def visualize(self) -> None:
        """
        Visualize the generated items in a 3D plot.
        """
        def plot_box(ax, x0: int, y0: int, z0: int, dx: int, dy: int, dz: int, color) -> None:
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
            
            ax.add_collection3d(Poly3DCollection(faces, facecolors=color, linewidths=.3, edgecolors='k', alpha=.5, zsort='min'))

        if not self.items:
            raise ValueError('Items have not been generated yet')

        fig = plt.figure(figsize=(9, 5))
        ax = fig.add_subplot(111, projection='3d')

        # Create a color palette for items
        colors = sns.color_palette("pastel", len(self.flat_items))

        for i, (origin, item) in enumerate(self.flat_items):
            x0, y0, z0 = origin
            dx, dy, dz = item
            color = colors[i % len(colors)]
            plot_box(ax, x0, y0, z0, dx, dy, dz, color)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # Set limits for the axes
        ax.set_xlim([0, self.bin_size[0] * self.n_bins])
        ax.set_ylim([0, self.bin_size[1]])
        ax.set_zlim([0, self.bin_size[2]])

        ax.title.set_text(f'3D Bin Packing Visualization')
        ax.set_box_aspect([self.bin_size[0] * self.n_bins, self.bin_size[1], self.bin_size[2]])
        
        # Add a legend with information
        info_text = (
            f'Bin size: {self.bin_size}\n'
            f'Number of bins: {self.n_bins}\n'
            f'Number of items per bin: {self.n_items}\n'
            f'Total volume of items: {self.total_volume}'
        )
        plt.figtext(.8, .5, info_text, fontsize=8, ha='left', va='center', bbox=dict(facecolor='white', edgecolor='black'))

        plt.show()

    def delete(self) -> None:
        """
        Delete the generated data file.
        """
        os.remove(self.filename)

# Example of using the Generator class
if 11 < 3:
    for i in range(100):
        generator = Generator(50, 5, seed=i, bin_size=[100, 100, 100])
        generator.generate()
        generator.delete()

if 11 < 3:
    generator = Generator(20, 1, seed=1, bin_size=[10, 10, 10], n_samples=10)
    generator.generate()
    generator.visualize()
    # generator.delete()

if 11 < 3:
    generator = Generator(20, 5, seed=1, bin_size=[10, 10, 10], n_samples=5)
    generator.generate()
    # generator.visualize()
    # generator.delete()

if 11 < 3:
    Generator(20, 5, seed=2, bin_size=[10, 10, 10], n_samples=10).generate()
    
if 11 < 3:
    generator = Generator(100, 2, seed=4, bin_size=[100, 100, 100], filename='testcase.dat')
    generator.generate()
    generator.visualize()
    generator.delete()