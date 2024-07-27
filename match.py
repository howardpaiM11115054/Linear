import os
import pandas as pd



def sort_txt_file(input_file, output_file):
    """
    Read a TXT file, sort by the specified column, and write the results to a new TXT file.

     parameter:
     - input_file: The path of the input file.
     - output_file: The path of the output file.
    """
    # Read TXT file into DataFrame
    df = pd.read_csv(input_file, header=None, sep=',')  # Assume data is comma separated and no header row

    # Sort by second column and first column
    df_sorted = df.sort_values(by=[1, 0])

    # Write the sorted DataFrame back to a new TXT file
    df_sorted.to_csv(output_file, index=False, header=False, sep=',')



def calculate_weight(values):
    weight1 = values[0]+0.2*(values[1]+values[3])
    return weight1

def merge_text_files(file1, file2, output_file):
    """
    Merge two text files into a new output file.

     parameter:
     - file1: The path of the first file.
     - file2: The path of the second file.
     - output_file: The path of the output file.
    """
    # Open the first file and read the contents
    with open(file1, 'r', encoding='utf-8') as f:
        content1 = f.readlines()

    # Open the second file and read the contents
    with open(file2, 'r', encoding='utf-8') as f:
        content2 = f.readlines()

    # merge
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(content1)
        f.writelines(content2)




list=['02','04','05','09','10','11','13']
for id in list:
    timestamps = []  # Create an empty list to store timestamps
    timestamps_to_index = {}  # Create an empty dictionary to store timestamps and their corresponding index values
    combined_results = []
    # File path configuration
    input_file_path = f"./mot17_val/MOT17-{id}-FRCNN.txt"  # Enter a file name, make sure it is in the directory where the script is running or specify the correct path
    if not os.path.exists("verygood"):
        os.makedirs("verygood")
    output_file_path = f'./verygood/MOT17-{id}-FRCNN.txt'  # Output file name
    
    sort_txt_file(input_file_path, output_file_path)



    with open( f"./verygood/MOT17-{id}-FRCNN.txt", 'r') as file:
        lines = file.readlines()

    
    for i in range(len(lines) - 1):
        current_line = lines[i].strip().split(',')
        next_line = lines[i + 1].strip().split(',')
        if next_line[1] != current_line[1]:
            continue

    
        if abs(float(next_line[0]) - float(current_line[0])) > 1 and abs(float(next_line[0]) - float(current_line[0])) < 3:
            missing_frame=abs(float(next_line[0]) - float(current_line[0]))

           
            timestamp = int(current_line[0]) + 1
            timestamps.append(timestamp)
            timestamps_to_index[timestamp] = i+1 
            values = [float(val) for val in current_line[2:]] 
            result = calculate_weight(values)  

           
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
            
          
            combined_line =  min_weight_line.split(',')[:]
            combined_line[1] =current_line[1]
            combined_results.append(','.join(combined_line)) 
            timestamp = [] 
            timestamp_to_index = {}
            while missing_frame!=2:
                 
                timestamp_in = int(combined_line[0]) + 1
                timestamp.append(timestamp_in)
                timestamp_to_index[timestamp_in] = i+1 
                values = [float(val) for val in combined_line[2:]]  
                result = calculate_weight(values)  
              
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
                            
               
                combined_line =  min_weight_line.split(',')[:]
                combined_line[1] =current_line[1]
                combined_results.append(','.join(combined_line)) 
                missing_frame=missing_frame-1
                # timestamp_in=timestamp_in+1
                        

    
    if not os.path.exists("bestdata04"):
        os.makedirs("bestdata04")
    with open(f"./bestdata04/MOT17-{id}-FRCNN_combined.txt", 'w') as output_file:
        for line in combined_results:
            output_file.write(line + '\n')
   
    file1_path = f'./mot17_val/MOT17-{id}-FRCNN.txt'
    file2_path = f'./bestdata04/MOT17-{id}-FRCNN_combined.txt'
    if not os.path.exists("Difference_method03"):
        os.makedirs("Difference_method03")
    output_file_path = f'./Difference_method03/MOT17-{id}-FRCNN.txt'


    merge_text_files(file1_path, file2_path, output_file_path)
# merge_all(f"./tracks53_0.94")
