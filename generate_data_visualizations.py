import argparse
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def load_dataframe(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [str(col).strip() for col in df.columns]
    return df


def ensure_output_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def plot_initial_positions(df_people: pd.DataFrame, output_path: Path) -> None:
    hue_col = None
    for candidate in ['group_number', 'sex', 'prior_visit', ' behavior_type', ' group_type']:
        if candidate.strip() in df_people.columns:
            hue_col = candidate.strip()
            break

    fig, ax = plt.subplots(figsize=(10, 6))
    if hue_col:
        categories = df_people[hue_col].astype('category')
        scatter = ax.scatter(
            df_people['x'],
            df_people['y'],
            c=categories.cat.codes,
            cmap='tab10',
            alpha=0.8,
            s=18,
        )
        cbar = fig.colorbar(scatter, ax=ax, ticks=np.unique(categories.cat.codes))
        cbar.ax.set_yticklabels(categories.cat.categories.astype(str))
        cbar.set_label(hue_col)
    else:
        ax.scatter(df_people['x'], df_people['y'], alpha=0.8, s=18, color='steelblue')

    ax.set_title('Posición inicial de agentes')
    ax.set_xlabel('Coordenada X')
    ax.set_ylabel('Coordenada Y')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


def plot_exit_window_scatter(df_layout: pd.DataFrame, output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 6))

    exit_points = df_layout[df_layout['Type'] == 'Exit'].copy()
    window_points = df_layout[df_layout['Type'] == 'Window'].copy()

    exit_points['center_x'] = (exit_points['x1'] + exit_points['x2']) / 2
    exit_points['center_y'] = (exit_points['y1'] + exit_points['y2']) / 2
    window_points['center_x'] = (window_points['x1'] + window_points['x2']) / 2
    window_points['center_y'] = (window_points['y1'] + window_points['y2']) / 2

    ax.scatter(exit_points['center_x'], exit_points['center_y'], color='red', label='Salidas', s=60)
    ax.scatter(window_points['center_x'], window_points['center_y'], color='blue', label='Ventanas', s=25, alpha=0.7)

    ax.set_title('Ubicación de salidas y ventanas')
    ax.set_xlabel('Coordenada X')
    ax.set_ylabel('Coordenada Y')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


def plot_fire_intensity(df_fire: pd.DataFrame, output_path: Path) -> None:
    fire_counts = df_fire.groupby('time').size().reset_index(name='n_fire_cells')

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(fire_counts['time'], fire_counts['n_fire_cells'], color='orangered', linewidth=2)
    ax.set_title('Intensidad de fuego por paso temporal')
    ax.set_xlabel('Tiempo (s)')
    ax.set_ylabel('Número de celdas en fuego')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


def plot_smoke_timeseries(df_smoke: pd.DataFrame, output_path: Path) -> None:
    smoke_summary = df_smoke.groupby('time')['density'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(smoke_summary['time'], smoke_summary['density'], color='darkslategray', linewidth=2)
    ax.set_title('Evolución del humo en el tiempo')
    ax.set_xlabel('Tiempo (s)')
    ax.set_ylabel('Densidad promedio de humo')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


def plot_spatial_density(df_people: pd.DataFrame, output_path: Path) -> None:
    max_x = int(df_people['x'].max())
    max_y = int(df_people['y'].max())
    density = np.zeros((max_y + 1, max_x + 1), dtype=np.int32)

    for _, row in df_people.iterrows():
        density[int(row['y']), int(row['x'])] += 1

    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(density, cmap='viridis', interpolation='nearest')
    fig.colorbar(im, ax=ax, label='Densidad espacial')
    ax.set_title('Heatmap de densidad espacial inicial')
    ax.set_xlabel('Coordenada X')
    ax.set_ylabel('Coordenada Y')
    plt.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


def plot_smoke_exposure(df_smoke: pd.DataFrame, output_path: Path) -> None:
    max_x = int(df_smoke['x'].max())
    max_y = int(df_smoke['y'].max())
    exposure = np.zeros((max_y + 1, max_x + 1), dtype=float)
    counts = np.zeros((max_y + 1, max_x + 1), dtype=int)

    for _, row in df_smoke.iterrows():
        x = int(row['x'])
        y = int(row['y'])
        exposure[y, x] += float(row['density'])
        counts[y, x] += 1

    exposure = np.divide(exposure, counts, out=np.zeros_like(exposure), where=counts > 0)

    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(exposure, cmap='magma', interpolation='nearest')
    fig.colorbar(im, ax=ax, label='Exposición promedio al humo')
    ax.set_title('Heatmap espacial de exposición al humo')
    ax.set_xlabel('Coordenada X')
    ax.set_ylabel('Coordenada Y')
    plt.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description='Generar visualizaciones descriptivas de los datos de entrada del modelo.')
    parser.add_argument('--output-dir', type=str, default='plots/data_visualizations', help='Directorios de salida para las figuras')
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    ensure_output_dir(output_dir)

    df_people = load_dataframe(Path('data/people.csv'))
    df_layout = load_dataframe(Path('data/building_nightclub.csv'))
    df_fire = load_dataframe(Path('data/fire_nightclub_merged.csv'))
    df_smoke = load_dataframe(Path('data/smoke.csv'))

    plot_initial_positions(df_people, output_dir / 'scatter_initial_positions.png')
    plot_exit_window_scatter(df_layout, output_dir / 'scatter_exits_windows.png')
    plot_fire_intensity(df_fire, output_dir / 'fire_intensity_timeseries.png')
    plot_smoke_timeseries(df_smoke, output_dir / 'smoke_timeseries.png')
    plot_spatial_density(df_people, output_dir / 'spatial_density_heatmap.png')
    plot_smoke_exposure(df_smoke, output_dir / 'smoke_exposure_heatmap.png')

    print(f"Figuras generadas en: {output_dir}")


if __name__ == '__main__':
    main()
