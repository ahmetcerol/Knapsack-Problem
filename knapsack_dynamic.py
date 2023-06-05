import time

start_time = time.time()

def knapsack(items, max_weight):
    n = len(items)
    dp = [[0 for _ in range(max_weight+1)] for _ in range(n+1)]
    for i in range(1, n+1):
        value, weight = items[i-1]
        for w in range(max_weight+1):
            if weight > w:
                dp[i][w] = dp[i-1][w]
            else:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w-weight] + value)
    optimal_value = dp[n][max_weight]
    selected_items = []
    w = max_weight
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected_items.append(i-1)
            w -= items[i-1][1]
    selected_items.reverse()
    return optimal_value, selected_items

with open("ks-200_0_redesigned.txt", "r") as f:
    max_items, max_weight = map(int, f.readline().split())
    items = []
    for line in f:
        value, weight = map(int, line.split())
        items.append((value, weight))

optimal_value, selected_items = knapsack(items, max_weight)

def write_output_to_file(filename, optimal_value, selected_items,execution_time,selected_indices):
    with open(filename, "a") as f:
        f.write("\nOptimal value: {}\n".format(optimal_value))
        f.write("Selected items: {}\n".format(selected_items))
        f.write("Time: {}\n".format(execution_time))
        f.write("Selected indices: {} \n".format(selected_indices))

filename = "knapsack_dynamic.txt"
selected_indices = [i for i in selected_items]

end_time=time.time()
execution_time = end_time - start_time

write_output_to_file(filename, optimal_value, [1 if i in selected_items else 0 for i in range(len(items))],execution_time,selected_indices)
print("Çıktı dosyası '{}' olarak oluşturuldu.".format(filename))
print("Optimal value:", optimal_value)
print("Selected items:", [1 if i in selected_items else 0 for i in range(len(items))])
print("Selected item indices:", selected_indices)
print("Time:",execution_time)  

