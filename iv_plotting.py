import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import ListedColormap
from cycler import cycler

font_size = 13
np.set_printoptions(suppress=True)
plt.rcParams.update({"text.usetex": True,
                     "font.size": font_size})
plt.rc('font', family='serif')
plt.rc('text', usetex=True)

def read_data(file_path):
    bias_data = []
    current_data = []
    
    with open(file_path, 'r') as file:
        # Skip the first line
        next(file)
        
        for line in file:
            try:
                # Split the line into bias and current values
                bias, current = line.split()
                # Convert to float and append
                bias_data.append(float(bias))
                current_data.append(float(current))
            except ValueError:
                # If the line can't be split into two values, skip it
                continue

    # Convert lists to numpy arrays and return
    bias_array = np.array(bias_data, dtype=np.float64)
    current_array = np.array(current_data, dtype=np.float64)
    
    return bias_array, current_array

# Function to convert values to scientific naming convention and scale
def convert_to_prefix(data):
    # Extended prefixes with LaTeX symbols
    prefixes = { 
        -15: r'$\mathrm{f}$',  # femto
        -12: r'$\mathrm{p}$',  # pico
        -9: r'$\mathrm{n}$',   # nano
        -6: r'$\mu$',          # micro (using LaTeX \mu for micro)
        -3: r'$\mathrm{m}$',   # milli
        0: '',                  # no prefix for base units
        3: r'$\mathrm{k}$',    # kilo
        6: r'$\mathrm{M}$',    # mega
        9: r'$\mathrm{G}$',    # giga
        12: r'$\mathrm{T}$',   # tera
        15: r'$\mathrm{P}$'    # peta
    }

    # Find the scaling factor to adjust the data to a reasonable range
    min_value = np.min(data)
    max_value = np.max(data)

    # Find the power of 10 closest to the values in the data
    power_10 = np.floor(np.log10(abs(min_value))) if abs(min_value) < abs(max_value) else np.floor(np.log10(abs(max_value)))
   
    power_3 = np.floor(power_10/3) * 3
       
    # Get the corresponding LaTeX prefix
    prefix = prefixes.get(power_3, '')
    data_scaled = data / (10 ** power_3)

    return data_scaled, prefix

def choose_option():
    # List of options
    options = ["Option 0: Plot one set of IV Data", 
               "Option 1: Plot selection of IV Data", 
               "Option 2: Plot all IV Data"]

    # Print available options
    print("Please choose one of the following options:")
    for option in options:
        print(option)

    # Get user input
    choice = input("Enter the number of your choice: ")

    # Validate choice
    if choice.isdigit() and int(choice) in range(len(options)):
        print(f"You chose: {options[int(choice)]}")
    else:
        print("Invalid choice, please choose a valid option.")
        choose_option()
    print("")
    return int(choice)

def choose_directory():
    # Define the path to the subdirectory called 'data'
    base_path = "data"
    
    # Check if the 'data' directory exists
    if not os.path.isdir(base_path):
        print(f"The directory {base_path} does not exist.")
        # Prompt user to enter a custom directory
        path_out = input("Please enter the full path of the data directory: ")
        if os.path.isdir(custom_dir):
            print(f"You chose the directory: {path_out}")
        else:
            print("Invalid directory path. Please try again.")
            return choose_directory()  # Restart if invalid

    else:

      # Get a list of directories in the 'data' subdirectory
      directories = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
      
      # If there are directories, display them for selection
      if directories:
          print("Please choose one of the following directories:")
          for idx, directory in enumerate(directories):
              print(f"{idx}: {directory}")
          
          # Ask user to choose a directory or input a custom one
          choice = input("Enter the number of your choice or type 'custom' for a custom directory: ")

          # Handle user input
          if choice.isdigit() and int(choice) in range(len(directories)):
              chosen_directory = directories[int(choice)]
              path_out = os.path.join(base_path, chosen_directory)
              print(f"You chose: {path_out}")
          elif choice.lower() == 'custom':
              path_out = input("Enter the full path of the data directory: ")
              if os.path.isdir(path_out):
                  print(f"You chose the directory: {path_out}")
              else:
                  print("Invalid directory path. Please try again.")
                  return choose_directory()  # Restart if invalid
          else:
              print("Invalid choice, please choose a valid option.")
              return choose_directory()  # Restart if invalid
      else:
          print(f"No directories found in {base_path}.")
          exit()

    print("")
    return path_out

def choose_files_to_plot(directory, option):
    # List all files in the selected directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    # If option 0 is chosen, allow the user to select a single file
    if option == 0:
        if files:
            print("Please choose a file to plot:")
            for idx, file in enumerate(files):
                print(f"{idx}: {file}")
            choice = input("Enter the number of your choice: ")
            if choice.isdigit() and int(choice) in range(len(files)):
                chosen_file = files[int(choice)]
                print(f"You chose: {chosen_file}")
                path_out = [chosen_file]
            else:
                print("Invalid choice. Please try again.")
                return choose_files_to_plot(directory, option)
        else:
            print("No files found in the directory.")
            exit()

    # If option 1 is chosen, allow the user to input file names one by one
    elif option == 1:
        print("Enter file number to plot one by one. Type 'stop' to stop.")
        for idx, file in enumerate(files):
          print(f"{idx}: {file}")
        selected_files = []
        while True:
            choice = input("Enter the number of your choice: ")
            if choice.lower() == 'stop':
                break
            if choice.isdigit() and int(choice) in range(len(files)):
                chosen_file = files[int(choice)]
                selected_files.append(chosen_file)
            else:
                print("File not found. Please enter a valid file name.")
        path_out = selected_files

    # If option 2 is chosen, select all files in the directory
    elif option == 2:
        if files:
            print("All files will be selected.")
            path_out = files
        else:
            print("No files found in the directory.")
            exit()

    else:
        print("Invalid option. Please choose a valid option.")
        return choose_files_to_plot(directory, option)

    print(f"You chose: {path_out}")
    print("")
    return path_out

colors = {
    "steel_blue": "#1F77B4",
    "light_steel_blue": "#AEC7E8",
    "orange": "#FF7F0E",
    "light_orange": "#FFBB78",
    "forest_green": "#2CA02C",
    "light_green": "#98DF8A",
    "firebrick_red": "#D62728",
    "soft_red": "#FF9896",
    "lavender": "#9467BD",
    "light_lavender": "#C5B0D5",
    "brown": "#8C564B",
    "tan": "#C49C94",
    "orchid": "#E377C2",
    "light_orchid": "#F7B6D2",
    "gray": "#7F7F7F",
    "light_gray": "#C7C7C7",
    "yellow_green": "#BCBD22",
    "light_yellow_green": "#DBDB8D",
    "turquoise": "#17BECF",
    "light_turquoise": "#9EDAE5"
}

custom_cmap = ListedColormap(colors.values())
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=custom_cmap.colors)

# ====================================== Definitions Finished ====================================== #

directory = choose_directory()
option = choose_option()

file_path = choose_files_to_plot(directory, option)

for file in file_path:
  bias, current = read_data(os.path.join(directory, file))
  current, prefix = convert_to_prefix(current)

  fig_height = 4; fig_width=fig_height  
  fig, [ax1, ax2] = plt.subplots(1, 2, figsize=(fig_width*2,fig_height), constrained_layout=True)

  ax1.plot(bias, current)
  ax2.semilogy(bias, current)

  ax1.set_xlabel("Bias (V)")
  ax2.set_xlabel("Bias (V)")

  ax1.set_ylabel(f"Current ({prefix}A)")

  fig.savefig(f"figures/{os.path.splitext(file)[0]}.pdf", bbox_inches='tight')
  plt.show()
