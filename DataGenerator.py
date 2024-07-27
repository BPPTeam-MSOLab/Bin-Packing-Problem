import random

def generate_bin_packing_data(num_items, seed, num_samples=20):
    if num_items < 10 or num_items > 1000:
        raise ValueError('num_items must be in range [10, 1000]')
    
    random.seed(seed)

    # We assume that the bin has size 100×100×100
    x, y, z = 100, 100, 100
    x_cut, y_cut, z_cut = [random.randint(1, 99) for _ in range(3)]
    
    items = [
        [x_cut, y_cut, z_cut],
        [x - x_cut, y_cut, z_cut],
        [x_cut, y - y_cut, z_cut],
        [x_cut, y_cut, z - z_cut],
        [x - x_cut, y - y_cut, z_cut],
        [x - x_cut, y_cut, z - z_cut],
        [x_cut, y - y_cut, z - z_cut],
        [x - x_cut, y - y_cut, z - z_cut],
    ]
    
    for _ in range(num_items + num_samples):
        item = items.pop(random.randint(0, len(items) - 1))
        
        dimension = random.randint(0, 2)
        size = item[dimension]
        
        if size == 1:
            items.append(item)
            continue
        
        z = random.randint(1, size - 1)
        
        new_item1 = item.copy()
        new_item2 = item.copy()
        new_item1[dimension] = z
        new_item2[dimension] = size - z
        
        items.append(new_item1)
        items.append(new_item2)

    random.shuffle(items)

    volume = 1

    for _ in range(num_samples):
        item = items.pop()
        volume = volume - item[0] * item[1] * item[2] / 1000000
    
    filename = f'Data/{num_items}_{seed}.dat'
    with open(filename, 'w') as file:
        file.write(f'{num_items} {volume}\n')
        for item in items:
            file.write(f'{item[0]} {item[1]} {item[2]}\n')

for i in range(10):
    generate_bin_packing_data(100, i)
