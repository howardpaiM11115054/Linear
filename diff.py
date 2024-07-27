import os
import pandas as pd
def sort_txt_file(input_file, output_file):
    
    df = pd.read_csv(input_file, header=None, sep=',')  

    df_sorted = df.sort_values(by=[1, 0])

    df_sorted.to_csv(output_file, index=False, header=False, sep=',')

def calculate_weight(values):
    # It is assumed here that the weight calculation is simple and can be adjusted according to your actual needs.
    return values[0]

def interpolate_frames(lines, start_index, end_index, start_frame, end_frame):
    
    interpolated_lines = []
    num_frames = end_frame - start_frame - 1
    step = [(float(end_line) - float(start_line)) / (num_frames + 1) for start_line, end_line in zip(lines[start_index].split(',')[2:], lines[end_index].split(',')[2:])]
    current_values = [float(value) for value in lines[start_index].split(',')[2:]]
    
    for i in range(1, num_frames + 1):
        new_frame = start_frame + i
        current_values = [value + delta for value, delta in zip(current_values, step)]
        interpolated_line = [str(new_frame), lines[start_index].split(',')[1]] + [str(x) for x in current_values]
        interpolated_lines.append(','.join(interpolated_line))
    return interpolated_lines

def main():
    ids = ['02', '04', '05', '09', '10', '11', '13']
    for id in ids:
        input_file_path = f"./goal/MOT17-{id}-FRCNN.txt"
        output_file_path = f"./traget/MOT17-{id}-FRCNN.txt"
        if not os.path.exists("verygood02"):
            os.makedirs("verygood02")
        sort_txt_file(input_file_path, output_file_path)

        with open(output_file_path, 'r') as file:
            lines = file.readlines()

        combined_results = []
        i = 0
        while i < len(lines) - 1:
            current_line = lines[i].strip().split(',')
            next_line = lines[i + 1].strip().split(',')
            if int(next_line[0]) - int(current_line[0]) > 1:
                missing_frames = int(next_line[0]) - int(current_line[0]) - 1
                interpolated_lines = interpolate_frames(lines, i, i + 1, int(current_line[0]), int(next_line[0]))
                combined_results.extend(interpolated_lines)
            combined_results.append(lines[i].strip())
            i += 1

        # add last line
        combined_results.append(lines[-1].strip())

        # Write results to new file
        if not os.path.exists("bestdata08"):
            os.makedirs("bestdata08")
        with open(f"./bestdata08/MOT17-{id}-FRCNN.txt", 'w') as output_file:
            for line in combined_results:
                output_file.write(line + '\n')

if __name__ == "__main__":
    main()
