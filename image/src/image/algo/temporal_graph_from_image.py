# -*- python -*-
#
#       OpenAlea.image.algo
#
#       Copyright 2012 INRIA - CIRAD - INRA
#
#       File author(s):  Jonathan Legrand <jonathan.legrand@ens-lyon.fr>
#                        Frederic Boudon <frederic.boudon@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite: http://openalea.gforge.inria.fr
#
################################################################################
"""This module helps to create PropertyGraph from SpatialImages."""

import numpy as np
import time, warnings, math
import copy as cp
from IPython import embed

from openalea.image.serial.basics import SpatialImage, imread
from openalea.image.algo.analysis import SpatialImageAnalysis, AbstractSpatialImageAnalysis, DICT
from openalea.image.spatial_image import is2D
from openalea.container import PropertyGraph
from openalea.container import TemporalPropertyGraph
from openalea.container.temporal_graph_analysis import translate_ids_Graph2Image, translate_keys_Graph2Image

from openalea.image.registration.registration import pts2transfo
from vplants.asclepios.vt_exec import reech3d


def find_daugthers_barycenters(graph, reference_image, reference_tp, tp_2register, vids, real_world_units=True, **kwargs):
    """
    Based on a TemporalPropertyGraph (lineage info), this script find the barycenter of 'fused' daughters cells between `reference_tp` & `tp_2register`.

    :Parameters:
     - `graph` (TemporalPropertyGraph) - a TemporalPropertyGraph used for the lineage information
     - `reference_image` (AbstractSpatialImageAnalysis|SpatialImage|str) - segmented image of the reference time point used to compute barycenters
     - `reference_tp` (int) - the
     - `tp_2register` (int) -
     - `real_world_units` (bool) -

    :Returns:
     - a dictionary where *keys= vids and *values= 3x1 vectors of coordinates
    """
    t_start = time.time()
    SpI_ids = translate_ids_Graph2Image(graph, vids)
    # -- **kwargs options:
    try: background = kwargs['background']
    except: background = 1
    assert isinstance(background, int)
    try: verbose = kwargs['verbose']
    except: verbose = False

    if isinstance(reference_image, str):
        reference_image = imread(reference_image)
    if isinstance(reference_image, SpatialImage):
        analysis = SpatialImageAnalysis(reference_image, ignoredlabels = 0, return_type = DICT, background = background)
    if isinstance(reference_image, AbstractSpatialImageAnalysis):
        analysis = reference_image
    else:
        warnings.warn("Could not determine the type of the `image`...")
        return None

    new_barycenters = {}
    print "Computing daugthers barycenters:"
    for n, vid in enumerate(vids):
        if n%50 == 0: print n,'/',len(vids)
        graph_children = graph.descendants(vid, reference_tp-tp_2register) - graph.descendants(vid, reference_tp-tp_2register-1)
        SpI_children = translate_ids_Graph2Image(graph, graph_children)
        x,y,z = [],[],[]
        for id_child in SpI_children:
            xyz = np.where( (analysis.image[analysis.boundingbox(id_child)]) == id_child )
            x.extend(xyz[0]+analysis.boundingbox(id_child)[0].start)
            y.extend(xyz[1]+analysis.boundingbox(id_child)[1].start)
            z.extend(xyz[2]+analysis.boundingbox(id_child)[2].start)

        if real_world_units:
            new_barycenters[vid] = np.mean(np.asarray([analysis.image.resolution]).T*np.asarray([x,y,z]),1)
        else:
            new_barycenters[vid] = np.mean(np.asarray([x,y,z]),1)

    t_stop = time.time()
    print "Time to find 'fused' daughters barycenter: {}s".format(t_stop-t_start)
    return translate_keys_Graph2Image(graph, new_barycenters)


def image_registration(image_2register, ref_points, reg_points, output_shape, **kwargs):
    """
    Register an image according to `ref_points` & `reg_points`.
    Interpolation methods is set to 'nearest' by default, but this can be changed by adding an 'interpolation_method' as kwargs.
    """
    ref_points, reg_points = np.asarray(ref_points), np.asarray(reg_points)
    registration = pts2transfo(ref_points, reg_points)
    if ('interpolation_method' in kwargs) and isinstance(kwargs['interpolation_method'],str):
        interpolation_method = kwargs['interpolation_method']
    else:
        interpolation_method = "nearest"
    im_reech = reech3d.reech3d(image_2register, mat=registration, interpolation=interpolation_method, vin=image_2register.resolution, vout=image_2register.resolution, output_shape=output_shape)

    if ('t_2def' in kwargs) and ('t_ref' in kwargs):
        t_2def = kwargs['t_2def']
        t_ref = kwargs['t_ref']
        np.savetxt('pts_{}{}_{}.txt'.format(t_2def+1,t_ref+1,t_2def+1),reg_points)
        np.savetxt('pts_{}{}_{}.txt'.format(t_2def+1,t_ref+1,t_ref+1),ref_points)
    if 'save_registered_image' in kwargs:
        assert ('t_2def' in kwargs) and ('t_ref' in kwargs)
        imsave('t{}_on_t{}.inr.gz'.format(t_2def+1,t_ref+1),im_reech)

    return im_reech


def find_object_boundingbox(image2crop, ignore_cells_in_image_margins=True, **kwargs):
    """
    Find the smallest box surrounding the labelled object in the image `image2crop`.
    """
    # -- **kwargs options:
    try: background = kwargs['background']
    except: background = 1
    assert isinstance(background, int)

    ### Reshaping with a boundingbox (around non-margin cells):
    def_analysis = SpatialImageAnalysis(image2crop, ignoredlabels = 0, return_type = DICT, background = background)
    if ignore_cells_in_image_margins:
        def_analysis.add2ignoredlabels( def_analysis.cells_in_image_margins() )
    if 'label2keep' in kwargs:
        def_analysis.add2ignoredlabels( list(set(def_analysis.labels())-set(kwargs['label2keep'])) )
    # labels to make a boundingbox around:
    labels2keep = def_analysis.labels()
    # Find the surrounding bbox of the object (without `self.cells_in_image_margins()`):
    bbox_init = def_analysis.boundingbox(labels2keep[0])
    global_box=[bbox_init[0].start,bbox_init[0].stop,bbox_init[1].start,bbox_init[1].stop,bbox_init[2].start,bbox_init[2].stop]
    for cell in labels2keep[1:]:
        bbox = def_analysis.boundingbox(cell)
        for i in xrange(3):
            if bbox[i].start < global_box[i*2]:
                global_box[i*2] = bbox[i].start
            if bbox[i].stop > global_box[i*2+1]:
                global_box[i*2+1] = bbox[i].stop

    print "New boundaries for the registered image: {}".format(global_box)

    return global_box


def fuse_daughters_in_image(image, graph, ref_vids, reference_tp, tp_2fuse, **kwargs):
    """
    Based on a TemporalPropertyGraph (lineage info), this script fuse daughters cells between `reference_tp` & `tp_2fuse`.

    :Parameters:
     - `image` (AbstractSpatialImageAnalysis|SpatialImage|str) - segmented image of the reference time point used to compute barycenters
     - `graph` (TemporalPropertyGraph) - a TemporalPropertyGraph used for the lineage information
     - `ref_vids` (list) - the
     - `reference_tp` (int) - time point (in the graph) of the 'reference image' i.e. from wher compute descendants
     - `tp_2fuse` (int) - time point (in the graph) to fuse descendants

    :Returns:
     - a dictionary where *keys= ref_vids and *values= 3x1 vectors of coordinates
    """
    t_start = time.time()
    SpI_ids = translate_ids_Graph2Image(graph, ref_vids)
    # -- **kwargs options:
    try: background = kwargs['background']
    except: background = 1
    assert isinstance(background, int)
    try: verbose = kwargs['verbose']
    except: verbose = False
    # -- Check the type the `image` object
    if isinstance(image, str):
        image = imread(image)
    if isinstance(image, SpatialImage):
        analysis = SpatialImageAnalysis(image, ignoredlabels = 0, return_type = DICT, background = background)
    elif isinstance(image, AbstractSpatialImageAnalysis):
        analysis = image
    else:
        raise TypeError("Could not determine the type of the `image`...")
    # -- 'fused' image creation:
    tmp_img = np.asarray(cp.copy(analysis.image))
    tmp_img.fill(0)
    tmp_img += analysis.image == background # retreive the background
    if verbose: print "Fusing daugthers from t{} at t{}:".format(reference_tp, tp_2fuse)
    not_found = []
    for n, vid in enumerate(ref_vids):
        if verbose and n%50 == 0: print n,'/',len(ref_vids)
        graph_children = graph.descendants(vid, tp_2fuse-reference_tp) - graph.descendants(vid, tp_2fuse-reference_tp-1)
        if graph_children == set([]):
            not_found.append(vid)
        SpI_children = translate_ids_Graph2Image(graph, graph_children)
        for id_child in SpI_children:
            mask = analysis.image[analysis.boundingbox(id_child)] == id_child
            tmp_img[analysis.boundingbox(id_child)] = tmp_img[analysis.boundingbox(id_child)] + np.multiply(mask, SpI_ids[n])

    t_stop = time.time()
    if verbose: print "Time to 'fuse' daughters with parent ids: {}s".format(t_stop-t_start)
    if not_found != []:
        warnings.warn("You have asked to fuse these labels' daughters, but they have no known daughters: {}"format(not_found)
    tmp_img = SpatialImage(tmp_img)
    tmp_img.resolution = analysis.image.resolution
    tmp_img.info = analysis.image.info
    return tmp_img


def generate_graph_topology(labels, neighborhood):
    """
    Function generating a topological/spatial graph based on neighbors detection.

    :Parameters:
     - `labels` (list) - list of labels to be found in the image and added to the topological graph.
     - `neighborhood` (dict) - dictionary giving neighbors of each object.

    :Returns:
     - `graph` (PropertyGraph) - the topological/spatial graph.
     - `label2vertex` (dict) - dictionary translating labels into vertex ids (vids).
     - `edges` (dict) - dictionary associating an edge id to a couple of topologically/spatially related vertex.
    """
    graph = PropertyGraph()
    vertex2label = {}
    for l in labels: vertex2label[graph.add_vertex(l)] = l
    label2vertex = dict([(j,i) for i,j in vertex2label.iteritems()])

    labelset = set(labels)
    edges = {}

    for source,targets in neighborhood.iteritems():
        if source in labelset :
            for target in targets:
                if source < target and target in labelset:
                    edges[(source,target)] = graph.add_edge(label2vertex[source],label2vertex[target])

    graph.add_vertex_property('label')
    graph.vertex_property('label').update(vertex2label)

    return graph, label2vertex, edges

def find_wall_median_voxel(dict_wall_voxels, labels2exclude = []):
    """
    """
    if isinstance(labels2exclude,int):
        labels2exclude = [labels2exclude]

    wall_median = {}
    for label_1, label_2 in dict_wall_voxels:
        if label_1 in labels2exclude or label_2 in labels2exclude:
            continue # if 0 means that it wasn't in the labels list provided, so we skip it.
        from openalea.plantgl.math import Vector3
        xyz = np.array(dict_wall_voxels[(label_1, label_2)]).T
        xyz = [Vector3(list([float(i) for i in k])) for k in xyz]
        # compute geometric median:
        from openalea.plantgl.algo import approx_pointset_median, pointset_median
        if len(xyz) <= 100:
            median_vox_id = pointset_median( xyz )
        else:
            median_vox_id = approx_pointset_median( xyz )
        wall_median[(label_1, label_2)] = xyz[median_vox_id]

    return wall_median

#~ spatio_temporal_properties2D = ['barycenter','boundingbox','border','L1','epidermis_surface','wall_surface','inertia_axis']
spatio_temporal_properties2D = ['barycenter','boundingbox','border','L1','epidermis_surface','inertia_axis']
spatio_temporal_properties3D = ['volume','barycenter','boundingbox','border','L1','epidermis_surface','wall_surface','inertia_axis', 'projected_anticlinal_wall_median', 'wall_median', 'wall_orientation', 'all_wall_orientation', 'division_wall_orientation', 'strain_landmarks']


def _spatial_properties_from_image(graph, SpI_Analysis, labels, neighborhood, label2vertex,
         mlabelpair2edge, background, spatio_temporal_properties, property_as_real, bbox_as_real):
    """
    Add properties from a `SpatialImageAnalysis` class object (representing a segmented image) to a PropertyGraph.
    """
    labelset = set(labels)
    # -- We want to keep the unit system of each variable
    graph.add_graph_property("units",dict())

    if ("wall_orientation" in spatio_temporal_properties) and ('all_wall_orientation' in spatio_temporal_properties):
        spatio_temporal_properties.remove("wall_orientation")

    if 'boundingbox' in spatio_temporal_properties :
        print 'Extracting boundingbox...'
        add_vertex_property_from_label_and_value(graph, 'boundingbox', labels, SpI_Analysis.boundingbox(labels,real=bbox_as_real), mlabel2vertex=label2vertex)
        #~ graph._graph_property("units").update( {"boundingbox":(u'\xb5m'if bbox_as_real else 'voxels')} )

    if 'volume' in spatio_temporal_properties and SpI_Analysis.is3D():
        print 'Computing volume property...'
        add_vertex_property_from_dictionary(graph, 'volume', SpI_Analysis.volume(labels,real=property_as_real), mlabel2vertex=label2vertex)
        #~ graph._graph_property("units").update( {"volume":(u'\xb5m\xb3'if property_as_real else 'voxels')} )

    barycenters = None
    if 'barycenter' in spatio_temporal_properties :
        print 'Computing barycenter property...'
        barycenters = SpI_Analysis.center_of_mass(labels, real=property_as_real)
        add_vertex_property_from_dictionary(graph, 'barycenter', barycenters, mlabel2vertex=label2vertex)
        #~ graph._graph_property("units").update( {"barycenter":(u'\xb5m'if property_as_real else 'voxels')} )

    background_neighbors = set(SpI_Analysis.neighbors(background))
    background_neighbors.intersection_update(labelset)
    if 'L1' in spatio_temporal_properties :
        print 'Generating the list of cells belonging to the first layer...'
        add_vertex_property_from_label_and_value(graph, 'L1', labels, [(l in background_neighbors) for l in labels], mlabel2vertex=label2vertex)

    if 'border' in spatio_temporal_properties :
        print 'Generating the list of cells at the margins of the stack...'
        border_cells = SpI_Analysis.cells_in_image_margins()
        try: border_cells.remove(background)
        except: pass
        border_cells = set(border_cells)
        add_vertex_property_from_label_and_value(graph, 'border', labels, [(l in border_cells) for l in labels], mlabel2vertex=label2vertex)

    if 'inertia_axis' in spatio_temporal_properties :
        print 'Computing inertia_axis property...'
        inertia_axis, inertia_values = SpI_Analysis.inertia_axis(labels,barycenters)
        add_vertex_property_from_dictionary(graph, 'inertia_axis', inertia_axis, mlabel2vertex=label2vertex)
        add_vertex_property_from_dictionary(graph, 'inertia_values', inertia_values, mlabel2vertex=label2vertex)

    if 'wall_surface' in spatio_temporal_properties :
        print 'Computing wall_surface property...'
        filtered_edges, unlabelled_target, unlabelled_wall_surfaces = {}, {}, {}
        for source,targets in neighborhood.iteritems():
            if source in labelset :
                filtered_edges[source] = [ target for target in targets if source < target and target in labelset ]
                unlabelled_target[source] = [ target for target in targets if target not in labelset and target != background]
        wall_surfaces = SpI_Analysis.wall_surfaces(filtered_edges,real=property_as_real)
        add_edge_property_from_label_property(graph,'wall_surface',wall_surfaces,mlabelpair2edge=mlabelpair2edge)

        graph.add_vertex_property('unlabelled_wall_surface')
        for source in unlabelled_target:
            unlabelled_wall_surface = SpI_Analysis.wall_surfaces({source:unlabelled_target[source]},real=property_as_real)
            graph.vertex_property('unlabelled_wall_surface')[label2vertex[source]] = sum(unlabelled_wall_surface.values())

        #~ graph._graph_property("units").update( {"wall_surface":('\xb5m\xb2'if property_as_real else 'voxels')} )
        #~ graph._graph_property("units").update( {"unlabelled_wall_surface":('\xb5m\xb2'if property_as_real else 'voxels')} )

    if 'epidermis_surface' in spatio_temporal_properties :
        print 'Computing epidermis_surface property...'
        def not_background(indices):
            a,b = indices
            if a == background:
                if b == background: raise ValueError(indices)
                else : return b
            elif b == background: return a
            else: raise ValueError(indices)
        epidermis_surfaces = SpI_Analysis.cell_wall_surface(background, list(background_neighbors), real=property_as_real)
        epidermis_surfaces = dict([(not_background(indices),value) for indices,value in epidermis_surfaces.iteritems()])
        add_vertex_property_from_label_property(graph,'epidermis_surface',epidermis_surfaces,mlabel2vertex=label2vertex)
        #~ graph._graph_property("units").update( {"epidermis_surface":('um2'if property_as_real else 'voxels')} )


    if 'projected_anticlinal_wall_median' in spatio_temporal_properties:
        print 'Computing projected_anticlinal_wall_median property...'
        dict_anticlinal_wall_voxels = SpI_Analysis.wall_voxels_per_cells_pairs( SpI_Analysis.layer1(), neighborhood, only_epidermis = True, ignore_background = True )
        wall_median = find_wall_median_voxel(dict_anticlinal_wall_voxels, labels2exclude = [0])

        add_edge_property_from_dictionary(graph, 'projected_anticlinal_wall_median', wall_median)

    if 'wall_median' in spatio_temporal_properties:
        print 'Computing wall_median property...'
        try: dict_wall_voxels
        except: dict_wall_voxels = SpI_Analysis.wall_voxels_per_cells_pairs(labels, neighborhood, ignore_background=False )

        wall_median = find_wall_median_voxel(dict_wall_voxels, labels2exclude = [])
        edge_wall_median, unlabelled_wall_median, vertex_wall_median = {},{},{}
        for label_1, label_2 in dict_wall_voxels.keys():
            if (label_1 in graph.vertices()) and (label_2 in graph.vertices()):
                edge_wall_median[(label_1, label_2)] = wall_median[(label_1, label_2)]
            if (label_1 == 0): # no need to check `label_2` because labels are sorted in keys returned by `wall_voxels_per_cells_pairs`
                unlabelled_wall_median[label_2] = wall_median[(label_1, label_2)]
            if (label_1 == 1): # no need to check `label_2` because labels are sorted in keys returned by `wall_voxels_per_cells_pairs`
                vertex_wall_median[label_2] = wall_median[(label_1, label_2)]

        add_edge_property_from_dictionary(graph, 'wall_median', edge_wall_median)
        add_vertex_property_from_dictionary(graph, 'epidermis_wall_median', vertex_wall_median)
        add_vertex_property_from_dictionary(graph, 'unlabelled_wall_median', unlabelled_wall_median)


    if 'all_walls_orientation' in spatio_temporal_properties:
        print 'Computing wall_orientation property...'
        # -- First we have to extract the voxels defining the frontier between two objects:
        # - Extract wall_orientation property for 'unlabelled' and 'epidermis' walls as well:
        try: dict_wall_voxels
        except: dict_wall_voxels = SpI_Analysis.wall_voxels_per_cells_pairs(labels, neighborhood, ignore_background=False )

        if 'wall_median' in graph.edge_properties():
            medians_coords = dict( (graph.edge_vertices(eid), coord) for eid,coord in graph.edge_property('wall_median').iteritems() )
            medians_coords.update(dict( (0,vid) for vid in graph.vertex_property('unlabelled_wall_median') ))
            medians_coords.update(dict( (1,vid) for vid in graph.vertex_property('epidermis_wall_median') ))
            pc_values, pc_normal, pc_directions, pc_origin = SpI_Analysis.wall_orientation( dict_wall_voxels, fitting_degree = 2, plane_projection = False, dict_coord_points_ori = medians_coords )
        else:
            pc_values, pc_normal, pc_directions, pc_origin = SpI_Analysis.wall_orientation( dict_wall_voxels, fitting_degree = 2, plane_projection = False )

        # -- Now we can compute the orientation of the frontier between two objects:
        edge_pc_values, edge_pc_normal, edge_pc_directions, edge_pc_origin = {},{},{},{}
        vertex_pc_values, vertex_pc_normal, vertex_pc_directions, vertex_pc_origin = {},{},{},{}
        epidermis_pc_values, epidermis_pc_normal, epidermis_pc_directions, epidermis_pc_origin = {},{},{},{}
        for label_1, label_2 in dict_wall_voxels.keys():
            if (label_1 in graph.vertices()) and (label_2 in graph.vertices()):
                edge_pc_values[(label_1, label_2)] = pc_values[(label_1, label_2)]
                edge_pc_normal[(label_1, label_2)] = pc_normal[(label_1, label_2)]
                edge_pc_directions[(label_1, label_2)] = pc_directions[(label_1, label_2)]
                edge_pc_origin[(label_1, label_2)] = pc_origin[(label_1, label_2)]
            if (label_1 == 0): # no need to check `label_2` because labels are sorted in keys returned by `wall_voxels_per_cells_pairs`
                vertex_pc_values[label_2] = pc_values[(label_1, label_2)]
                vertex_pc_normal[label_2] = pc_normal[(label_1, label_2)]
                vertex_pc_directions[label_2] = pc_directions[(label_1, label_2)]
                vertex_pc_origin[label_2] = pc_origin[(label_1, label_2)]
            if (label_1 == 1): # no need to check `label_2` because labels are sorted in keys returned by `wall_voxels_per_cells_pairs`
                epidermis_pc_values[label_2] = pc_values[(label_1, label_2)]
                epidermis_pc_normal[label_2] = pc_normal[(label_1, label_2)]
                epidermis_pc_directions[label_2] = pc_directions[(label_1, label_2)]
                epidermis_pc_origin[label_2] = pc_origin[(label_1, label_2)]

        add_edge_property_from_dictionary(graph, 'wall_principal_curvature_values', edge_pc_values)
        add_edge_property_from_dictionary(graph, 'wall_principal_curvature_normal', edge_pc_normal)
        add_edge_property_from_dictionary(graph, 'wall_principal_curvature_directions', edge_pc_directions)
        if not 'wall_median' in graph.edge_properties():
            add_edge_property_from_dictionary(graph, 'wall_principal_curvature_origin', edge_pc_origin)
        if vertex_pc_values != {}:
            add_vertex_property_from_dictionary(graph, 'unlabelled_wall_principal_curvature_values', vertex_pc_values)
            add_vertex_property_from_dictionary(graph, 'unlabelled_wall_principal_curvature_normal', vertex_pc_normal)
            add_vertex_property_from_dictionary(graph, 'unlabelled_wall_principal_curvature_directions', vertex_pc_directions)
            if not 'wall_median' in graph.edge_properties():
                add_vertex_property_from_dictionary(graph, 'unlabelled_wall_principal_curvature_origin', vertex_pc_origin)
        if epidermis_pc_values != {}:
            add_vertex_property_from_dictionary(graph, 'epidermis_wall_principal_curvature_values', epidermis_pc_values)
            add_vertex_property_from_dictionary(graph, 'epidermis_wall_principal_curvature_normal', epidermis_pc_normal)
            add_vertex_property_from_dictionary(graph, 'epidermis_wall_principal_curvature_directions', epidermis_pc_directions)
            if not 'wall_median' in graph.edge_properties():
                add_vertex_property_from_dictionary(graph, 'epidermis_wall_principal_curvature_origin', epidermis_pc_origin)

    if 'epidermis_local_principal_curvature' in spatio_temporal_properties:
        index_radius = default_properties.index('epidermis_local_principal_curvature')+1
        if isinstance(default_properties[index_radius],int):
            radius = [default_properties[index_radius]]
        elif isinstance(default_properties[index_radius],list):
            radius = default_properties[index_radius]
        else:
            radius = [60]

        graph.add_graph_property('radius_local_principal_curvature_estimation',radius)
        for radius in graph.graph_property('radius_local_principal_curvature_estimation'):
            print 'Computing local_principal_curvature property with radius = {}voxels...'.format(radius)
            print u"This represent a local curvature estimation area of {}\xb5m\xb2".format(round(math.pi*(radius*SpI_Analysis.image.resolution[0])*(radius*SpI_Analysis.image.resolution[1])))
            SpI_Analysis.compute_principal_curvatures(vids=labels, radius=radius, verbose=True)
            add_vertex_property_from_dictionary(graph, 'epidermis_local_principal_curvature_values_r'+str(radius), SpI_Analysis.principal_curvatures)
            add_vertex_property_from_dictionary(graph, 'epidermis_local_principal_curvature_normal_r'+str(radius), SpI_Analysis.principal_curvatures_normal)
            add_vertex_property_from_dictionary(graph, 'epidermis_local_principal_curvature_directions_r'+str(radius), SpI_Analysis.principal_curvatures_directions)
        if not 'wall_median' in graph.edge_properties():
            add_vertex_property_from_dictionary(graph, 'epidermis_local_principal_curvature_origin', SpI_Analysis.principal_curvatures_origin)

    return graph


def _temporal_properties_from_images(graph, SpI_Analysis, vids, background,
         spatio_temporal_properties, property_as_real, bbox_as_real):
    """
    Add properties from a `SpatialImageAnalysis` class object (representing a segmented image) to a TemporalPropertyGraph.

    :Parameters:
     - `graph` (TPG)
     - `SpI_Analysis` (AbstractSpatialImageAnalysis) - Spatial analysis of an image.
     - `labels` (list) - list of labels to be found in the image.
     - `label2vertex`
     - `background` (int) - label representing background.
     - `spatio_temporal_properties` (list) - the list of name of properties to create. It should be in spatio_temporal_properties.
     - `property_as_real` (bool) - If property_as_real = True, property is in real-world units else in voxels.
     - `bbox_as_real` (bool) - If bbox_as_real = True, bounding boxes are in real-world units else in voxels.

    """
    try:
        min_contact_surface = graph.graph_property('min_contact_surface')
        assert isinstance(min_contact_surface, int) or isinstance(min_contact_surface, float)
    except:
        min_contact_surface = None
    available_properties = ['epidermis_2D_landmarks', '3D_landmarks', 'division_wall_orientation', 'fused_daughters_inertia_axis']
    properties = [ppt for ppt in spatio_temporal_properties if isinstance(ppt,str)] # we want to compare str types, no extra args passed
    if set(properties) & set(available_properties) != set([]):
        fused_image_analysis, neighborhood = {}, {}
        if 'epidermis_2D_landmarks' in spatio_temporal_properties:
            assert 'projected_anticlinal_wall_median' in graph.edge_property_names()

            print "Computing epidermis_2D_landmarks..."
            # -- First we need to extract the medians of 'anticlinal walls' at the surface for the daughters fused images:
            fused_anticlinal_wall_median, fused_vertex_wall_median = {}, {}
            for tp_2fuse in xrange(1,graph.nb_time_points+1,1):
                ref_tp = tp_2fuse-1
                print "Extract the surfacic wall medians of daughters fused images between t{} and t{}".format(ref_tp, tp_2fuse)
                ref_vids = [k for k in graph.vertex_at_time(ref_tp, as_parent=True) if k in vids]
                ref_SpI_ids = translate_ids_Graph2Image(graph, ref_vids)
                # - 'Fusing' daughters from `ref_tp` in `tp_2fuse`:
                fused_image = fuse_daughters_in_image(SpI_Analysis[tp_2fuse], graph, ref_vids, ref_tp, tp_2fuse, background=background[tp_2fuse], verbose=True)
                # - Creating a `SpatialImageAnalysis`:
                fused_image_analysis[tp_2fuse] = SpatialImageAnalysis(fused_image, ignoredlabels = 0, return_type = DICT, background = background[tp_2fuse])
                # - Extracting neighborhood info:
                fused_neighborhood = fused_image_analysis[tp_2fuse].neighbors(ref_SpI_ids, min_contact_surface = min_contact_surface)
                # - Computing voxels position of 'anticlinal walls' at the surface:
                fused_dict_anticlinal_wall_voxels = fused_image_analysis[tp_2fuse].wall_voxels_per_cells_pairs(ref_SpI_ids, fused_neighborhood, only_epidermis = True, ignore_background = False)
                # - Finally compute the position of the median for each groups of voxels:
                fused_anticlinal_wall_median[tp_2fuse] = find_wall_median_voxel(fused_dict_anticlinal_wall_voxels, labels2exclude = [])
                for label_1, label_2 in fused_anticlinal_wall_median[tp_2fuse].keys():
                    if (label_1 == 1): # no need to check `label_2` because labels are sorted in keys returned by `wall_voxels_per_cells_pairs`
                        fused_vertex_wall_median[label_2] = fused_anticlinal_wall_median[tp_2fuse][(label_1, label_2)]
                        fused_anticlinal_wall_median[tp_2fuse].pop((label_1, label_2))
                extend_vertex_property_from_dictionary(graph, 'daughters_fused_epidermis_wall_median', fused_vertex_wall_median, time_point = ref_tp)

            # -- Now we can proceed to the landmarks association:
            for tp_2fuse in xrange(1,graph.nb_time_points+1,1):
                ref_tp = tp_2fuse-1
                print "Surfacic 3D landmarks association between t{} and t{}".format(ref_tp, tp_2fuse)
                # - Translating 'projected_anticlinal_wall_median' in `graph.edge_property()` with pair of labels as keys:
                edge2labelpair_m = edge2labelpair_map(graph, ref_tp)
                wall_median = dict([(edge2labelpair_m[eid],m) for eid,m in graph.edge_property('projected_anticlinal_wall_median').iteritems() if edge2labelpair_m.has_key(eid)])
                # - Starting the landmarks association:
                asso, no_asso_found = {}, []
                for k in wall_median:
                    if fused_anticlinal_wall_median[tp_2fuse].has_key(k):
                        asso[k] = [wall_median[k], fused_anticlinal_wall_median[tp_2fuse][k]]
                    else:
                        no_asso_found.append(k)
                # - Saving detected landmarks association:
                extend_edge_property_from_dictionary(graph, 'epidermis_2D_landmarks', asso, time_point=ref_tp)
                # - Displaying informations about how good this landmarks association step went :
                print "Found {} associations over {} ({}%)".format(len(asso),len(wall_median),round(float(len(asso))/len(wall_median)*100,1))
                new_contact_from_fusing = set(fused_anticlinal_wall_median[tp_2fuse].keys())-set(asso.keys())
                if not new_contact_from_fusing == set([]):
                    print "New contact found after daughters fusion :"
                    for label_1, label_2 in new_contact_from_fusing:
                        print u"Contact between {} and {}, surface: {}\xb5m\xb2".format(label_1, label_2, round(fused_image_analysis[tp_2fuse].cell_wall_surface(label_1, label_2),1))
                        print u"Contact surface between {} and {} at t_n-1: {}\xb5m\xb2".format(label_1, label_2, round(SpI_Analysis[ref_tp].cell_wall_surface(label_1, label_2),1))

            print "Done\n"

        if '3D_landmarks' in spatio_temporal_properties:
            assert 'wall_median' in graph.edge_property_names()
            assert 'unlabelled_wall_median' in graph.vertex_property_names()
            assert 'epidermis_wall_median' in graph.vertex_property_names()

        if 'division_wall_orientation' in spatio_temporal_properties:
            pass

        if 'fused_daughters_inertia_axis' in spatio_temporal_properties:
            # Try to use 'fused_image_analysis' dict else compute it:
            if fused_image_analysis == {} or len(fused_image_analysis) != graph.nb_time_points:
                for tp_2fuse in xrange(1,graph.nb_time_points+1,1):
                    ref_tp = tp_2fuse-1
                    print "Fusing daughters of  t{} in image t{}".format(ref_tp, tp_2fuse)
                    ref_vids = [k for k in graph.vertex_at_time(ref_tp, as_parent=True) if k in vids]
                    ref_SpI_ids = translate_ids_Graph2Image(graph, ref_vids)
                    # - 'Fusing' daughters from `ref_tp` in `tp_2fuse`:
                    fused_image = fuse_daughters_in_image(SpI_Analysis[tp_2fuse], graph, ref_vids, ref_tp, tp_2fuse, background=background[tp_2fuse], verbose=True)
                    # - Creating a `SpatialImageAnalysis`:
                    fused_image_analysis[tp_2fuse] = SpatialImageAnalysis(fused_image, ignoredlabels = 0, return_type = DICT, background = background[tp_2fuse])

            print 'Computing fused_daughters_inertia_axis property...'
            for tp_2fuse in xrange(1,graph.nb_time_points+1,1):
                ref_tp = tp_2fuse-1
                ref_vids = [k for k in graph.vertex_at_time(ref_tp,lineaged=True) if k in vids]
                ref_SpI_ids = translate_ids_Graph2Image(graph, ref_vids)
                inertia_axis, inertia_values = fused_image_analysis[tp_2fuse].inertia_axis(ref_SpI_ids,fused_image_analysis[tp_2fuse].center_of_mass(ref_SpI_ids))
                extend_vertex_property_from_dictionary(graph, 'fused_daughters_inertia_axis', inertia_axis, time_point=ref_tp)
                extend_vertex_property_from_dictionary(graph, 'fused_daughters_inertia_values', inertia_values, time_point=ref_tp)


    return graph


def graph_from_image2D(image, labels, background, spatio_temporal_properties,
                     property_as_real, bbox_as_real,
                     ignore_cells_at_stack_margins, min_contact_surface):
    return _graph_from_image(image, labels, background, spatio_temporal_properties,
                            property_as_real, bbox_as_real, ignore_cells_at_stack_margins, min_contact_surface)

def graph_from_image3D(image, labels, background, spatio_temporal_properties,
                     property_as_real, bbox_as_real,
                     ignore_cells_at_stack_margins, min_contact_surface):
    return _graph_from_image(image, labels, background, spatio_temporal_properties,
                            property_as_real, bbox_as_real, ignore_cells_at_stack_margins, min_contact_surface)


def temporal_graph_from_image(images, lineages, time_steps = [], background = 1, spatio_temporal_properties = None,
     properties4lineaged_vertex = False, property_as_real = True, bbox_as_real = False, ignore_cells_at_stack_margins = True, **kwargs):
    """
    Function creating a TemporalPropertyGraph based on a list of SpatialImages and list of lineage.
    Optional parameter can be provided, see below.

    :Parameters:
     - `images` (list) : list of images
     - `lineages` (list) : list of lineages
     - `time_steps` (list) : time steps between images
     - `list_labels` (list) : list of labels (list) to use in each spatial graph
     - `background` (int|list) : label or list of labels (list) to use as background during `SpatialImageAnalysis`
     - `spatio_temporal_properties` (list) : list of strings related to spatio-temporal properties to compute
     - `properties4lineaged_vertex` (bool|str) : if `False` compute properties for every possible vertex, if `True` for lineaged vertex only and if `strict` vertices temporally linked from the beginning to the end
     - `property_as_real` (bool) : specify if the computed spatio-temporal properties should be return in real-world units
     - `bbox_as_real` (bool) : specify if the (cells) bounding boxes should be return in real-world units
    """
    nb_images = len(images)
    assert len(lineages) == nb_images-1
    assert len(time_steps) == nb_images
    if isinstance(background, int):
        background = [background for k in xrange(nb_images)]
    elif isinstance(background, list):
        assert len(background) == nb_images

    if isinstance(images[0], AbstractSpatialImageAnalysis):
        assert [isinstance(image, AbstractSpatialImageAnalysis) for image in images]
    if isinstance(images[0], SpatialImage):
        assert [isinstance(image, SpatialImage) for image in images]
    if isinstance(images[0], str):
        assert [isinstance(image, str) for image in images]

    try: min_contact_surface = kwargs['min_contact_surface']
    except: min_contact_surface = None
    try: real_surface = kwargs['real_surface']
    except: real_surface = property_as_real

    print "# -- Creating Spatial Graphs..."
    analysis, labels, graphs, label2vertex, edges, neighborhood = {}, {}, {}, {}, {}, {}
    for n,image in enumerate(images):
        print "Initialising SpatialImageAnalysis #{}...".format(n)
        # - First we contruct an object `analysis` from class `AbstractSpatialImageAnalysis`
        if isinstance(image, str):
            analysis[n] = SpatialImageAnalysis(imread(image), ignoredlabels = 0, return_type = DICT, background = background[n])
        if isinstance(image, SpatialImage):
            analysis[n] = SpatialImageAnalysis(image, ignoredlabels = 0, return_type = DICT, background = background[n])
        if isinstance(image, AbstractSpatialImageAnalysis):
            analysis[n] = image
        # - We modify it according to input parameters:
        if ignore_cells_at_stack_margins:
            analysis[n].add2ignoredlabels(analysis[n].cells_in_image_margins())
        labels[n] = analysis[n].labels()
        if background[n] in labels[n]: labels[n].remove(background[n])
        # -- Now we construct the Spatial Graph (topology):
        neighborhood[n] = analysis[n].neighbors(labels[n], min_contact_surface = min_contact_surface)
        graphs[n], label2vertex[n], edges[n] = generate_graph_topology(labels[n], neighborhood[n])
    print "Done\n"

    print "# -- Creating Spatio-Temporal Graph..."
    # -- Now we construct the Temporal Property Graph (with no properties attached to vertex):
    tpg = TemporalPropertyGraph()
    tpg.extend([graph for graph in graphs.values()], lineages, time_steps)
    tpg.add_graph_property('min_contact_surface', min_contact_surface)
    print "Done\n"

    # -- If we already removed cells at the margins of the stack, no need to look for them after:
    if ignore_cells_at_stack_margins:
        try: spatio_temporal_properties.remove('border')
        except: pass

    # -- Registration step:
    if 'register_images' in kwargs and kwargs['register_images']:
        print "# -- Images registration..."
        if 'reference_image' in kwargs:
            if isinstance(kwarg['reference_image'],int):
                ref_image =  kwarg['reference_image']
                unreg_images_ids_list = list( set(np.arange(tpg.nb_time_points+1)) - set([ref_image]) )
                ref_images_ids_list = np.repeat(ref_images, tpg.nb_time_points)
            if isinstance(kwarg['reference_image'],list):
                ref_images_ids_list =  kwarg['reference_image']
                assert len(ref_images_ids_list) == tpg.nb_time_points
                if 'unregistered_images' in kwargs and isinstance(kwarg['unregistered_images'],list):
                    unreg_images_ids_list = kwarg['unregistered_images']
                    assert len(unreg_images_ids_list)==tpg.nb_time_points
                else:
                    warnings.warn("You gave a 'reference_image' list but no 'unregistered_images' list as 'kwargs'.")
                    return None
        else:
            # -- By default we register every images onto the next one, starting with the last one.
            ref_images_ids_list = list(np.arange(tpg.nb_time_points,0,-1))
            unreg_images_ids_list = list(np.array(ref_images_ids_list)-1)

        reg_neighborhood, excluded_labels, wall_surfaces = {}, {}, {}
        for ref_img_id, unreg_img_id in zip(ref_images_ids_list,unreg_images_ids_list):
            # - we save previously 'ignored_labels':
            excluded_labels[unreg_img_id] = analysis[unreg_img_id].ignoredlabels()
            print "Registering image #{} over {}image #{} ...".format(unreg_img_id, "" if ref_img_id==tpg.nb_time_points else "registered ", ref_img_id)
            # we use only cells that are fully lineaged for stability reasons!
            unreg_img_vids = tpg.vertex_at_time(unreg_img_id, fully_lineaged = True)
            # translation into SpatialImage ids:
            unreg_SpI_ids = translate_ids_Graph2Image(tpg, unreg_img_vids)
            # we now need the barycenters of the 'fused' daughters:
            fused_daughters_bary = find_daugthers_barycenters(tpg, analysis[ref_img_id], ref_img_id, unreg_img_id, unreg_img_vids)
            # registration and resampling step:
            ref_points = [fused_daughters_bary[k] for k in fused_daughters_bary]
            reg_points = [analysis[unreg_img_id].center_of_mass(unreg_SpI_ids)[k] for k in fused_daughters_bary]
            registered_img = image_registration(analysis[unreg_img_id].image, ref_points, reg_points, output_shape=analysis[ref_img_id].image.shape)
            # redoing the `SpatialImageAnalysis`
            analysis[unreg_img_id] = SpatialImageAnalysis(registered_img, ignoredlabels = 0, return_type = DICT, background = background[n])
            analysis[unreg_img_id].add2ignoredlabels(excluded_labels[unreg_img_id])
            # -- Now we RE-construct the Spatial Graph (topology):
            labels[n] = analysis[n].labels()
            neighborhood[unreg_img_id] = analysis[n].neighbors(labels[n], min_contact_surface = min_contact_surface)
            graphs[n], label2vertex[n], edges[n] = generate_graph_topology(labels[n], neighborhood[n])
        print "Done\n"

        # -- Re-creating Spatio-Temporal Graph after registration...
        print "# -- Re-creating the Spatio-Temporal Graph after registration..."
        tpg = TemporalPropertyGraph()
        tpg.extend([graph for graph in graphs.values()], lineages, time_steps)
        tpg.add_graph_property('min_contact_surface', min_contact_surface)
        print "Done\n"


    # -- Adding spatio-temporal features to the Spatio-Temporal Graph...
    print "# -- Adding spatio-temporal features to the Spatio-Temporal Graph..."
    spatio_temporal_properties = check_properties(tpg, spatio_temporal_properties)

    if isinstance(properties4lineaged_vertex,str) and properties4lineaged_vertex == 'strict':
        vids = tpg.lineaged_vertex(fully_lineaged=True)
    else:
        vids = tpg.lineaged_vertex(fully_lineaged=False)

    tpg = _spatial_properties_from_images(tpg, analysis, vids, background,
         spatio_temporal_properties, property_as_real, bbox_as_real)

    tpg = _temporal_properties_from_images(tpg, analysis, vids, background,
         spatio_temporal_properties, property_as_real, bbox_as_real)
    print "Done\n"

    return tpg

def check_properties(graph, spatio_temporal_properties):
    """
    Function used to ensure 'spatio_temporal_properties' coherence !
    """
    if ("wall_orientation" in spatio_temporal_properties) and ('all_wall_orientation' in spatio_temporal_properties):
        spatio_temporal_properties.remove("wall_orientation")

    if 'epidermis_2D_landmarks' in spatio_temporal_properties:
        if 'projected_anticlinal_wall_median' not in graph.edge_properties() and 'projected_anticlinal_wall_median' not in spatio_temporal_properties:
            spatio_temporal_properties.append('projected_anticlinal_wall_median')
        if 'wall_median' not in graph.edge_properties() and 'wall_median' not in spatio_temporal_properties:
            spatio_temporal_properties.append('wall_median')
        if 'L1' not in graph.vertex_properties() and 'L1' not in spatio_temporal_properties:
            spatio_temporal_properties.append('L1')

    if 'epidermis_local_principal_curvature' in spatio_temporal_properties:
        index_radius = spatio_temporal_properties.index('epidermis_local_principal_curvature')+1
        if isinstance(spatio_temporal_properties[index_radius],int):
            radius = [spatio_temporal_properties[index_radius]]
        elif isinstance(spatio_temporal_properties[index_radius],list):
            radius = spatio_temporal_properties[index_radius]
        else:
            radius = [60]

        try:
            graph.add_graph_property('radius_local_principal_curvature_estimation',radius)
            radius_2_compute = radius
            graph.add_graph_property('radius_2_compute',radius_2_compute)
        except:
            existing_radius = set(graph.graph_property('radius_local_principal_curvature_estimation')) & set(radius)
            if existing_radius != set([]):
                radius_2_compute = list(set(radius) - existing_radius)
            graph.graph_property('radius_local_principal_curvature_estimation').extend(radius_2_compute)
            graph.add_graph_property('radius_2_compute',radius_2_compute)

    return spatio_temporal_properties

def label2vertex_map(graph, time_point = None):
    """
        Compute a dictionary that map label to vertex id.
        It requires the existence of a 'label' vertex property

        :rtype: dict
    """
    if isinstance(graph, TemporalPropertyGraph):
        assert time_point is not None
        return dict([(j,i) for i,j in graph.vertex_property('label').iteritems() if graph.vertex_property('index')[i]==time_point])
    else:
        return dict([(j,i) for i,j in graph.vertex_property('label').iteritems()])

def vertex2label_map(graph, time_point = None):
    """
        Compute a dictionary that map label to vertex id.
        It requires the existence of a 'label' vertex property

        :rtype: dict
    """
    if isinstance(graph, TemporalPropertyGraph):
        assert time_point is not None
        return dict([(i,j) for i,j in graph.vertex_property('label').iteritems() if graph.vertex_property('index')[i]==time_point])
    else:
        return dict([(i,j) for i,j in graph.vertex_property('label').iteritems()])

def label2vertex(graph, labels, time_point = None):
    """
        Translate label as vertex id.
        It requires the existence of a 'label' vertex property

        :rtype: dict
    """
    label2vertexmap = label2vertex_map(graph, time_point)
    if isinstance(labels,list):
        return [label2vertexmap[label] for label in labels]
    else:
        return label2vertexmap[labels]

def labelpair2edge_map(graph, time_point = None):
    """
        Compute a dictionary that map pair of labels to edge id.
        It requires the existence of a 'label' property

        :rtype: dict
    """
    mvertex2label = vertex2label_map(graph, time_point)

    return dict([((mvertex2label[graph.source(eid)],mvertex2label[graph.target(eid)]),eid) for eid in graph.edges()
     if (mvertex2label.has_key(graph.source(eid)) and mvertex2label.has_key(graph.target(eid)))] )

def edge2labelpair_map(graph, time_point = None):
    """
        Compute a dictionary that map pair of labels to edge id.
        It requires the existence of a 'label' property

        :rtype: dict
    """
    mvertex2label = vertex2label_map(graph, time_point)

    return dict([(eid, (mvertex2label[graph.source(eid)],mvertex2label[graph.target(eid)])) for eid in graph.edges()
     if (mvertex2label.has_key(graph.source(eid)) and mvertex2label.has_key(graph.target(eid)))] )

def vertexpair2edge_map(graph):
    """
        Compute a dictionary that map pair of labels to edge id.
        It requires the existence of a 'label' property

        :rtype: dict
    """
    return dict([((graph.source(eid),graph.target(eid)),eid) for eid in graph.edges()])


def add_vertex_property_from_dictionary(graph, name, dictionary, mlabel2vertex = None, time_point = None):
    """
        Add a vertex property with name 'name' to the graph build from an image.
        The values of the property are given as by a dictionary where keys are vertex labels.
    """
    if isinstance(graph, TemporalPropertyGraph):
        assert time_point is not None
    if mlabel2vertex is None:
        mlabel2vertex = label2vertex_map(graph, time_point)
    if name in graph.vertex_properties():
        raise ValueError("Existing vertex property '{}'".format(name))

    graph.add_vertex_property(name)
    graph.vertex_property(name).update( dict([(mlabel2vertex[k], dictionary[k]) for k in dictionary]) )

def add_vertex_property_from_label_and_value(graph, name, labels, property_values, mlabel2vertex = None):
    """
        Add a vertex property with name 'name' to the graph build from an image.
        The values of the property are given as two lists.
        First one gives the label in the image and second gives the value of the property.
        Labels are first translated in id of the graph and values are assigned to these ids in the graph
    """
    if mlabel2vertex is None:
        mlabel2vertex = label2vertex_map(graph)
    if name in graph.vertex_properties():
        raise ValueError("Existing vertex property '{}'".format(name))

    graph.add_vertex_property(name)
    graph.vertex_property(name).update(dict([(mlabel2vertex[i], v) for i,v in zip(labels,property_values)]))

def add_vertex_property_from_label_property(graph, name, label_property, mlabel2vertex = None):
    """
        Add a vertex property with name 'name' to the graph build from an image.
        The values of the property are given as a dictionnary associating a label and a value.
        Labels are first translated in id of the graph and values are assigned to these ids in the graph
    """
    if mlabel2vertex is None:
        mlabel2vertex = label2vertex_map(graph)
    if name in graph.vertex_properties():
        raise ValueError("Existing vertex property '{}'".format(name))

    graph.add_vertex_property(name)
    graph.vertex_property(name).update(dict([(mlabel2vertex[i], v) for i,v in label_property.iteritems()]))

def add_edge_property_from_dictionary(graph, name, dictionary, mlabelpair2edge = None):
    """
        Add an edge property with name 'name' to the graph build from an image.
        The values of the property are given as by a dictionary where keys are vertex labels.
    """
    if mlabelpair2edge is None:
        mlabelpair2edge = labelpair2edge_map(graph)
    if name in graph.edge_properties():
        raise ValueError("Existing edge property '{}'".format(name))

    graph.add_edge_property(name)
    graph.edge_property(name).update( dict([(mlabelpair2edge[k], dictionary[k]) for k in dictionary]) )

def add_edge_property_from_label_and_value(graph, name, label_pairs, property_values, mlabelpair2edge = None):
    """
        Add an edge property with name 'name' to the graph build from an image.
        The values of the property are given as two lists.
        First one gives the pair of labels in the image that are connected and the second list gives the value of the property.
        Pairs of labels are first translated in edge ids of the graph and values are assigned to these ids in the graph
    """
    if mlabelpair2edge is None:
        mlabelpair2edge = labelpair2edge_map(graph)
    if name in graph.edge_properties():
        raise ValueError("Existing edge property '{}'".format(name))

    graph.add_edge_property(name)
    graph.edge_property(name).update(dict([(mlabelpair2edge[labelpair], value) for labelpair,value in zip(label_pairs,property_values)]))

def add_edge_property_from_label_property(graph, name, labelpair_property, mlabelpair2edge = None):
    """
        Add an edge property with name 'name' to the graph build from an image.
        The values of the property are given as a dictionnary associating a pair of label and a value.
        Pairs of labels are first translated in edge ids of the graph and values are assigned to these ids in the graph
    """
    if mlabelpair2edge is None:
        mlabelpair2edge = labelpair2edge_map(graph)
    if name in graph.edge_properties():
        raise ValueError("Existing edge property '{}'".format(name))

    graph.add_edge_property(name)
    graph.edge_property(name).update(dict([(mlabelpair2edge[labelpair], value) for labelpair,value in labelpair_property.iteritems()]))

def extend_edge_property_from_dictionary(graph, name, dictionary, time_point = None, mlabelpair2edge = None):
    """
        Add an edge property with name 'name' to the graph build from an image.
        The values of the property are given as by a dictionary where keys are vertex labels.
    """
    if isinstance(graph, TemporalPropertyGraph):
        assert time_point is not None
    if mlabelpair2edge is None:
        mlabelpair2edge = labelpair2edge_map(graph, time_point)
    if name not in graph.edge_properties():
        warnings.warn("Edge property '{}' does not exist".format(name))
        graph.add_edge_property(name)

    missing_edges = list(set(dictionary.keys())-set(mlabelpair2edge.keys()))
    if missing_edges != []:
        warnings.warn("Error found while saving edge property '{}'".format(name))
        warnings.warn("The provided TemporalPropertyGraph did not contain an edge between vertices: {}".format(missing_edges))
    graph.edge_property(name).update( dict([(mlabelpair2edge[k], dictionary[k]) for k in dictionary if k in mlabelpair2edge.keys()]) )

def extend_vertex_property_from_dictionary(graph, name, dictionary, mlabel2vertex = None, time_point = None):
    """
        Add a vertex property with name 'name' to the graph build from an image.
        The values of the property are given as by a dictionary where keys are vertex labels.
    """
    if isinstance(graph, TemporalPropertyGraph):
        assert time_point is not None
    if mlabel2vertex is None:
        mlabel2vertex = label2vertex_map(graph, time_point)
    if name not in graph.vertex_properties():
        warnings.warn("Vertex property '{}' does not exist".format(name))
        graph.add_vertex_property(name)

    missing_vertex = list(set(dictionary.keys())-set(mlabel2vertex.keys()))
    if missing_vertex != []:
        warnings.warn("Error found while saving vertex property '{}'".format(name))
        warnings.warn("The provided TemporalPropertyGraph did not contain the vollowing vert{}: {}".format("ices" if len(missing_vertex)>=2 else "ex", missing_vertex))
    graph.vertex_property(name).update( dict([(mlabel2vertex[k], dictionary[k]) for k in dictionary if k in mlabel2vertex.keys()]) )


def add_property2graph(graph, images, spatio_temporal_properties, vids, background, property_as_real, bbox_as_real):
    """
    Allow to add a property 'spatio_temporal_properties' to an existing `TemporalPropertyGraph` 'graph'.
    :Parameters:
     - `graph` (TemporalPropertyGraph) - graph to complete
     - `images` (list) - list of strings, SpatialImages or AbstractSpatialImageAnalysis to compute properties from
     - `spatio_temporal_properties` (list) - list of strings related to spatio-temporal properties to compute
     - `vids` (list) - list of vids for which to compute extra properties, if `None` use all lineaged vertex
     - `background` (int|list) - id or list of id specifying the background labels in each `images`
     - `property_as_real` (bool) - specify if the computed spatio-temporal properties should be return in real-world units
     - `bbox_as_real` (bool) - specify if the (cells) bounding boxes should be return in real-world units
    """
    for ppt in spatio_temporal_properties:
        if isinstance(ppt,str) and (ppt in graph.vertex_properties() or ppt in graph.edge_properties()):
            print "The property '{}' is already in the graph !!!".format(ppt)
            spatio_temporal_properties.remove(spatio_temporal_properties.index(ppt))

    nb_images = len(images)
    if isinstance(background, int):
        background = [background for k in xrange(nb_images)]
    elif isinstance(background, list):
        assert len(background) == nb_images

    if isinstance(images[0], AbstractSpatialImageAnalysis):
        assert [isinstance(image, AbstractSpatialImageAnalysis) for image in images]
    if isinstance(images[0], SpatialImage):
        assert [isinstance(image, SpatialImage) for image in images]
    if isinstance(images[0], str):
        assert [isinstance(image, str) for image in images]

    print "# -- Creating Spatial Graphs..."
    analysis, labels, graphs, label2vertex, edges, neighborhood = {}, {}, {}, {}, {}, {}
    for n,image in enumerate(images):
        print "Initialising SpatialImageAnalysis #{}...".format(n)
        # - First we contruct an object `analysis` from class `AbstractSpatialImageAnalysis`
        if isinstance(image, str):
            analysis[n] = SpatialImageAnalysis(imread(image), ignoredlabels = 0, return_type = DICT, background = background[n])
        if isinstance(image, SpatialImage):
            analysis[n] = SpatialImageAnalysis(image, ignoredlabels = 0, return_type = DICT, background = background[n])
        if isinstance(image, AbstractSpatialImageAnalysis):
            analysis[n] = image

    # -- Adding spatio-temporal features to the Spatio-Temporal Graph...
    print "# -- Adding spatio-temporal features to the Spatio-Temporal Graph..."
    spatio_temporal_properties = check_properties(graph, spatio_temporal_properties)

    if isinstance(vids,str) and vids == 'strict':
        vids = graph.lineaged_vertex(fully_lineaged=True)
    elif vids is None:
        vids = graph.lineaged_vertex(fully_lineaged=False)
    else:
        assert isinstance(vids, list)

    graph = _spatial_properties_from_images(graph, analysis, vids, background,
         spatio_temporal_properties, property_as_real, bbox_as_real)
    graph = _temporal_properties_from_images(graph, analysis, vids, background,
         spatio_temporal_properties, property_as_real, bbox_as_real)
    print "Done\n"

    return graph


def _spatial_properties_from_images(graph, SpI_Analysis, vids, background,
         spatio_temporal_properties, property_as_real, bbox_as_real):
    """
    Add properties from a `SpatialImageAnalysis` class object (representing a segmented image) to a TemporalPropertyGraph.
    """
    assert isinstance(graph, TemporalPropertyGraph)
    available_properties = ['boundingbox', 'volume', 'barycenter', 'L1', 'border', 'inertia_axis', 'wall_surface', 'epidermis_surface', 'projected_anticlinal_wall_median', 'wall_median', 'all_walls_orientation', 'epidermis_local_principal_curvature']
    properties = [ppt for ppt in spatio_temporal_properties if isinstance(ppt,str)] # we want to compare str types, no extra args passed
    if set(properties) & set(available_properties) != set([]):
        for tp in xrange(graph.nb_time_points+1):
            print "# - Analysing image #{}".format(tp)
            labels = translate_ids_Graph2Image(graph, [k for k in graph.vertex_at_time(tp) if k in vids])
            labelset = set(labels)
            neighborhood = translate_keys_Graph2Image(graph, dict([(vid, translate_ids_Graph2Image(graph, graph.neighbors(vid,'s'))) for vid in vids if graph.vertex_property('index')[vid]==tp]), tp)
            # -- We want to keep the unit system of each variable
            try: graph.add_graph_property("units",dict())
            except: pass

            if 'boundingbox' in spatio_temporal_properties :
                print 'Extracting boundingbox...'
                extend_vertex_property_from_dictionary(graph, 'boundingbox', SpI_Analysis[tp].boundingbox(labels,real=bbox_as_real), time_point=tp)
                #~ graph._graph_property("units").update( {"boundingbox":(u'\xb5m'if bbox_as_real else 'voxels')} )

            if 'volume' in spatio_temporal_properties and SpI_Analysis[tp].is3D():
                print 'Computing volume property...'
                extend_vertex_property_from_dictionary(graph, 'volume', SpI_Analysis[tp].volume(labels,real=property_as_real), time_point=tp)
                #~ graph._graph_property("units").update( {"volume":(u'\xb5m\xb3'if property_as_real else 'voxels')} )

            barycenters = None
            if 'barycenter' in spatio_temporal_properties :
                print 'Computing barycenter property...'
                barycenters = SpI_Analysis[tp].center_of_mass(labels, real=property_as_real)
                extend_vertex_property_from_dictionary(graph, 'barycenter', barycenters, time_point=tp)
                #~ graph._graph_property("units").update( {"barycenter":(u'\xb5m'if property_as_real else 'voxels')} )

            background_neighbors = SpI_Analysis[tp].neighbors(background[tp])
            if isinstance(background_neighbors, dict):
                background_neighbors = set(background_neighbors[background[tp]])
            else:
                background_neighbors = set(background_neighbors)
            background_neighbors.intersection_update(labelset)
            if 'L1' in spatio_temporal_properties :
                print 'Generating the list of cells belonging to the first layer...'
                extend_vertex_property_from_dictionary(graph, 'L1', dict([(l, (l in background_neighbors)) for l in labels]), time_point=tp)

            if 'border' in spatio_temporal_properties :
                print 'Generating the list of cells at the margins of the stack...'
                border_cells = SpI_Analysis[tp].cells_in_image_margins()
                try: border_cells.remove(background)
                except: pass
                border_cells = set(border_cells)
                extend_vertex_property_from_dictionary(graph, 'border', dict([(l, (l in border_cells)) for l in labels]), time_point=tp)

            if 'inertia_axis' in spatio_temporal_properties :
                print 'Computing inertia_axis property...'
                inertia_axis, inertia_values = SpI_Analysis[tp].inertia_axis(labels,barycenters)
                extend_vertex_property_from_dictionary(graph, 'inertia_axis', inertia_axis, time_point=tp)
                extend_vertex_property_from_dictionary(graph, 'inertia_values', inertia_values, time_point=tp)

            if 'wall_surface' in spatio_temporal_properties :
                print 'Computing wall_surface property...'
                filtered_edges, unlabelled_target, unlabelled_wall_surfaces = {}, {}, {}
                for source,targets in neighborhood.iteritems():
                    if source in labelset :
                        filtered_edges[source] = [ target for target in targets if source < target and target in labelset ]
                        unlabelled_target[source] = [ target for target in targets if target not in labelset and target != background]
                wall_surfaces = SpI_Analysis[tp].wall_surfaces(filtered_edges,real=property_as_real)
                extend_vertex_property_from_dictionary(graph, 'wall_surface', wall_surfaces, time_point=tp)

                graph.add_vertex_property('unlabelled_wall_surface')
                for source in unlabelled_target:
                    unlabelled_wall_surface = SpI_Analysis[tp].wall_surfaces({source:unlabelled_target[source]},real=property_as_real)
                    graph.vertex_property('unlabelled_wall_surface')[label2vertex[source]] = sum(unlabelled_wall_surface.values())

                #~ graph._graph_property("units").update( {"wall_surface":(u'\xb5m\xb2' if property_as_real else 'voxels')} )
                #~ graph._graph_property("units").update( {"unlabelled_wall_surface":(u'\xb5m\xb2'if property_as_real else 'voxels')} )

            if 'epidermis_surface' in spatio_temporal_properties :
                print 'Computing epidermis_surface property...'
                def not_background(indices):
                    a,b = indices
                    if a == background:
                        if b == background: raise ValueError(indices)
                        else : return b
                    elif b == background: return a
                    else: raise ValueError(indices)
                epidermis_surfaces = SpI_Analysis[tp].cell_wall_surface(background, list(background_neighbors), real=property_as_real)
                epidermis_surfaces = dict([(not_background(indices),value) for indices,value in epidermis_surfaces.iteritems()])
                extend_vertex_property_from_dictionary(graph,'epidermis_surface', epidermis_surfaces, time_point=tp)
                #~ graph._graph_property("units").update( {"epidermis_surface":(u'\xb5m\xb2' if property_as_real else 'voxels')} )


            if 'projected_anticlinal_wall_median' in spatio_temporal_properties:
                print 'Computing projected_anticlinal_wall_median property...'
                dict_anticlinal_wall_voxels = SpI_Analysis[tp].wall_voxels_per_cells_pairs( SpI_Analysis[tp].layer1(), neighborhood, only_epidermis = True, ignore_background = True )
                wall_median = find_wall_median_voxel(dict_anticlinal_wall_voxels, labels2exclude = [0])

                extend_edge_property_from_dictionary(graph, 'projected_anticlinal_wall_median', wall_median, time_point=tp)

            if 'wall_median' in spatio_temporal_properties:
                print 'Computing wall_median property...'
                try: dict_wall_voxels
                except: dict_wall_voxels = SpI_Analysis[tp].wall_voxels_per_cells_pairs(labels+[background[tp]], neighborhood.update({background[tp]:list(background_neighbors)}), ignore_background=False )

                wall_median = find_wall_median_voxel(dict_wall_voxels, labels2exclude = [])
                edge_wall_median, unlabelled_wall_median, vertex_wall_median = {},{},{}
                for label_1, label_2 in dict_wall_voxels.keys():
                    if (label_1 == 0): # no need to check `label_2` because labels are sorted in keys returned by `wall_voxels_per_cells_pairs`
                        unlabelled_wall_median[label_2] = wall_median[(label_1, label_2)]
                    elif (label_1 == 1): # no need to check `label_2` because labels are sorted in keys returned by `wall_voxels_per_cells_pairs`
                        vertex_wall_median[label_2] = wall_median[(label_1, label_2)]
                    else:
                        edge_wall_median[(label_1, label_2)] = wall_median[(label_1, label_2)]

                extend_edge_property_from_dictionary(graph, 'wall_median', edge_wall_median, time_point=tp)
                extend_vertex_property_from_dictionary(graph, 'epidermis_wall_median', vertex_wall_median, time_point=tp)
                extend_vertex_property_from_dictionary(graph, 'unlabelled_wall_median', unlabelled_wall_median, time_point=tp)


            if 'all_walls_orientation' in spatio_temporal_properties:
                print 'Computing wall_orientation property...'
                # -- First we have to extract the voxels defining the frontier between two objects:
                # - Extract wall_orientation property for 'unlabelled' and 'epidermis' walls as well:
                try: dict_wall_voxels
                except: dict_wall_voxels = SpI_Analysis[tp].wall_voxels_per_cells_pairs(labels+[background[tp]], neighborhood.update({background[tp]:list(background_neighbors)}), ignore_background=False )

                if 'wall_median' in graph.edge_properties():
                    medians_coords = dict( (graph.edge_vertices(eid), coord) for eid,coord in graph.edge_property('wall_median').iteritems() )
                    medians_coords.update(dict( (0,vid) for vid in graph.vertex_property('unlabelled_wall_median') ))
                    medians_coords.update(dict( (1,vid) for vid in graph.vertex_property('epidermis_wall_median') ))
                    pc_values, pc_normal, pc_directions, pc_origin = SpI_Analysis[tp].wall_orientation( dict_wall_voxels, fitting_degree = 2, plane_projection = False, dict_coord_points_ori = medians_coords )
                else:
                    pc_values, pc_normal, pc_directions, pc_origin = SpI_Analysis[tp].wall_orientation( dict_wall_voxels, fitting_degree = 2, plane_projection = False )

                # -- Now we can compute the orientation of the frontier between two objects:
                edge_pc_values, edge_pc_normal, edge_pc_directions, edge_pc_origin = {},{},{},{}
                vertex_pc_values, vertex_pc_normal, vertex_pc_directions, vertex_pc_origin = {},{},{},{}
                epidermis_pc_values, epidermis_pc_normal, epidermis_pc_directions, epidermis_pc_origin = {},{},{},{}
                for label_1, label_2 in dict_wall_voxels.keys():
                    if (label_1 in graph.vertices()) and (label_2 in graph.vertices()):
                        edge_pc_values[(label_1, label_2)] = pc_values[(label_1, label_2)]
                        edge_pc_normal[(label_1, label_2)] = pc_normal[(label_1, label_2)]
                        edge_pc_directions[(label_1, label_2)] = pc_directions[(label_1, label_2)]
                        edge_pc_origin[(label_1, label_2)] = pc_origin[(label_1, label_2)]
                    if (label_1 == 0): # no need to check `label_2` because labels are sorted in keys returned by `wall_voxels_per_cells_pairs`
                        vertex_pc_values[label_2] = pc_values[(label_1, label_2)]
                        vertex_pc_normal[label_2] = pc_normal[(label_1, label_2)]
                        vertex_pc_directions[label_2] = pc_directions[(label_1, label_2)]
                        vertex_pc_origin[label_2] = pc_origin[(label_1, label_2)]
                    if (label_1 == 1): # no need to check `label_2` because labels are sorted in keys returned by `wall_voxels_per_cells_pairs`
                        epidermis_pc_values[label_2] = pc_values[(label_1, label_2)]
                        epidermis_pc_normal[label_2] = pc_normal[(label_1, label_2)]
                        epidermis_pc_directions[label_2] = pc_directions[(label_1, label_2)]
                        epidermis_pc_origin[label_2] = pc_origin[(label_1, label_2)]

                extend_edge_property_from_dictionary(graph, 'wall_principal_curvature_values', edge_pc_values, time_point=tp)
                extend_edge_property_from_dictionary(graph, 'wall_principal_curvature_normal', edge_pc_normal, time_point=tp)
                extend_edge_property_from_dictionary(graph, 'wall_principal_curvature_directions', edge_pc_directions, time_point=tp)
                if not 'wall_median' in graph.edge_properties():
                    extend_edge_property_from_dictionary(graph, 'wall_principal_curvature_origin', edge_pc_origin, time_point=tp)
                if vertex_pc_values != {}:
                    extend_vertex_property_from_dictionary(graph, 'unlabelled_wall_principal_curvature_values', vertex_pc_values, time_point=tp)
                    extend_vertex_property_from_dictionary(graph, 'unlabelled_wall_principal_curvature_normal', vertex_pc_normal, time_point=tp)
                    extend_vertex_property_from_dictionary(graph, 'unlabelled_wall_principal_curvature_directions', vertex_pc_directions, time_point=tp)
                    if not 'wall_median' in graph.edge_properties():
                        extend_vertex_property_from_dictionary(graph, 'unlabelled_wall_principal_curvature_origin', vertex_pc_origin, time_point=tp)
                if epidermis_pc_values != {}:
                    extend_vertex_property_from_dictionary(graph, 'epidermis_wall_principal_curvature_values', epidermis_pc_values, time_point=tp)
                    extend_vertex_property_from_dictionary(graph, 'epidermis_wall_principal_curvature_normal', epidermis_pc_normal, time_point=tp)
                    extend_vertex_property_from_dictionary(graph, 'epidermis_wall_principal_curvature_directions', epidermis_pc_directions, time_point=tp)
                    if not 'wall_median' in graph.edge_properties():
                        extend_vertex_property_from_dictionary(graph, 'epidermis_wall_principal_curvature_origin', epidermis_pc_origin, time_point=tp)

            if 'epidermis_local_principal_curvature' in spatio_temporal_properties:
                for radius in graph.graph_property('radius_2_compute'):
                    print 'Computing local_principal_curvature property with radius = {}voxels...'.format(radius)
                    print u"This represent a local curvature estimation area of {}\xb5m\xb2".format(round(math.pi*(radius*SpI_Analysis[tp].image.resolution[0])*(radius*SpI_Analysis[tp].image.resolution[1])))
                    SpI_Analysis[tp].principal_curvatures, SpI_Analysis[tp].principal_curvatures_normal, SpI_Analysis[tp].principal_curvatures_directions = {}, {}, {}
                    SpI_Analysis[tp].compute_principal_curvatures(vids=labels, radius=radius, verbose=True)
                    extend_vertex_property_from_dictionary(graph, 'epidermis_local_principal_curvature_values_r'+str(radius), SpI_Analysis[tp].principal_curvatures, time_point=tp)
                    extend_vertex_property_from_dictionary(graph, 'epidermis_local_principal_curvature_normal_r'+str(radius), SpI_Analysis[tp].principal_curvatures_normal, time_point=tp)
                    extend_vertex_property_from_dictionary(graph, 'epidermis_local_principal_curvature_directions_r'+str(radius), SpI_Analysis[tp].principal_curvatures_directions, time_point=tp)
                if not 'wall_median' in graph.edge_properties():
                    extend_vertex_property_from_dictionary(graph, 'epidermis_local_principal_curvature_origin', SpI_Analysis[tp].principal_curvatures_origin, time_point=tp)
                #embed()

            # - We want the `dict_wall_voxels` to be computed again at each `time_point`:
            try: del dict_wall_voxels
            except: pass

        # - We want to compute the 'epidermis_local_principal_curvature' for all time points:
        try: graph.remove_graph_property('radius_2_compute')
        except: pass

    return graph
