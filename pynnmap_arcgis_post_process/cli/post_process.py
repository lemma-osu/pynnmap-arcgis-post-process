import os

import click

from pynnmap.parser import parameter_parser_factory as ppf

from pynnmap_arcgis_post_process.core import process_func as pf


@click.command(short_help='Convert spatial layers to ArcGIS format')
@click.argument(
    'parameter-file',
    type=click.Path(exists=True),
    required=True)
def post_process(parameter_file):
    p = ppf.get_parameter_parser(parameter_file)

    # Load grids into lists corresponding to type
    axes = []
    distances = []
    neighbors = []

    frmt_dict = {
        'GIO': '',
        'GTiff': '.tif',
        'ENVI': '.bsq',
        'HFA': '.img',
    }

    def build_name(model_dir, prefix, number, frmt):
        base_name = ''.join((prefix, str(number), frmt_dict[frmt]))
        return os.path.join(model_dir, base_name)

    md = p.model_directory
    of = p.output_format
    for n in range(1, int(p.write_axes) + 1):
        axis_grid = build_name(md, p.axes_file, n, of)
        axes.append(axis_grid)

    for n in range(1, int(p.write_neighbors) + 1):
        neighbor_grid = build_name(md, p.neighbor_file, n, of)
        neighbors.append(neighbor_grid)

    for n in range(1, int(p.write_distances) + 1):
        distance_grid = build_name(md, p.distance_file, n, of)
        distances.append(distance_grid)

    # Define projections on all grids
    pf.define_projections(axes, p.projection_file)
    pf.define_projections(neighbors, p.projection_file)
    pf.define_projections(distances, p.projection_file)

    # Convert axis and distance grids to integers (scaled by 100.0)
    pf.integerize_rasters(axes)
    pf.integerize_rasters(distances)

    # Copy the neighbor rasters to force recalculation of statistics
    pf.copy_rasters(neighbors)

    # Join attributes to original neighbor grids
    attribute_join_field = p.plot_id_field
    for neighbor in neighbors:
        pf.join_attributes(
            neighbor, 'VALUE', p.stand_attribute_file, attribute_join_field,
            p.stand_metadata_file
        )

    # Copy, clip and mask neighbor grids & join attributes
    if p.mask_raster != '':
        for i, neighbor in enumerate(neighbors):
            masked_neighbor = '%s/mr%d_nnmsk%d' % (
                p.model_directory, p.model_region, i + 1)
            pf.create_masked_raster(
                neighbor, p.boundary_raster, p.mask_raster, masked_neighbor)
            pf.join_attributes(
                masked_neighbor, 'VALUE', p.stand_attribute_file,
                attribute_join_field, p.stand_metadata_file)
