import os
import pandas as pd



def sort_txt_file(input_file, output_file):
    """
    读取一个TXT文件，按指定的列进行排序，并将结果写入一个新的TXT文件。

    参数:
    - input_file: 输入文件的路径。
    - output_file: 输出文件的路径。
    """
    # 读取TXT文件到DataFrame
    df = pd.read_csv(input_file, header=None, sep=',')  # 假设数据是以逗号分隔的，没有标题行

    # 按第二列和第一列进行排序
    df_sorted = df.sort_values(by=[1, 0])

    # 将排序后的DataFrame写回到新的TXT文件
    df_sorted.to_csv(output_file, index=False, header=False, sep=',')



def calculate_weight(values):
    weight1 = values[0]+0.2*(values[1]+values[3])
    return weight1

def merge_text_files(file1, file2, output_file):
    """
    合并两个文本文件到一个新的输出文件中。

    参数:
    - file1: 第一个文件的路径。
    - file2: 第二个文件的路径。
    - output_file: 输出文件的路径。
    """
    # 打开第一个文件并读取内容
    with open(file1, 'r', encoding='utf-8') as f:
        content1 = f.readlines()

    # 打开第二个文件并读取内容
    with open(file2, 'r', encoding='utf-8') as f:
        content2 = f.readlines()

    # 将两个文件的内容合并，然后写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(content1)
        f.writelines(content2)




list=['02','04','05','09','10','11','13']
for id in list:
    timestamps = []  # 創建一個空列表來存放時間戳
    timestamps_to_index = {}  # 創建一個空字典來存放時間戳及其對應的索引值
    combined_results = []
    


# 開啟檔案並解析 "./mot17_val_post/data/MOT17-04-FRCNN.txt" 中的資料
    with open( f"./Difference_method03/MOT17-{id}-FRCNN.txt", 'r') as file:
        lines = file.readlines()

    # 解析每一行資料並進行比較
    for i in range(len(lines) - 1):
        current_line = lines[i].strip().split(',')
        next_line = lines[i + 1].strip().split(',')
        if next_line[1] != current_line[1]:
            continue

        # 如果後一項的 B[0] 與前一項的 A[0] 差距超過 2，則將 A[0] + 1 加入列表
        if abs(float(next_line[0]) - float(current_line[0])) > 1 and abs(float(next_line[0]) - float(current_line[0])) < 3:
            missing_frame=abs(float(next_line[0]) - float(current_line[0]))

           
            timestamp = int(current_line[0]) + 1
            timestamps.append(timestamp)
            timestamps_to_index[timestamp] = i+1  # 將時間戳及其對應的索引值存入字典
            values = [float(val) for val in current_line[2:]]  # 將數值轉換為浮點數
            result = calculate_weight(values)  # 計算權重

            # 在"./gmot_test_post/data/MOT17-04-FRCNN.txt"中找到最接近的權重行
            min_weight_line = None
            min_weight_diff = float('inf')
            with open(f"./tracks53_0.94/MOT17-{id}-FRCNN.txt", 'r') as gmot_file:
                gmot_lines = gmot_file.readlines()
                for gmot_line in gmot_lines:
                    gmot_current_line = gmot_line.strip().split(',')
                    gmot_timestamp = int(gmot_current_line[0])
                    if gmot_timestamp == timestamp:
                        gmot_values = [float(val) for val in gmot_current_line[2:]]
                        gmot_weight = calculate_weight(gmot_values)
                        weight_diff = abs(result - gmot_weight)
                        if weight_diff < min_weight_diff:
                            min_weight_diff = weight_diff
                            min_weight_line = gmot_line.strip()
            
            # 將兩行結合並添加到結果列表中
            combined_line =  min_weight_line.split(',')[:]
            combined_line[1] =current_line[1]
            combined_results.append(','.join(combined_line)) 
            timestamp = []  # 創建一個空列表來存放時間戳
            timestamp_to_index = {} # 創建一個空字典來存放時間戳及其對應的索引值
            while missing_frame!=2:
                 
                timestamp_in = int(combined_line[0]) + 1
                timestamp.append(timestamp_in)
                timestamp_to_index[timestamp_in] = i+1  # 將時間戳及其對應的索引值存入字典
                values = [float(val) for val in combined_line[2:]]  # 將數值轉換為浮點數
                result = calculate_weight(values)  # 計算權重
                # 在"./gmot_test_post/data/MOT17-04-FRCNN.txt"中找到最接近的權重行
                min_weight_line_in = None
                min_weight_diff_in = float('inf')
                with open(f"./tracks53_0.94/MOT17-{id}-FRCNN.txt", 'r') as gmot_file:
                    gmot_lines = gmot_file.readlines()
                    for gmot_line in gmot_lines:
                        gmot_current_line = gmot_line.strip().split(',')
                        gmot_timestamp = int(gmot_current_line[0])
                        if gmot_timestamp == timestamp:
                            gmot_values = [float(val) for val in gmot_current_line[2:]]
                            gmot_weight = calculate_weight(gmot_values)
                            weight_diff = abs(result - gmot_weight)
                            if weight_diff < min_weight_diff:
                                min_weight_diff = weight_diff
                                min_weight_line = gmot_line.strip()
                            
                # 將兩行結合並添加到結果列表中
                combined_line =  min_weight_line.split(',')[:]
                combined_line[1] =current_line[1]
                combined_results.append(','.join(combined_line)) 
                missing_frame=missing_frame-1
                # timestamp_in=timestamp_in+1
                        

    # 將結果寫入新的txt文件中
    if not os.path.exists("bestdata05"):
        os.makedirs("bestdata05")
    with open(f"./bestdata05/MOT17-{id}-FRCNN_combined.txt", 'w') as output_file:
        for line in combined_results:
            output_file.write(line + '\n')
    # 文件路径
    file1_path = f'./Difference_method03/MOT17-{id}-FRCNN.txt'
    file2_path = f'./bestdata05/MOT17-{id}-FRCNN_combined.txt'
    if not os.path.exists("Difference_method04"):
        os.makedirs("Difference_method04")
    output_file_path = f'./Difference_method04/MOT17-{id}-FRCNN.txt'  # 你可以自定义输出文件的名字

    # 调用函数执行合并
    merge_text_files(file1_path, file2_path, output_file_path)