class Problem:
    def __init__(self, path: str):
        self.path = path
        self.load_data()

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

if 11 < 3:
    problem = Problem('Data/Dataset/50_5_1.dat')