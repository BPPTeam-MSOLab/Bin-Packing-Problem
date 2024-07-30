import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from typing import List, Tuple, Callable, Optional
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class Problem:
    def __init__(self, path: str):
        self.path = path
        self.load_data()
        self.total_items = self.n_items * self.n_bins
        self.used_bins = self.total_items
        self.loads = None
        self.best_fitness = np.inf
        self.solution: List[List[List[Tuple[int], Tuple[int]]]] = None

    def load_data(self):
        with open(self.path, 'r') as file:
            lines = file.readlines()
        
        self.bin_size = tuple(map(int, lines[0].split()[2:]))
        self.n_bins = int(lines[1].strip().split()[3])
        self.n_items = int(lines[2].strip().split()[5])
        self.total_volume = int(lines[3].strip().split()[4])
        self.items = []

        for line in lines[5:]:
            item = tuple(map(int, line.strip().split()))
            self.items.append(item)

        print(f'Loaded data from {self.path}')
        print(f'Problem: {self.n_items} items | {self.n_bins} bins | {self.bin_size} | {self.total_volume}')

    def visualize(self):
        if not self.solution:
            raise ValueError('No solution found')
        
        def plot_box(ax, x0: int, y0: int, z0: int, x1: int, y1: int, z1: int, color) -> None:
            dx, dy, dz = x1 - x0, y1 - y0, z1 - z0
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
            
            poly3d = Poly3DCollection(faces, facecolors=color, linewidths=0.5, edgecolors='k', alpha=0.2, zsort='average')
            ax.add_collection3d(poly3d)

        fig = plt.figure(figsize=(9, 5))
        ax = fig.add_subplot(111, projection='3d')

        # Create a color palette for items
        flat_items = [item for bin_items in self.solution for item in bin_items]
        colors = sns.color_palette("Set3", len(flat_items))

        item_count = 0
        for bin_idx, bin_items in enumerate(self.solution):
            bin_origin_x = bin_idx * self.bin_size[0]
            for item in bin_items:
                (x0, y0, z0), (x1, y1, z1) = item
                x0 += bin_origin_x
                x1 += bin_origin_x
                color = colors[item_count % len(colors)]
                plot_box(ax, x0, y0, z0, x1, y1, z1, color)
                item_count += 1

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # Set limits for the axes
        ax.set_xlim([0, self.bin_size[0] * self.used_bins])
        ax.set_ylim([0, self.bin_size[1]])
        ax.set_zlim([0, self.bin_size[2]])

        ax.title.set_text('3D Bin Packing Visualization')
        ax.set_box_aspect([self.bin_size[0] * self.used_bins, self.bin_size[1], self.bin_size[2]])
        
        # Add a legend with information
        info_text = (
            f'Bin size: {self.bin_size}\n'
            f'Number of bins: {self.used_bins}'
        )
        plt.figtext(0.75, 0.5, info_text, fontsize=8, ha='left', va='center', bbox=dict(facecolor='white', edgecolor='black'))

        plt.show()
    
class Placement:
    class Bin:
        def __init__(self, size: Tuple[int]):
            self.size = size
            self.EMSs: List[List[Tuple[int]]] = [
                [(0, 0, 0), size] # Each EMS is a list of 2 tuples, the first one is always like this
            ]
            self.items: List[List[Tuple[int]]] = []
            self.load = 0

        # Return the EMS is chosen to place the item based on Distance to Front-Top-Right Corner (FTR) rule
        def choose(self, item: Tuple[int]) -> Tuple[int]:
            max_distance = -1
            selected_EMS = None
            for EMS in self.EMSs:
                # print(f'Fit: {self.fit(item, EMS)} | Check: {self.check(item, EMS)}')
                if self.fit(item, EMS) and self.check(item, EMS): 
                    x, y, z = EMS[0][0] + item[0], EMS[0][1] + item[1], EMS[0][2] + item[2]
                    distance = (self.size[0] - x) ** 2 + (self.size[1] - y) ** 2 + (self.size[2] - z) ** 2
                    if distance > max_distance:
                        max_distance = distance
                        selected_EMS = EMS
            return selected_EMS
        
        # Check if the item can be placed into the chosen EMS
        def check(self, item: List[Tuple[int]], EMS: List[Tuple[int]]) -> bool:
            x1, y1, z1 = EMS[0]
            x2, y2, z2 = x1 + item[0], y1 + item[1], z1 + item[2]
            space = [(x1, y1, z1), (x2, y2, z2)]
            if not self.items: return True
            for other_item in self.items:
                if self.overlapped(space, other_item): return False # If the space is overlapped with other items
            return True
        
        @staticmethod
        def fit(item: Tuple[int], EMS: List[Tuple[int]]) -> bool:
            for i in range(3):
                if EMS[0][i] + item[i] > EMS[1][i]: return False
            return True
        
        @staticmethod
        def overlapped(item1: List[Tuple[int]], item2: List[Tuple[int]]) -> bool:
            return np.all(np.array(item1[0]) < np.array(item2[1])) and np.all(np.array(item1[1]) > np.array(item2[0])) # EMS1 and EMS2 are overlapped
        
        @staticmethod
        def inscribed(EMS1: List[Tuple[int]], EMS2: List[Tuple[int]]) -> bool:
            return np.all(np.array(EMS1[0]) >= np.array(EMS2[0])) and np.all(np.array(EMS1[1]) <= np.array(EMS2[1])) # EMS1 is inscribed in EMS2

        # Update EMSs after placing the item into the chosen EMS
        def update(self, item: Tuple[int], selected_EMS: Tuple[int]) -> None:
            x1, y1, z1 = selected_EMS[0]
            x2, y2, z2 = x1 + item[0], y1 + item[1], z1 + item[2]
            x3, y3, z3 = selected_EMS[1]

            self.items.append([(x1, y1, z1), (x2, y2, z2)])

            new_EMSs = [
                [(x2, y1, z1), (x3, y3, z3)],
                [(x1, y2, z1), (x3, y3, z3)],
                [(x1, y1, z2), (x3, y3, z3)]
            ]

            self.EMSs.remove(selected_EMS)
            for EMS in new_EMSs:
                isValid = True
                for i in range(3):
                    if EMS[0][i] >= EMS[1][i]:
                        isValid = False
                        break

                for other_EMS in self.EMSs:
                    if self.inscribed(EMS, other_EMS):
                        isValid = False
                        break

                if isValid:
                    self.EMSs.append(EMS)

            self.load += item[0] * item[1] * item[2]

    def __init__(self, problem: Problem):
        self.problem = problem
        self.bin_size = problem.bin_size
        self.n_bins = problem.n_bins
        self.n_items = problem.n_items
        self.total_volume = problem.total_volume
        self.items = problem.items

        self.used_bins = 1
        self.total_items = self.n_items * self.n_bins
        self.bins = [self.Bin(self.bin_size)]
        self.loads = None

    @staticmethod
    def get_orientation(gene: float) -> int:
        return int(np.ceil(6 * gene))
    
    @staticmethod
    def get_size(item: Tuple[int], orientation: int) -> Tuple[int]:
        x, y, z = item
        if   orientation == 1: return (x, y, z)
        elif orientation == 2: return (x, z, y)
        elif orientation == 3: return (y, x, z)
        elif orientation == 4: return (y, z, x)
        elif orientation == 5: return (z, x, y)
        elif orientation == 6: return (z, y, x)

    def decode(self, solution) -> None:
        if len(solution) != 2 * self.total_items:
            raise ValueError('Invalid solution length')
        
        orders = np.argsort(solution[:self.total_items])

        copy = self.items.copy()

        for i in range(self.total_items):
            item = copy[i]
            orientation = self.get_orientation(solution[self.total_items + i])
            size = self.get_size(item, orientation)
            # print(f'Item: {item} | Orientation: {orientation} | Size: {size} | Order: {orders[i]}')
            self.items[orders[i]] = size

    def evaluate(self, solution: List[float]) -> float:
        self.decode(solution)
        
        for item in self.items:
            selected_bin = None
            selected_EMS = None

            for bin in self.bins:
                # print(f'Bin index: {self.bins.index(bin)}')
                EMS = bin.choose(item)
                # print(f'Item: {item} | Selected EMS: {EMS}')
                if EMS is not None:
                    selected_bin = bin
                    selected_EMS = EMS
                    break

            if selected_bin is None:
                self.used_bins += 1
                self.bins.append(self.Bin(self.bin_size))
                selected_bin = self.bins[-1]
                selected_EMS = selected_bin.EMSs[0]

            # print(f'Item: {item} | Selected EMS: {selected_EMS} | Bin index: {self.bins.index(selected_bin)}')
            selected_bin.update(item, selected_EMS)
            if 11 < 3:
                print(f'Updated load: {selected_bin.load}')
                print(f'Updated EMSs: {selected_bin.EMSs}')
                print(f'Item: {item} | EMSs: {selected_bin.EMSs} | Bin index: {self.bins.index(selected_bin)}')

        self.loads = [bin.load for bin in self.bins]
        least_load = np.min(self.loads) / (self.bin_size[0] * self.bin_size[1] * self.bin_size[2])
        fitness = self.used_bins + least_load

        if fitness < self.problem.best_fitness:
            self.problem.used_bins = self.used_bins
            self.problem.best_fitness = fitness
            self.problem.loads = self.loads
            self.problem.solution = [bin.items for bin in self.bins]

        return fitness # To maximize the fitness
    
if 11 < 3:
    problem = Problem('Data/Dataset/test.dat')
    placement = Placement(problem)
    solution = np.random.rand(2 * problem.total_items)
    fitness = placement.evaluate(solution)
    print(f'Fitness: {fitness} | Used bins: {placement.used_bins} | Loads: {placement.problem.loads}')

if 11 < 3:
    np.random.seed(1)
    problem = Problem('Data/Dataset/20_1_1.dat')
    placement = Placement(problem)
    # solution = [i/problem.total_items for i in range(problem.total_items)] + [0.1 for _ in range(problem.total_items)]
    solution = np.random.rand(2 * problem.total_items)
    fitness = placement.evaluate(solution)
    print(f'Fitness: {fitness} | Used bins: {placement.used_bins} | Loads: {placement.problem.loads}')
    problem.visualize()
