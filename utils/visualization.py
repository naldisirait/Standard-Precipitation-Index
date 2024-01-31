import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import geopandas as gpd
import cartopy as crt

def plot_map(values, latitude, longitude, shp, path_output_fig, title):

    # Create a figure and axes
    fig, ax = plt.subplots(subplot_kw={'projection': crt.crs.PlateCarree()})

    # Plot the data using pcolor
    pcm = plt.pcolor(longitude, latitude, values, cmap='RdYlGn_r')

    # Plot the NTT shapefile boundaries
    shp.plot(ax=ax, facecolor='none', edgecolor='k', linewidth=1)

    # Add gridlines
    ax.gridlines(draw_labels=False, linewidth=0.5, color='gray', alpha=0.5, linestyle='--')

    # Add colorbar
    plt.colorbar(pcm, shrink=0.5)

    # Set labels for longitude and latitude
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')

    # Specify the desired number of ticks
    num_ticks_x = 5
    num_ticks_y = 5

    # Calculate tick positions
    xtick_positions = np.linspace(longitude.min(), longitude.max(), num_ticks_x)
    ytick_positions = np.linspace(latitude.min(), latitude.max(), num_ticks_y)

    # Set ticks on the x and y axes
    ax.set_xticks(xtick_positions)
    ax.set_yticks(ytick_positions)

    # Set title
    ax.set_title(f'{title}', pad=12)

    plt.savefig(f"{path_output_fig}/{title}.png")