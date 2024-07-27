import random

def generate_bin_packing_data(n_items, seed=0, n_samples=5, bin_size = [100, 100, 100]):
    if n_items < 10 or n_items > 1000:
        raise ValueError('Number of items must be between 10 and 1000')
    
    random.seed(seed)

    # Initialize items with a single bin
    items = [([0, 0, 0], bin_size)]
    
    while len(items) < n_items + n_samples:
        (origin, item) = items.pop()
        
        # Choose the dimension with the largest size to split
        dimension = item.index(max(item))
        size = item[dimension]
        
        if size == 1:
            items.append((origin, item))
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
        items.append((new_origin1, new_item1))
        items.append((new_origin2, new_item2))
        items.sort(key=lambda x: x[1][0] * x[1][1] * x[1][2])

    # Sort items by height to remove some topmost items
    items.sort(key=lambda x: x[0][2])
    residual = len(items) - n_items
    volume = bin_size[0] * bin_size[1] * bin_size[2]
    for _ in range(residual):
        item = items.pop()
        volume -= item[1][0] * item[1][1] * item[1][2]
    
    # Reorder items randomly
    random.shuffle(items)
    
    # Write data to file
    filename = f'Data/Dataset/{n_items}.{seed}.dat'
    with open(filename, 'w') as file:
        file.write(f'{n_items} {volume}\n')
        for (origin, item) in items:  # Chỉ lấy đúng số lượng vật phẩm cần thiết
            file.write(f'{item[0]} {item[1]} {item[2]}\n')
    
    return items

# Generate data for bin packing problem with 100 items
for i in range(100):
    generate_bin_packing_data(100, i)
