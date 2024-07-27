import pandas as pd
from scipy.optimize import linear_sum_assignment
import os
import shutil

def write_to_txt(data, path):
    fileroot=f"root"
    
    base_name = os.path.basename(path)
    name = os.path.splitext(base_name)[0]
    if not os.path.exists(fileroot):
        os.makedirs(fileroot)
    #創立雙資料夾

    if os.path.exists(os.path.join(fileroot, name)):
        name += "_target"
    if not os.path.exists(os.path.join(fileroot, name)):
        os.makedirs(os.path.join(fileroot, name))

    for id, content in data.items():
        id_folder = os.path.join(fileroot,name, str(id))
        if not os.path.exists(id_folder):
            os.makedirs(id_folder)

        with open(os.path.join(id_folder, f"{id}.txt"), "w") as f:
            # 写入标题行
            # f.write("frame,id,PLS_left,PLS_top,PLS_width,PLS_height,conf,x,y,z\n")
            # 写入每一行数据
            for item in content:
                f.write(','.join(map(str, item)) + "\n")

def data(path):
    with open(path, "r") as file:
        lines = file.readlines()
    data = {}
    for line in lines[1:]:  # 跳过标题行
        values = line.strip().split(',')
        id = values[1]
        if id not in data:
            data[id] = []
        data[id].append(values)
    
    return data

def write_to_txt_spilt_id(data, path):
    fileroot=f"root"
    folder_name = "spilt_id_"+os.path.basename(path).split('.')[0]

    # 如果文件夹已存在，则在文件夹名称后添加"_target"
    if os.path.exists(os.path.join(fileroot,folder_name)):
        folder_name += "_target"
    
    # 创建文件夹
    os.makedirs(os.path.join(fileroot,folder_name), exist_ok=True)

    # 写入数据到对应的文件夹中
    for id, content in data.items():
        file_path = os.path.join(fileroot,folder_name, f"{id}.txt")
        with open(file_path, "w") as f:
            for item in content:
                f.write(','.join(map(str, item)) + "\n")

def MOT_spilt_id(path):
    with open(path, "r") as file:
        lines = file.readlines()
    
    data = {}
    for line in lines[1:]:  # 跳过标题行
        values = line.strip().split(',')
        id = values[1]
        if id not in data:
            data[id] = []
        data[id].append(values)
    
    return data
def calculate_weights(team1, team2):
    # 转换数据为DataFrame
    df1 = pd.DataFrame(team1, columns=["id","frame","PLS_left","PLS_top","PLS_width","PLS_height","conf","x","y","z"])
    df2 = pd.DataFrame(team2, columns=["id","frame","PLS_left","PLS_top","PLS_width","PLS_height","conf","x","y","z"])


    # 将DataFrame的值转换为字典
    # team1_dict = dict(df1.values.tolist())
    # team2_dict = dict(df2.values.tolist())
    team1_dict=df1.set_index('id', inplace=True)
    team2_dict=df2.set_index('id', inplace=True)

    # 执行权重计算
    result = []
    for idx1, row1 in df1.iterrows():
        row_result = []
        for idx2, row2 in df2.iterrows():
            weight = abs((row2["frame"])+row2['PLS_left']+row2["PLS_top"] +(0.2*row1["PLS_width"])-(row1["frame"])- row1['PLS_left']-row1["PLS_top"]-(0.2*row1["PLS_width"]))
            # weight = abs(row2['PLS_left']- row1['PLS_left'])
            row_result.append(weight)
        result.append(row_result)
    
    return result

def copy_files(source_folder, target_folder, file_names):
    # 确保目标文件夹存在
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # 循环复制指定的文件
    for index, file_name in enumerate(file_names, start=1):
        # 创建与索引相对应的文件夹
        index_folder = os.path.join(target_folder, str(index))
        if not os.path.exists(index_folder):
            os.makedirs(index_folder)

        # 复制文件到对应的文件夹中
        source_file_path = os.path.join(source_folder, f"{file_name}.txt")
        target_file_path = os.path.join(index_folder, f"{file_name}.txt")
        # shutil.copy(source_file_path, target_file_path)
        if os.path.exists(source_file_path):
            # 构建目标文件路径并复制文件
            target_file_path = os.path.join(index_folder, f"{file_name}.txt")
            shutil.copy(source_file_path, target_file_path)
        else:
            print(f"File not found: {source_file_path}")






def loadtxt(path):
    
    Column_num=["frame","id","PLS_left","PLS_top","PLS_width","PLS_height","conf","x","y","z"]
    df=pd.read_csv(path,header=None)
    df.columns=Column_num

    df.set_index(Column_num)

    result=df.groupby("id", as_index=False).mean()
    # result.to_csv('datasave.txt', sep='\t', index=False)
   

    folder_path = f"./save"
    if not os.path.exists(folder_path):
         os.makedirs(folder_path)


    name= os.path.basename(path)
    name=name.split('.')[0]
    # print(name)
    with open(os.path.join(folder_path, f"{name}.txt"), "w") as f:
            
       result.to_csv(os.path.join(folder_path, f"{name}.txt"))
    

    return result

def match(filename):

    if filename.endswith(".txt"):
        #match the data
        print()
def merge_txt_files(folder_path):
    # 获取文件夹中的所有TXT文件路径
    txt_files = [file for file in os.listdir(folder_path) if file.endswith('.txt')]
    
    # 读取所有TXT文件并合并
    df_merged = pd.DataFrame()
    for file in txt_files:
        df = pd.read_csv(os.path.join(folder_path, file), header=None)
        df_merged = pd.concat([df_merged, df])
    # print(folder_path, file)
   
    # 保存合并后的数据为新的TXT文件
    # long= folder_path.count('/')
    # print(len)
    name= os.path.basename(folder_path)
    df_merged[1]=id
    file_name = os.path.split(os.path.dirname(folder_path))[-1]
    # print(file_name)
    
    if not os.path.exists("./{}_final".format(file_name)):
        os.makedirs("./{}_final".format(file_name))
   
   
    # print(id)
    # 去除重复行
    df_merged.drop_duplicates(subset=[0,1],inplace=True)
    df_merged=df_merged.sort_values(by=[1,0])
    df_merged.to_csv(os.path.join(file_name+'_final',"{}.txt".format(name)), index=False, header=False)


def merge_all(folder_path,id_final):
    # 获取文件夹中的所有TXT文件路径
    txt_files = [file for file in os.listdir(folder_path) if file.endswith('.txt')]
    
    # 读取所有TXT文件并合并
    df_merged = pd.DataFrame()
    for file in txt_files:
        df = pd.read_csv(os.path.join(folder_path, file), header=None)
        df_merged = pd.concat([df_merged, df])
    # print(folder_path, file)
   
    

   
    
    # 保存合并后的数据为新的TXT文件
    # long= folder_path.count('/')
    # print(len)
    name= os.path.basename(folder_path)
    df_merged[1]=id_final
    file_name = os.path.split(os.path.dirname(folder_path))[-1]
    # print(file_name)
    
    if not os.path.exists("./{}_final".format(file_name)):
        os.makedirs("./{}_final".format(file_name))
   
   
    # print(id)
    # 去除重复行
    df_merged.drop_duplicates(subset=[0,1],inplace=True)
    df_merged=df_merged.sort_values(by=[1,0])
    df_merged.to_csv(os.path.join(file_name+'_final',"{}.txt".format(name)), index=False, header=False) 
def merge_txt_files(folder_path):
    # 获取文件夹中的所有TXT文件路径
    txt_files = [file for file in os.listdir(folder_path) if file.endswith('.txt')]
    
    # 读取所有TXT文件并合并
    df_merged = pd.DataFrame()
    for file in txt_files:
        df = pd.read_csv(os.path.join(folder_path, file), header=None)
        df_merged = pd.concat([df_merged, df])
   
    
    
    # 保存合并后的数据为新的TXT文件
    file_name = os.path.basename(folder_path)
    file_name = file_name.split("_")[0]
    if not os.path.exists("./merged_final"):
         os.makedirs("./merged_final")
    # 去除重复行
    df_merged.drop_duplicates(inplace=True)
    df_merged=df_merged.sort_values(by=[1,0])
    df_merged.to_csv(os.path.join("./merged_final", f"{file_name}.txt"), index=False, header=False)


def main():
    #step1 形成每個ID的獨立資料夾
   
    list=['02','04','05','09','10','11','13']
    for id in list:
        # 读取数据文件
        # path_target = f"./mot17_val_post/tracks53_0.94/MOT17-{id}-FRCNN.txt"
        # path = f"./gmot_test_post/data/MOT17-{id}-FRCNN.txt"
        path = f"./mot17_val_post/tracks53_0.94/MOT17-{id}-FRCNN.txt"
        path_target = f"./gmot_test_post/data/MOT17-{id}-FRCNN.txt"
        # # # # 解析数据
        mot_data = data(path)
        target_mot_data = data(path_target)
        write_to_txt(mot_data, path)
        write_to_txt(target_mot_data, path_target)
    ###########################################################################################################################
    #step2 txt中的分開ID
    list=['02','04','05','09','10','11','13']
    for id in list:
        # 读取数据文件
        path_target = f"./mot17_val_post/tracks53_0.94/MOT17-{id}-FRCNN.txt"
        path = f"./gmot_test_post/data/MOT17-{id}-FRCNN.txt"
        # path_target = f"C:/Users/er050/Desktop/MOTMATCH/mot17_val_post/data/MOT17-{id}-FRCNN.txt"
        # path = f"C:/Users/er050/Desktop/MOTMATCH/gmot_test_post/data/MOT17-{id}-FRCNN.txt"
        # # 解析数据
        mot_data = MOT_spilt_id(path)
        target_mot_data = MOT_spilt_id(path_target)
        write_to_txt_spilt_id(mot_data, path)
        write_to_txt_spilt_id(target_mot_data, path_target)   
    ###########################################################################################################################
    # 匈牙利演算法
    for id in list:
        # path1=f'./mot17_val_post/data/MOT17-{id}-FRCNN.txt'
        # data1=loadtxt(path1)
        # path2=f'./gmot_test_post/data/MOT17-{id}-FRCNN.txt'
        # data2=loadtxt(path2)
        path2=f'./mot17_val_post/tracks53_0.94/MOT17-{id}-FRCNN.txt'
        data2=loadtxt(path2)
        path1=f'./gmot_test_post/data/MOT17-{id}-FRCNN.txt'
        data1=loadtxt(path1)

        result = calculate_weights(data1, data2)
            # print(result)
            # with open('C:/Users/er050/Desktop/paper/matrix.txt', 'w') as f:
            #  f.write(str(result))
        row_ind,col_ind=linear_sum_assignment(result)
        col_ind+=1
            # print(col_ind)
        col_ind_new = [str(item) for item in col_ind]#改格式[126 1 5.....]=>['126','1','5'......]

        source_folder = f'./root/spilt_id_MOT17-{id}-FRCNN'
        target_folder = f'./root/MOT17-{id}-FRCNN_target'#目的地
        file_names = col_ind_new

        copy_files(source_folder, target_folder, file_names)
    ###########################################################################################################################    
    for num in list:
        for id_final in os.listdir(f'./root/MOT17-{num}-FRCNN_target'):
            merge_all(os.path.join(f'./root/MOT17-{num}-FRCNN_target', id_final),id_final)
    ###########################################################################################################################
    for num in list:  
       # 指定要合并的文件夹路径
        folder_path = f'./MOT17-{num}-FRCNN_target_final'
        
        # 调用函数合并所有txt文件
        merge_txt_files(folder_path)       
     
    

if __name__ == "__main__":
    main()