"""
Plotting Functions Module for Idaho Policy Institute Analysis

This module provides customized visualization functions for exploring
IPI financial and crime data. Functions create publication-ready plots
with appropriate formatting and styling.

Functions:
    plot_year: Visualize trends over time with bar plots
    plot_corr_matrix: Generate lower-triangle correlation heatmaps
    plot_scatter_matrix: Create scatter plot matrices with correlation annotations

Author: Dominik Huffield
Project: Strategic Financial Insight - Idaho Policy Institute
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import support.load_data as load
import support.supporting_funcs as funcs
import statsmodels.formula.api as smf
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import *
import matplotlib.lines as mlines
from pandas.plotting._tools import _set_ticks_props, _subplots
from pandas.core.dtypes.missing import notna
from scipy.stats import gaussian_kde

def plot_year(data, search, size=False):
    """
    Visualize a feature's trend over time using bar plots.
    
    Creates a publication-ready bar plot showing how a variable changes
    across years. Optionally groups by city size categories.
    
    Args:
        data (pd.DataFrame): Dataset with 'Year4' column
        search (str): Search pattern to find the column to plot (regex supported)
        size (bool): If True, groups bars by city size category. Default is False.
    
    Returns:
        None: Displays plot directly
    
    Note:
        - If multiple columns match the search, plots only the first
        - Uses seaborn styling for professional appearance
        - Figure size optimized for presentations (16x10 inches)
    
    Example:
        >>> data = load.all_data()
        >>> 
        >>> # Plot total crime over time
        >>> plot_year(data, 'Total_Crime')
        >>> 
        >>> # Plot police expenditure grouped by city size
        >>> plot_year(data, 'Police_PerExp', size=True)
    """
    # Find column(s) matching the search pattern
    cols = funcs.search_all(data, search, silent=True)
    
    # Handle multiple matches
    if len(cols) > 1:
        print(f"\nMORE THAN ONE VALUE FOUND, plotting the first:\n{cols[0]}")
    
    # Handle no matches
    if len(cols) == 0:
        print("ERROR: No columns found matching pattern. Exiting.")
        return
    
    # Create figure with appropriate size
    plt.figure(figsize=[15, 9])
    
    # Plot with or without city size grouping
    if size:
        # Group bars by city size category
        ax = sns.barplot(x='Year4', y=cols[0], data=data, hue='size')
    else:
        # Simple year-by-year bars
        ax = sns.barplot(x='Year4', y=cols[0], data=data)
    
    # Format x-axis labels for readability
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
    
    # Set axis labels and title
    plt.ylabel(cols[0].replace("_", " "), fontsize=18)
    plt.xlabel('Year', fontsize=16)
    plt.xticks(fontsize=14)
    plt.title(f"{cols[0]} by Year", fontsize=25)
    
    # Set final figure size
    fig = plt.gcf()
    fig.set_size_inches(16, 10)
    
    plt.show()


def plot_corr_matrix(data, cols):
    """
    Generate a lower-triangle correlation heatmap for selected features.
    
    Creates a clean, professional correlation matrix visualization showing
    only the lower triangle to avoid redundancy. Uses diverging color map
    to highlight positive and negative correlations.
    
    Args:
        data (pd.DataFrame): Dataset containing the features
        cols (list): List of column names to include in correlation matrix
    
    Returns:
        None: Displays plot directly
    
    Limitations:
        Maximum 20 features recommended for readability
    
    Visual Features:
        - Diverging color palette (blue for negative, red for positive)
        - Lower triangle only (removes redundant upper triangle)
        - Square cells with clear gridlines
        - Color bar for correlation scale
    
    Example:
        >>> data = load.all_data()
        >>> 
        >>> # Select features of interest
        >>> features = ['Total_Crime_100k', 'Police_PerExp', 'Debt_100k', 
        ...             'Population', 'Unemployment_Rate']
        >>> 
        >>> # Plot correlation matrix
        >>> plot_corr_matrix(data, features)
    """
    # Subset data to selected columns
    subset = data[cols]
    
    # Check feature count
    if len(cols) <= 20:
        print(f"\nPlotting correlation heatmap for {len(cols)} features:\n")
    if len(cols) > 20:
        print("ERROR: Too many features (>20). Please reduce for readability.")
        return
    
    # Set seaborn style
    sns.set(style="white")
    plt.figure(figsize=[15, 9])

    # Compute correlation matrix
    corr = subset.corr()

    # Generate a mask for the upper triangle (keep only lower triangle)
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))

    # Generate a custom diverging colormap (blue-white-red)
    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})
    
    plt.show()


def plot_scatter_matrix(
    data,
    cols,
    alpha=0.8,
    figsize=None,
    ax=None,
    grid=False,
    diagonal="hist",
    marker=".",
    density_kwds=None,
    hist_kwds={'bins': 20},
    range_padding=0.05,
    plot_axes="lower",  # "all", "lower", "upper"
    **kwds
):
    """
    Create a comprehensive scatter plot matrix with correlation annotations.
    
    Generates a matrix of scatter plots showing pairwise relationships between
    features, with histograms on the diagonal and correlation coefficients
    annotated on each plot.
    
    Args:
        data (pd.DataFrame): Dataset containing the features
        cols (list): List of column names to plot
        alpha (float): Transparency of scatter points (0-1). Default is 0.8.
        figsize (tuple): Figure size (width, height). Default is (15, 9).
        ax (matplotlib.axes): Existing axes to plot on. Default is None (create new).
        grid (bool): Whether to show grid. Default is False.
        diagonal (str): Type of plot on diagonal - 'hist' or 'kde'. Default is 'hist'.
        marker (str): Marker style for scatter points. Default is '.'.
        density_kwds (dict): Keyword arguments for KDE plots. Default is None.
        hist_kwds (dict): Keyword arguments for histograms. Default is {'bins': 20}.
        range_padding (float): Padding around data range (0-1). Default is 0.05.
        plot_axes (str): Which axes to plot - 'all', 'lower', or 'upper'. Default is 'lower'.
        **kwds: Additional keyword arguments passed to scatter plot
    
    Returns:
        matplotlib.axes: Array of axes objects
    
    Features:
        - Lower triangle: Scatter plots with best-fit visualization
        - Diagonal: Histograms or KDE plots showing distributions
        - Annotations: Pearson correlation coefficients on each scatter plot
        - Automatic axis scaling and label formatting
    
    Example:
        >>> data = load.all_data()
        >>> 
        >>> # Select features for pairwise analysis
        >>> features = ['Total_Crime_100k', 'Police_PerExp', 
        ...             'Long_Term_Debt_100k', 'Population']
        >>> 
        >>> # Create scatter matrix
        >>> plot_scatter_matrix(data, features, diagonal='kde')
    """
    features = data[cols]
    # plt.figure(figsize=(15,9))

    def _get_marker_compat(marker):

        if marker not in mlines.lineMarkers:
            return "o"
        return marker


    df = features._get_numeric_data()
    n = df.columns.size
    naxes = n * n
    fig, axes = _subplots(naxes=naxes, figsize=(15,9), ax=ax, squeeze=False)

    # no gaps between subplots
    fig.subplots_adjust(wspace=0, hspace=0)

    mask = notna(df)

    marker = _get_marker_compat(marker)

    hist_kwds = hist_kwds or {}
    density_kwds = density_kwds or {}

    
    kwds.setdefault("edgecolors", "none")

    boundaries_list = []
    for a in df.columns:
        values = df[a].values[mask[a].values]
        rmin_, rmax_ = np.min(values), np.max(values)
        rdelta_ext = (rmax_ - rmin_) * range_padding / 2.0
        boundaries_list.append((rmin_ - rdelta_ext, rmax_ + rdelta_ext))

    for i, a in enumerate(df.columns):
        for j, b in enumerate(df.columns):
            ax = axes[i, j]
            ax.set_visible(False)  

            if i == j:
                values = df[a].values[mask[a].values]

                # Deal with the diagonal by drawing a histogram there.
                if diagonal == "hist":
                    ax.hist(values, **hist_kwds)

                elif diagonal in ("kde", "density"):

                    y = values
                    gkde = gaussian_kde(y)
                    ind = np.linspace(y.min(), y.max(), 1000)
                    ax.plot(ind, gkde.evaluate(ind), **density_kwds)
                    
                ax.set_xlim(boundaries_list[i])
                ax.set_visible(True)

            elif plot_axes == "all" or (i > j and plot_axes == "lower") or (i < j and plot_axes == "upper"):
                common = (mask[a] & mask[b]).values

                ax.scatter(
                    df[b][common], df[a][common], marker=marker, alpha=alpha, **kwds
                )

                ax.set_xlim(boundaries_list[j])
                ax.set_ylim(boundaries_list[i])
                ax.set_visible(True)

            ax.set_xlabel(b,rotation=40)
            ax.set_ylabel(a,rotation=40)
            # plt.xticks(rotation=90)

            if plot_axes in ("all", "lower"):
                if j != 0:
                    ax.yaxis.set_visible(False)
                if i != n - 1:
                    ax.xaxis.set_visible(False)
            elif plot_axes == "upper":
                if i != j:
                    ax.yaxis.set_visible(False)
                if i == 0:
                    ax.xaxis.tick_top()
                    ax.xaxis.set_label_position('top') 
                else:
                    ax.xaxis.set_visible(False)

    if len(df.columns) > 1:
        lim1 = boundaries_list[0]
        locs = axes[0][1].yaxis.get_majorticklocs()
        locs = locs[(lim1[0] <= locs) & (locs <= lim1[1])]
        adj = (locs - lim1[0]) / (lim1[1] - lim1[0])

        lim0 = axes[0][0].get_ylim()
        adj = adj * (lim0[1] - lim0[0]) + lim0[0]
        axes[0][0].yaxis.set_ticks(adj)

        if np.all(locs == locs.astype(int)):
            # if all ticks are int
            locs = locs.astype(int)
        axes[0][0].yaxis.set_ticklabels(locs)

    _set_ticks_props(axes, xlabelsize=6, xrot=0, ylabelsize=6, yrot=0)
    axes[0][0].yaxis.set_visible(False)
    
    corrs = df.corr().values
    for i, j in zip(*plt.np.tril_indices_from(axes, k = 1)):
        axes[i, j].annotate('Corr. coef = %.3f' % corrs[i, j], (0.8, 0.2), xycoords='axes fraction', ha='center', va='center', size=12)

    plt.show()
    return axes
    # return


