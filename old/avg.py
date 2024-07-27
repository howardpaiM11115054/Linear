import os


def read_data(txt_path):
    with open(txt_path, "r") as file:
        lines = file.readlines()
    data = []
    for line in lines:
        values = line.strip().split(',')
        data.append(values)
    return data

def write_to_txt(data, path):
    fileroot = "idsilky"
    
    if not os.path.exists(fileroot):
        os.makedirs(fileroot)

    base_name = os.path.basename(path)
    name = os.path.splitext(base_name)[0]
    file_path = os.path.join(fileroot, name + ".txt")
    

    with open(file_path, "w") as f:
        for item in data:
            f.write(','.join(map(str, item)) + "\n")


def fill_missing_data(data):
    filled_data = []
    for i in range(len(data)):
        filled_data.append(data[i])
        if i > 0:
            diff = int(data[i][0]) - int(data[i-1][0])
            if diff > 1 and diff <= 2:
                prev_values = [float(data[i-1][k]) for k in [2, 3, 4, 5]]
                next_values = [float(data[i][k]) for k in [2, 3, 4, 5]]
                for j in range(1, diff):
                    new_frame = int(data[i-1][0]) + j
                    ratio = j / diff
                    avg_values = [(prev_values[l] * (1 - ratio) + next_values[l] * ratio) for l in range(len(prev_values))]
                    filled_data.append([str(new_frame), '1'] + [str(value) for value in avg_values]+ ['-1', '-1', '-1', '-1'])  # 将所有元素转换为字符串类型
    return sorted(filled_data, key=lambda x: int(x[1]))  # 按帧号排序

# # 示例数据
# data = [
#     ['1', '1', '560.82', '460.23', '18.88', '55.97', '-1', '-1', '-1', '-1'],
#     ['2', '1', '563.68', '460.96', '17.99', '55.33', '-1', '-1', '-1', '-1'],
#     ['4', '1', '562.86', '460.18', '18.22', '56.48', '-1', '-1', '-1', '-1'],
#     ['9', '1', '559.49', '458.86', '20.07', '57.65', '-1', '-1', '-1', '-1']
# ]
list=['02','04','05','09','10','11','13']
for id in list:
        # 读取数据文件
    path= f"./mot17_val_post/data/MOT17-{id}-FRCNN.txt"
    data=read_data(path)
    # 填充缺失的数据并重新排序
    filled_data = fill_missing_data(data)
    write_to_txt(filled_data,path)

# # 打印结果
# for item in filled_data:
#     print(','.join(item))
