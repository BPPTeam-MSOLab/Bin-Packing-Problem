from typing import List, Tuple, Callable, Optional
import numpy as np

class Problem:
    # An inner class to represent a bin and store information about the items placed in the bin
    class Bin:
        def __init__(self, size: Tuple[int]):
            self.size = size
            self.EMSs: List[List[Tuple[int]]] = [
                [(0, 0, 0), size] # Each EMS is a list of 2 tuples, the first one is always like this
            ]
            self.load = 0

        # Return the EMS is chosen to place the item based on Distance to Front-Top-Right Corner (FTR) rule
        def choose(self, item: Tuple[int]) -> Tuple[int]:
            max_distance = -1
            selected_EMS = None
            for EMS in self.EMSs:
                if self.fit(item, EMS):
                    x, y, z = EMS[0][0] + item[0], EMS[0][1] + item[1], EMS[0][2] + item[2]
                    distance = (self.size[0] - x) ** 2 + (self.size[1] - y) ** 2 + (self.size[2] - z) ** 2
                    if distance > max_distance:
                        max_distance = distance
                        selected_EMS = EMS
            return selected_EMS
        
        @staticmethod
        def fit(item: Tuple[int], EMS: List[Tuple[int]]) -> bool:
            for i in range(3):
                if EMS[0][i] + item[i] > EMS[1][i]:
                    return False
            return True

        @staticmethod
        def overlapped(EMS1: List[Tuple[int]], EMS2: List[Tuple[int]]) -> bool:
            return np.all(EMS1[0] < EMS2[1]) and np.all(EMS1[1] > EMS2[0]) # EMS1 is overlapped with EMS2
        
        @staticmethod
        def inscribed(EMS1: List[Tuple[int]], EMS2: List[Tuple[int]]) -> bool:
            return np.all(EMS1[0] >= EMS2[0]) and np.all(EMS1[1] <= EMS2[1]) # EMS1 is inscribed in EMS2

        # Update EMSs after placing the item into the chosen EMS
        def update(self, item: Tuple[int], selected_EMS: Tuple[int]) -> None:
            ems = [selected_EMS[0], (selected_EMS[0][0] + item[0], selected_EMS[0][1] + item[1], selected_EMS[0][2] + item[2])]

            for EMS in self.EMSs:
                if self.overlapped(ems, EMS):
                    self.EMSs.remove(EMS)

                    # New EMSs
                    x1, y1, z1 = EMS[0]
                    x2, y2, z2 = EMS[1]
                    x3, y3, z3 = ems[1]

                    new_EMSs = [
                        [(x3, y1, z1), (x2, y2, z2)],
                        [(x1, y3, z1), (x2, y2, z2)],
                        [(x1, y1, z3), (x2, y2, z2)],
                    ]

                    for new_EMS in new_EMSs:
                        isValid = True
                        for EMS in self.EMSs:
                            if self.inscribed(new_EMS, EMS):
                                isValid = False
                                break

                        if isValid:
                            self.EMSs.append(new_EMS)

            self.load += item[0] * item[1] * item[2]

    def __init__(self, path: str):
        self.path = path
        self.load_data()

        self.used_bins = self.n_bins
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
            orientation = self.get_orientation(solution[self.total_items + i])
            size = self.get_size(item, orientation)
            self.items[orders[i]] = size

    def evaluate(self, solution: List[float]) -> float:
        self.decode(solution)
        
        for item in self.items:
            selected_bin = None
            selected_EMS = None

            for bin in self.bins:
                EMS = bin.choose(item)
                if EMS is not None:
                    selected_bin = bin
                    selected_EMS = EMS
                    break

            if selected_bin is None:
                self.used_bins += 1
                self.bins.append(self.Bin(self.bin_size))
                selected_bin = self.bins[-1]
                selected_EMS = selected_bin.EMSs[0]

            selected_bin.update(item, selected_EMS)

        # Sum of load in first n_bins bins
        fitness = np.sum([bin.load for bin in self.bins[:self.n_bins]])
        return fitness    