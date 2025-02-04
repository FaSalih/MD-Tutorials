import numpy as np
import gromacs.formats
import matplotlib.pyplot as plt
import os
import sys

property_list = [
    'Potential', 
    'Kinetic-En.', 
    'Total-Energy',
    'Pressure',
    'Temperature', 
    'Density',
]

# folder = "Gromacs/equilibrate_system/"
folder = ""
window_size_in = int(sys.argv[1])
run_name = (f'_{sys.argv[2]}' if len(sys.argv) > 2 else "")

## Routine to calculate rolling average
def rolling_average(x, N=10):
    """get rolling average of x with window size N

    Args:
        x (1D floating point array): raw data
        N (Integer): window size

    Returns:
        x_avg (1D floating point array): processed data
    """
    x_avg = np.convolve(x, np.ones((N,))/N, mode='valid')
    return x_avg

## Plot energies
fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(6, 6))
for i in range(3):
    # Read xvg file
    property_name = property_list[i]
    try:
        xvg = gromacs.formats.XVG(f"{folder}{property_name}{run_name}.xvg")
        data = xvg.to_df().to_numpy()
    except FileNotFoundError:
        # replace data with array of nans
        t = data[:,0]
        data = np.nan*np.ones(np.shape(data)[0])
        data = np.concatenate((t[:,None], data[:,None]), axis=1)
    # print(f'{property_name} data shape: {np.shape(data)}')

    # Plot xvg data
    ax = axs[i]
    ax.plot(
        data[:,0], data[:,1],
        label=property_name
        )
    
    # Plot rolling average
    window_size = window_size_in
    ax.plot(
        data[:,0][:-(window_size-1)], 
        rolling_average(data[:,1], N=window_size),
        label=f'{property_name} (rolling average)'
        )
    
    # Add plot attributes
    ax.legend()
    # ax.set_xlabel('Time [ps]')
    # ax.set_ylabel('Energy [kJ/mol]')

# add combined ylabel
fig.supxlabel('Time [ps]', fontweight='bold', fontsize=12)
fig.supylabel('Energy [kJ/mol]', fontweight='bold', fontsize=12)
fig.suptitle('Energies', fontweight='bold', fontsize=14)
fig.tight_layout() 
plt.subplots_adjust(hspace=0)
plt.savefig(f'{folder}Energies{run_name}.png', dpi=300)
# plt.show()

## Plot pressure, temperature and density
fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(6, 6))
for i in range(3):
    # Read xvg file
    property_name = property_list[i+3]
    try:
        xvg = gromacs.formats.XVG(f"{folder}{property_name}{run_name}.xvg")
        data = xvg.to_df().to_numpy()
    except FileNotFoundError:
        # replace data with array of nans
        t = data[:,0]
        data = np.nan*np.ones(np.shape(data)[0])
        data = np.concatenate((t[:,None], data[:,None]), axis=1)
        
    # Plot xvg data
    ax = axs[i]
    ax.plot(
        data[:,0], data[:,1],
        label=property_name
        )
    
    # Plot rolling average
    window_size = window_size_in
    ax.plot(
        data[:,0][:-(window_size-1)], 
        rolling_average(data[:,1], N=window_size),
        label=f'{property_name} (rolling average)'
        )
    
    # Add horizontal line for each nano-second
    if property_name == 'Density':
        t_ns = data[:,0]/1000
        integer_t_ns = np.unique(np.ceil(t_ns))
        for t_ns_i in integer_t_ns[0:-1]:
            t_ns_i_idx = np.where(integer_t_ns == t_ns_i)[0][0]
            t_ns_ip1 = integer_t_ns[t_ns_i_idx + 1]
            if t_ns_ip1 > t_ns[-1]:
                continue
            start_idx = np.where(t_ns == t_ns_i)[0][0]
            end_idx = np.where(t_ns == t_ns_ip1)[0][0]
            time_range = t_ns[start_idx:end_idx] * 1000
            range_avg = np.mean(data[start_idx:end_idx,1]) * np.ones(np.shape(time_range))

            ax.plot(time_range,range_avg, label='', color='black', linewidth=1) 
    
    # Add plot attributes
    units = ['bar', 'K', 'kg/m3']
    ax.legend()
    ax.set_ylabel(f'{property_name} [{units[i]}]', fontweight='bold', fontsize=12)

# add combined ylabel
fig.supxlabel('Time [ps]', fontweight='bold', fontsize=12)
fig.suptitle('PVT', fontweight='bold', fontsize=14)
fig.tight_layout() 
plt.subplots_adjust(hspace=0)
plt.savefig(f'{folder}PVT{run_name}.png', dpi=300)
# plt.show()


## Extract equilibrated density and volume
# Read xvg file
folder = ''
property_name = 'Density'
xvg = gromacs.formats.XVG(f"{folder}{property_name}.xvg")
data = xvg.to_df().to_numpy()

# Get average density for last 25 ns
dt = data[1,0] - data[0,0]
n_steps = int(10000/dt)
avg_density = np.mean(data[-n_steps:,1])
std_density = np.std(data[-n_steps:,1])
print(avg_density)
print(std_density)

# # Get equivalent box volume
# volume = m_tot/density  # [m3]
# side_length = volume**(1/3) # [m]
# side_length *= 1e9  # [nm]
# print(side_length)
