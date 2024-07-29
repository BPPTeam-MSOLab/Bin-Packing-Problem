from typing import List, Tuple, Callable, Optional
import numpy as np

class Problem:
    # An inner class to represent a bin and store information about the items placed in the bin
    class Bin:
        def __init__(self, size: Tuple[int]):
            self.size = size
            self.EMSs: List[Tuple[int]] = [(0, 0, 0), size]
            self.load = 0

        # Return the EMS is chosen to place the item based on Distance to Front-Top-Right Corner (FTR) rule
        def choose(self, item: Tuple[int]) -> Tuple[int]:
            return None

        # Update EMSs after placing the item into the chosen EMS
        def update(self, item: Tuple[int], EMS: Tuple[int]) -> None:
            self.load += item[0] * item[1] * item[2]
            pass

    def __init__(self, path: str):
        self.path = path
        self.load_data()
        self.total_items = self.n_items * self.n_bins
        self.bins = [self.Bin(self.bin_size) for _ in range(self.n_bins)] 

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

        for i in range(self.total_items):
            item = self.items[i]
            orientation = self.get_orientation(self.solution[self.total_items + i])
            size = self.get_size(item, orientation)
            self.items[orders[i]] = size

    def evaluate(self, solution: List[float]) -> float:
        self.decode(solution)
        
        for item in self.items:
            selected_bin = None
            selected_EMS = None

            for i, bin in enumerate(self.bins):
                EMS = bin.choose(item)
                if EMS is not None:
                    selected_bin = bin
                    selected_EMS = EMS
                    break

            if selected_bin is None:
                self.bins.append(self.Bin(self.bin_size))
                selected_bin = self.bins[-1]
                selected_EMS = selected_bin.EMSs[0]

            self.bins[i].update(item, selected_EMS)

        # Sum of load in first n_bins bins
        fitness = np.sum([bin.load for bin in self.bins[:self.n_bins]])
        return fitness


        

    