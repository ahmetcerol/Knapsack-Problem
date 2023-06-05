import time

start_time= time.time()

def knapsack(items, max_weight):
    n = len(items)
    prev = [0] * (max_weight + 1)
    curr = [0] * (max_weight + 1)

    for i in range(1, n + 1):
        value, weight = items[i - 1]
        value_per_weight = value / weight

        for w in range(1, max_weight + 1):
            if weight > w:
                curr[w] = prev[w]
            else:
                curr[w] = max(prev[w], prev[w - weight] + value_per_weight)

        prev = curr[:]
    
    optimal_value = curr[max_weight]
    selected_items = []

    w = max_weight
    for i in range(n, 0, -1):
        if curr[w] != prev[w]:
            selected_items.append(i - 1)
            w -= items[i - 1][1]

    selected_items.reverse()
    return optimal_value, selected_items

def dosyadan_oku(dosya_adi):
    with open(dosya_adi, "r") as f:
        max_items, max_weight = map(int, f.readline().split())
        items = []
        for line in f:
            value, weight = map(int, line.split())
            items.append((value, weight))
    return max_weight, items

def dosyaya_yaz(filename, optimal_value, selected_items,selected_indices,execution_time):
    with open(filename, "a") as f:
        f.write("\nOptimal value: {}\n".format(optimal_value))
        f.write("Selected items: {}\n".format(selected_items))
        f.write("Selected indices: {}\n".format(selected_indices))
        f.write("Time: {}\n".format(execution_time))

dosya_adi = "ks_10000_0.txt"
max_weight, items = dosyadan_oku(dosya_adi)

optimal_value, selected_items = knapsack(items, max_weight)

dosya_yolu = "knapsack_valueweight.txt"
end_time = time.time()
execution_time= end_time-start_time
selected_indices = [i for i in selected_items]

dosyaya_yaz(dosya_yolu, optimal_value, [1 if i in selected_items else 0 for i in range(len(items))],selected_indices,execution_time)

print("Çıktı dosyası '{}' olarak oluşturuldu.".format(dosya_yolu))
print("Optimal değer:", optimal_value)
print("Seçilen öğeler:", [1 if i in selected_items else " " for i in range(len(items))])

