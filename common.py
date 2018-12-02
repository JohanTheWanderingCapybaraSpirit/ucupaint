import bpy, os, sys, re, time, numpy
from mathutils import *
from bpy.app.handlers import persistent
#from .__init__ import bl_info

BLENDER_28_GROUP_INPUT_HACK = False

TEXGROUP_PREFIX = '~yP Tex '
MASKGROUP_PREFIX = '~yP Mask '
ADDON_NAME = 'yTexLayers'

SOURCE_TREE_START = '__source_start_'
SOURCE_TREE_END = '__source_end_'
SOURCE_SOLID_VALUE = '__source_solid_'

MOD_TREE_START = '__mod_start_'
MOD_TREE_END = '__mod_end_'

MASK_TREE_START = '__mask_start_'
MASK_TREE_END = '__mask_end_'

blend_type_items = (("MIX", "Mix", ""),
	             ("ADD", "Add", ""),
	             ("SUBTRACT", "Subtract", ""),
	             ("MULTIPLY", "Multiply", ""),
	             ("SCREEN", "Screen", ""),
	             ("OVERLAY", "Overlay", ""),
	             ("DIFFERENCE", "Difference", ""),
	             ("DIVIDE", "Divide", ""),
	             ("DARKEN", "Darken", ""),
	             ("LIGHTEN", "Lighten", ""),
	             ("HUE", "Hue", ""),
	             ("SATURATION", "Saturation", ""),
	             ("VALUE", "Value", ""),
	             ("COLOR", "Color", ""),
	             ("SOFT_LIGHT", "Soft Light", ""),
	             ("LINEAR_LIGHT", "Linear Light", ""))

TEMP_UV = '~TL Temp Paint UV'

neighbor_directions = ['n', 's', 'e', 'w']

normal_blend_items = (
        ('MIX', 'Mix', ''),
        #('VECTOR_MIX', 'Vector Mix', ''),
        ('OVERLAY', 'Overlay', '')
        )

layer_type_items = (
        ('IMAGE', 'Image', ''),
        #('ENVIRONMENT', 'Environment', ''),
        ('BRICK', 'Brick', ''),
        ('CHECKER', 'Checker', ''),
        ('GRADIENT', 'Gradient', ''),
        ('MAGIC', 'Magic', ''),
        ('MUSGRAVE', 'Musgrave', ''),
        ('NOISE', 'Noise', ''),
        #('POINT_DENSITY', 'Point Density', ''),
        #('SKY', 'Sky', ''),
        ('VORONOI', 'Voronoi', ''),
        ('WAVE', 'Wave', ''),
        ('VCOL', 'Vertex Color', ''),
        ('BACKGROUND', 'Background', ''),
        ('COLOR', 'Solid Color', ''),
        ('GROUP', 'Group', ''),
        )

mask_type_items = (
        ('IMAGE', 'Image', ''),
        #('ENVIRONMENT', 'Environment', ''),
        ('BRICK', 'Brick', ''),
        ('CHECKER', 'Checker', ''),
        ('GRADIENT', 'Gradient', ''),
        ('MAGIC', 'Magic', ''),
        ('MUSGRAVE', 'Musgrave', ''),
        ('NOISE', 'Noise', ''),
        #('POINT_DENSITY', 'Point Density', ''),
        #('SKY', 'Sky', ''),
        ('VORONOI', 'Voronoi', ''),
        ('WAVE', 'Wave', ''),
        ('VCOL', 'Vertex Color', ''),
        )

layer_type_labels = {
        'IMAGE' : 'Image',
        #'ENVIRONMENT' : 'Environment',
        'BRICK' : 'Brick',
        'CHECKER' : 'Checker',
        'GRADIENT' : 'Gradient',
        'MAGIC' : 'Magic',
        'MUSGRAVE' : 'Musgrave',
        'NOISE' : 'Noise',
        #'POINT_DENSITY' : 'Point Density',
        #'SKY' : 'Sky',
        'VORONOI' : 'Voronoi',
        'WAVE' : 'Wave',
        'VCOL' : 'Vertex Color',
        'BACKGROUND' : 'Background',
        'COLOR' : 'Solid Color',
        'GROUP' : 'Layer Group',
        }

texcoord_type_items = (
        ('Generated', 'Generated', ''),
        ('Normal', 'Normal', ''),
        ('UV', 'UV', ''),
        ('Object', 'Object', ''),
        ('Camera', 'Camera', ''),
        ('Window', 'Window', ''),
        ('Reflection', 'Reflection', ''),
        )

channel_socket_input_bl_idnames = {
    'RGB': 'NodeSocketColor',
    'VALUE': 'NodeSocketFloatFactor',
    'NORMAL': 'NodeSocketVector',
}

channel_socket_output_bl_idnames = {
    'RGB': 'NodeSocketColor',
    'VALUE': 'NodeSocketFloat',
    'NORMAL': 'NodeSocketVector',
}

possible_object_types = {
        'MESH',
        'META',
        'CURVE',
        'SURFACE',
        'FONT'
        }

texture_node_types = {
        'TEX_IMAGE',
        'TEX_BRICK',
        'TEX_ENVIRONMENT',
        'TEX_CHECKER',
        'TEX_GRADIENT',
        'TEX_MAGIC',
        'TEX_MUSGRAVE',
        'TEX_NOISE',
        'TEX_POINTDENSITY',
        'TEX_SKY',
        'TEX_VORONOI',
        'TEX_WAVE',
        }

layer_node_bl_idnames = {
        'IMAGE' : 'ShaderNodeTexImage',
        'ENVIRONMENT' : 'ShaderNodeTexEnvironment',
        'BRICK' : 'ShaderNodeTexBrick',
        'CHECKER' : 'ShaderNodeTexChecker',
        'GRADIENT' : 'ShaderNodeTexGradient',
        'MAGIC' : 'ShaderNodeTexMagic',
        'MUSGRAVE' : 'ShaderNodeTexMusgrave',
        'NOISE' : 'ShaderNodeTexNoise',
        'POINT_DENSITY' : 'ShaderNodeTexPointDensity',
        'SKY' : 'ShaderNodeTexSky',
        'VORONOI' : 'ShaderNodeTexVoronoi',
        'WAVE' : 'ShaderNodeTexWave',
        'VCOL' : 'ShaderNodeAttribute',
        'BACKGROUND' : 'NodeGroupInput',
        'COLOR' : 'ShaderNodeRGB',
        'GROUP' : 'NodeGroupInput',
        }

GAMMA = 2.2

def get_current_version_str():
    bl_info = sys.modules[ADDON_NAME].bl_info
    return str(bl_info['version']).replace(', ', '.').replace('(','').replace(')','')

def get_active_material():
    scene = bpy.context.scene
    engine = scene.render.engine
    if not hasattr(bpy.context, 'object'): return None
    obj = bpy.context.object

    if not obj: return None

    mat = obj.active_material

    if engine in {'BLENDER_RENDER', 'BLENDER_GAME'}:
        return None

    return mat

def get_list_of_tl_nodes(mat):

    if not mat.node_tree: return []
    
    tl_nodes = []
    for node in mat.node_tree.nodes:
        if node.type == 'GROUP' and node.node_tree.tl.is_tl_node:
            tl_nodes.append(node)

    return tl_nodes

#def in_active_layer(obj):
#    scene = bpy.context.scene
#    space = bpy.context.space_data
#    if space.type == 'VIEW_3D' and space.local_view:
#        return any([layer for layer in obj.layers_local_view if layer])
#    else:
#        return any([layer for i, layer in enumerate(obj.layers) if layer and scene.layers[i]])

def get_addon_filepath():

    sep = os.sep

    # Search for addon dirs
    roots = bpy.utils.script_paths()

    possible_dir_names = [ADDON_NAME, ADDON_NAME + '-master']

    for root in roots:
        if os.path.basename(root) != 'scripts': continue
        filepath = root + sep + 'addons'

        dirs = next(os.walk(filepath))[1]
        folders = [x for x in dirs if x in possible_dir_names]

        if folders:
            return filepath + sep + folders[0] + sep

    return 'ERROR: No path found for yTexLayers!'

def srgb_to_linear_per_element(e):
    if e <= 0.03928:
        return e/12.92
    else: 
        return pow((e + 0.055) / 1.055, 2.4)

def linear_to_srgb_per_element(e):
    if e > 0.0031308:
        return 1.055 * (pow(e, (1.0 / 2.4))) - 0.055
    else: 
        return 12.92 * e

def srgb_to_linear(inp):

    if type(inp) == float:
        return srgb_to_linear_per_element(inp)

    elif type(inp) == Color:

        c = inp.copy()

        for i in range(3):
            c[i] = srgb_to_linear_per_element(c[i])

        return c

def linear_to_srgb(inp):

    if type(inp) == float:
        return linear_to_srgb_per_element(inp)

    elif type(inp) == Color:

        c = inp.copy()

        for i in range(3):
            c[i] = linear_to_srgb_per_element(c[i])

        return c

def copy_node_props_(source, dest, extras = []):
    #print()
    props = dir(source)
    filters = ['rna_type', 'name']
    filters.extend(extras)
    for prop in props:
        if prop.startswith('__'): continue
        if prop.startswith('bl_'): continue
        if prop in filters: continue
        val = getattr(source, prop)
        if 'bpy_func' in str(type(val)): continue
        # Copy stuff here
        try: 
            setattr(dest, prop, val)
            #print('SUCCESS:', prop, val)
        except: 
            #print('FAILED:', prop, val)
            pass

def copy_node_props(source ,dest, extras = []):
    # Copy node props
    copy_node_props_(source, dest, extras)

    if source.type == 'CURVE_RGB':
        
        # Copy mapping props
        copy_node_props_(source.mapping, dest.mapping)
        
        # Copy curve props
        for i, curve in enumerate(source.mapping.curves):
            curve_copy = dest.mapping.curves[i]
            copy_node_props_(curve, curve_copy)
    
            # Copy point props
            for j, point in enumerate(curve.points):
                if j >= len(curve_copy.points):
                    point_copy = curve_copy.points.new(point.location[0], point.location[1])
                else: point_copy = curve_copy.points[j]
                copy_node_props_(point, point_copy)
                
            # Copy selection
            for j, point in enumerate(curve.points):
                point_copy = curve_copy.points[j]
                point_copy.select = point.select
                
        # Update curve
        dest.mapping.update()
    
    elif source.type == 'VALTORGB':
    
        # Copy color ramp props
        copy_node_props_(source.color_ramp, dest.color_ramp)
        
        # Copy color ramp elements
        for i, elem in enumerate(source.color_ramp.elements):
            if i >= len(dest.color_ramp.elements):
                elem_copy = dest.color_ramp.elements.new(elem.position)
            else: elem_copy = dest.color_ramp.elements[i]
            copy_node_props_(elem, elem_copy)

    elif source.type in texture_node_types:

        # Copy texture mapping
        copy_node_props_(source.texture_mapping, dest.texture_mapping)

    # Copy inputs default value
    for i, inp in enumerate(source.inputs):
        dest.inputs[i].default_value = inp.default_value

    # Copy outputs default value
    for i, outp in enumerate(source.outputs):
        dest.outputs[i].default_value = outp.default_value 

def update_image_editor_image(context, image):
    for area in context.screen.areas:
        if area.type == 'IMAGE_EDITOR':
            if not area.spaces[0].use_image_pin:
                if area.spaces[0].image != image:
                    area.spaces[0].image = image

# Check if name already available on the list
def get_unique_name(name, items, surname = ''):

    if surname != '':
        unique_name = name + ' ' + surname
    else: unique_name = name

    name_found = [item for item in items if item.name == unique_name]
    if name_found:
        i = 1
        while True:

            if surname != '':
                new_name = name + ' ' + str(i) + ' ' + surname
            else: new_name = name + ' ' + str(i)

            name_found = [item for item in items if item.name == new_name]
            if not name_found:
                unique_name = new_name
                break
            i += 1

    return unique_name

def get_active_node():
    mat = get_active_material()
    if not mat or not mat.node_tree: return None
    node = mat.node_tree.nodes.active
    return node

# Specific methods for this addon

def get_active_cpaint_node():
    ycpui = bpy.context.window_manager.ycpui

    # Get material UI prop
    mat = get_active_material()
    if not mat or not mat.node_tree: 
        ycpui.active_mat = ''
        return None

    # Search for its name first
    mui = ycpui.materials.get(mat.name)

    # Flag for indicate new mui just created
    change_name = False

    # If still not found, create one
    if not mui:

        if ycpui.active_mat != '':
            prev_mat = bpy.data.materials.get(ycpui.active_mat)
            if not prev_mat:
                #print(ycpui.active_mat)
                change_name = True
                # Remove prev mui
                prev_idx = [i for i, m in enumerate(ycpui.materials) if m.name == ycpui.active_mat]
                if prev_idx:
                    ycpui.materials.remove(prev_idx[0])
                    #print('Removed!')

        mui = ycpui.materials.add()
        mui.name = mat.name
        #print('New MUI!', mui.name)

    if ycpui.active_mat != mat.name:
        ycpui.active_mat = mat.name

    # Try to get tl node
    node = get_active_node()
    if node and node.type == 'GROUP' and node.node_tree and node.node_tree.tl.is_tl_node:
        # Update node name
        if mui.active_tl_node != node.name:
            #print('From:', mui.active_tl_node)
            mui.active_tl_node = node.name
            #print('To:', node.name)
        if ycpui.active_tl_node != node.name:
            ycpui.active_tl_node = node.name
        return node

    # If not active node isn't a group node
    # New mui possibly means material name just changed, try to get previous active node
    if change_name: 
        node = mat.node_tree.nodes.get(ycpui.active_tl_node)
        if node:
            #print(mui.name, 'Change name from:', mui.active_tl_node)
            mui.active_tl_node = node.name
            #print(mui.name, 'Change name to', mui.active_tl_node)
            return node

    node = mat.node_tree.nodes.get(mui.active_tl_node)
    #print(mui.active_tl_node, node)
    if node: return node

    # If node still not found
    for node in mat.node_tree.nodes:
        if node.type == 'GROUP' and node.node_tree and node.node_tree.tl.is_tl_node:
            #print('Last resort!', mui.name, mui.active_tl_node)
            mui.active_tl_node = node.name
            return node

    return None

def remove_node(tree, entity, prop, remove_data=True, obj=None):
    if not hasattr(entity, prop): return
    #if prop not in entity: return

    scene = bpy.context.scene
    node = tree.nodes.get(getattr(entity, prop))
    #node = tree.nodes.get(entity[prop])

    if node: 
        if remove_data:
            # Remove image data if the node is the only user
            if node.bl_idname == 'ShaderNodeTexImage':
                image = node.image
                if image:
                    if ((scene.tool_settings.image_paint.canvas == image and image.users == 2) or
                        (scene.tool_settings.image_paint.canvas != image and image.users == 1)):
                        bpy.data.images.remove(image)

            elif node.bl_idname == 'ShaderNodeGroup':
                if node.node_tree and node.node_tree.users == 1:
                    bpy.data.node_groups.remove(node.node_tree)

            elif (obj and obj.type == 'MESH' #and obj.active_material and obj.active_material.users == 1
                    and hasattr(entity, 'type') and entity.type == 'VCOL' and node.bl_idname == 'ShaderNodeAttribute'):
                vcol = obj.data.vertex_colors.get(node.attribute_name)

                T = time.time()

                # Check if other layer use this vertex color
                other_users_found = False
                for ng in bpy.data.node_groups:
                    for t in ng.tl.layers:

                        # Search for vcol layer
                        if t.type == 'VCOL':
                            src = get_layer_source(t)
                            if src != node and src.attribute_name == vcol.name:
                                other_users_found = True
                                break

                        # Search for mask layer
                        for m in t.masks:
                            if m.type == 'VCOL':
                                src = get_mask_source(m)
                                if src != node and src.attribute_name == vcol.name:
                                    other_users_found = True
                                    break

                print('INFO: Searching on entire node groups to search for vcol takes', '{:0.2f}'.format((time.time() - T) * 1000), 'ms!')

                #other_user_found = False
                #for t in tl.layers:
                #    if t.type == 'VCOL':
                if not other_users_found:
                    obj.data.vertex_colors.remove(vcol)

        # Remove the node itself
        #print('Node ' + prop + ' from ' + str(entity) + ' removed!')
        tree.nodes.remove(node)

    setattr(entity, prop, '')
    #entity[prop] = ''

def mute_node(tree, entity, prop):
    if not hasattr(entity, prop): return
    node = tree.nodes.get(getattr(entity, prop))
    if node: node.mute = True

def unmute_node(tree, entity, prop):
    if not hasattr(entity, prop): return
    node = tree.nodes.get(getattr(entity, prop))
    if node: node.mute = False

def new_node(tree, entity, prop, node_id_name, label=''):
    ''' Create new node '''
    if not hasattr(entity, prop): return
    
    # Create new node
    node = tree.nodes.new(node_id_name)

    # Set node name to object attribute
    setattr(entity, prop, node.name)

    # Set label
    node.label = label

    return node

def check_new_node(tree, entity, prop, node_id_name, label=''):
    ''' Check if node is available, if not, create one '''

    # Try to get the node first
    try: node = tree.nodes.get(getattr(entity, prop))
    except: return None

    # Create new node if not found
    if not node:
        node = new_node(tree, entity, prop, node_id_name, label)

    return node

def check_duplicated_node_group(node_group):

    for node in node_group.nodes:
        if node.type == 'GROUP' and node.node_tree:

            # Check if its node tree duplicated
            m = re.match(r'^(.+)\.\d{3}$', node.node_tree.name)
            if m:
                ng = bpy.data.node_groups.get(m.group(1))
                if ng:
                    #print(node.node_tree.name)

                    # Remember current tree
                    prev_tree = node.node_tree

                    # Replace new node
                    node.node_tree = ng

                    # Remove previous tree
                    if prev_tree.users == 0:
                        bpy.data.node_groups.remove(prev_tree)

            check_duplicated_node_group(node.node_tree)

def get_node_tree_lib(name):
    # Node groups necessary are in nodegroups_lib.blend
    filepath = get_addon_filepath() + "lib.blend"

    appended = False
    with bpy.data.libraries.load(filepath) as (data_from, data_to):

        # Load node groups
        exist_groups = [ng.name for ng in bpy.data.node_groups]
        for ng in data_from.node_groups:
            if ng == name and ng not in exist_groups:

                data_to.node_groups.append(ng)
                appended = True

                break

    node_tree = bpy.data.node_groups.get(name)

    # Check if another group is exists inside the group
    if node_tree and appended:
        check_duplicated_node_group(node_tree)

    return node_tree

def replace_new_node(tree, entity, prop, node_id_name, label='', group_name='', return_status=False):
    ''' Check if node is available, replace if available '''

    # Try to get the node first
    try: node = tree.nodes.get(getattr(entity, prop))
    except: return None, False

    replaced = False

    # Remove node if found and has different id name
    if node and node.bl_idname != node_id_name:
        remove_node(tree, entity, prop)
        node = None

    # Create new node
    if not node:
        node = new_node(tree, entity, prop, node_id_name, label)
        replaced = True

    if node.type == 'GROUP':

        # Get previous tree
        prev_tree = node.node_tree

        # Check if group is copied
        if prev_tree:
            m = re.match(r'^' + group_name + '_Copy\.*\d{0,3}$', prev_tree.name)
        else: m = None

        #print(prev_tree)

        if not prev_tree or (prev_tree.name != group_name and not m):

            # Replace group tree
            node.node_tree = get_node_tree_lib(group_name)

            if not prev_tree:
                replaced = True

            else:
                # Compare previous group inputs with current group inputs
                if len(prev_tree.inputs) != len(node.inputs):
                    replaced = True
                else:
                    for i, inp in enumerate(node.inputs):
                        if inp.name != prev_tree.inputs[i].name:
                            replaced = True
                            break

                # Remove previous tree if it has no user
                if prev_tree.users == 0:
                    bpy.data.node_groups.remove(prev_tree)

    if return_status:
        return node, replaced

    return node

def get_tree(entity):

    #m = re.match(r'tl\.layers\[(\d+)\]', entity.path_from_id())
    #if not m: return None
    #if not hasattr(entity.id_data, 'tl') or not hasattr(entity, 'group_node'): return None

    try:
        tree = entity.id_data
        tl = tree.tl
        group_node = tree.nodes.get(entity.group_node)
        #if not group_node or group_node.type != 'GROUP': return None
        return group_node.node_tree
    except: 
        return None

def get_mod_tree(entity):

    tl = entity.id_data.tl

    m = re.match(r'^tl\.channels\[(\d+)\].*', entity.path_from_id())
    if m:
        return entity.id_data

    m = re.match(r'^tl\.layers\[(\d+)\]\.channels\[(\d+)\].*', entity.path_from_id())
    if m:
        layer = tl.layers[int(m.group(1))]
        ch = layer.channels[int(m.group(2))]
        tree = get_tree(layer)

        mod_group = tree.nodes.get(ch.mod_group)
        if mod_group and mod_group.type == 'GROUP':
            return mod_group.node_tree

        return tree

    m = re.match(r'^tl\.layers\[(\d+)\].*', entity.path_from_id())
    if m:
        layer = tl.layers[int(m.group(1))]
        tree = get_tree(layer)

        source_group = tree.nodes.get(layer.source_group)
        if source_group and source_group.type == 'GROUP': 
            tree = source_group.node_tree

        mod_group = tree.nodes.get(layer.mod_group)
        if mod_group and mod_group.type == 'GROUP':
            return mod_group.node_tree

        return tree

def get_mask_tree(mask):

    m = re.match(r'tl\.layers\[(\d+)\]\.masks\[(\d+)\]', mask.path_from_id())
    if not m : return None

    tl = mask.id_data.tl
    layer = tl.layers[int(m.group(1))]
    layer_tree = get_tree(layer)

    group_node = layer_tree.nodes.get(mask.group_node)
    if not group_node or group_node.type != 'GROUP': return layer_tree
    return group_node.node_tree

def get_mask_source(mask):
    tree = get_mask_tree(mask)
    return tree.nodes.get(mask.source)

def get_mask_mapping(mask):
    tree = get_mask_tree(mask)
    return tree.nodes.get(mask.mapping)

def get_source_tree(layer, tree=None):
    if not tree: tree = get_tree(layer)
    if not tree: return None

    if layer.source_group != '':
        source_group = tree.nodes.get(layer.source_group)
        return source_group.node_tree

    return tree

def get_layer_source(layer, tree=None):
    if not tree: tree = get_tree(layer)

    source_tree = get_source_tree(layer, tree)
    if source_tree: return source_tree.nodes.get(layer.source)
    if tree: return tree.nodes.get(layer.source)

    return None

def get_layer_mapping(layer):
    tree = get_source_tree(layer)
    return tree.nodes.get(layer.mapping)

def get_neighbor_uv_space_input(texcoord_type):
    if texcoord_type == 'UV':
        return 0.0 # Tangent Space
    if texcoord_type in {'Generated', 'Normal', 'Object'}:
        return 1.0 # Object Space
    if texcoord_type in {'Camera', 'Window', 'Reflection'}: 
        return 2.0 # View Space

def change_layer_name(tl, obj, src, layer, texes):
    if tl.halt_update: return

    tl.halt_update = True

    if layer.type == 'VCOL' and obj.type == 'MESH':

        # Get vertex color from node
        vcol = obj.data.vertex_colors.get(src.attribute_name)

        # Temporarily change its name to temp name so it won't affect unique name
        vcol.name = '___TEMP___'

        # Get unique name
        layer.name = get_unique_name(layer.name, obj.data.vertex_colors) 

        # Set vertex color name and attribute node
        vcol.name = layer.name
        src.attribute_name = layer.name

    elif layer.type == 'IMAGE':
        src.image.name = '___TEMP___'
        layer.name = get_unique_name(layer.name, bpy.data.images) 
        src.image.name = layer.name

    else:
        name = layer.name
        layer.name = '___TEMP___'
        layer.name = get_unique_name(name, texes) 

    tl.halt_update = False

def set_obj_vertex_colors(obj, vcol, color):
    if obj.type != 'MESH': return

    if bpy.app.version_string.startswith('2.8'):
        col = (color[0], color[1], color[2], 1.0)
    else: col = color

    for poly in obj.data.polygons:
        for loop_index in poly.loop_indices:
            vcol.data[loop_index].color = col

def force_bump_base_value(tree, ch, value):
    col = (value, value, value, 1.0)

    bump_base = tree.nodes.get(ch.bump_base)
    if bump_base: bump_base.inputs[1].default_value = col

    neighbor_directions = ['n', 's', 'e', 'w']
    for d in neighbor_directions:
        b = tree.nodes.get(getattr(ch, 'bump_base_' + d))
        if b: b.inputs[1].default_value = col

    #for mod in ch.modifiers:
    #    if mod.type == 'OVERRIDE_COLOR' and mod.oc_use_normal_base:
    #        mod.oc_col = col

def update_bump_base_value_(tree, ch):
    force_bump_base_value(tree, ch, ch.bump_base_value)
    
def get_transition_bump_channel(layer):
    tl = layer.id_data.tl

    bump_ch = None
    for i, ch in enumerate(layer.channels):
        if tl.channels[i].type == 'NORMAL' and ch.enable and ch.enable_transition_bump:
            bump_ch = ch
            break

    return bump_ch

def get_showed_transition_bump_channel(layer):

    tl = layer.id_data.tl

    bump_ch = None
    for i, ch in enumerate(layer.channels):
        if tl.channels[i].type == 'NORMAL' and ch.show_transition_bump:
            bump_ch = ch
            break

    return bump_ch

# BLENDER_28_GROUP_INPUT_HACK
def duplicate_lib_node_tree(node):
    node.node_tree.name += '_Copy'
    if node.node_tree.users > 1:
        node.node_tree = node.node_tree.copy()

    # Make sure input match to actual node its connected to
    for n in node.node_tree.nodes:
        if n.type == 'GROUP_INPUT':
            for i, inp in enumerate(node.inputs):
                for link in n.outputs[i].links:
                    try: link.to_socket.default_value = node.inputs[i].default_value
                    except: pass

def match_group_input(node, key=None, extra_node_names=[]):

    input_node_names = ['Group Input']
    input_node_names.extend(extra_node_names)

    for name in input_node_names:
        try:
            n = node.node_tree.nodes.get(name)
            if not key: outputs = n.outputs
            else: outputs = [n.outputs[key]]
        except: continue

        for outp in outputs:
            for link in outp.links:
                try: 
                    if link.to_socket.default_value != node.inputs[outp.name].default_value:
                        link.to_socket.default_value = node.inputs[outp.name].default_value
                except: pass

def fix_io_index(item, items, correct_index):
    cur_index = [i for i, it in enumerate(items) if it == item]
    if cur_index and cur_index[0] != correct_index:
        items.move(cur_index[0], correct_index)

def get_layer_depth(layer):

    tl = layer.id_data.tl

    upmost_found = False
    depth = 0
    cur_tex = layer
    parent_tex = layer

    while True:
        if cur_tex.parent_idx != -1:

            try: layer = tl.layers[cur_tex.parent_idx]
            except: break

            if layer.type == 'GROUP':
                parent_tex = layer
                depth += 1

        if parent_tex == cur_tex:
            break

        cur_tex = parent_tex

    return depth

def is_top_member(layer):
    
    if layer.parent_idx == -1:
        return False

    tl = layer.id_data.tl

    for i, t in enumerate(tl.layers):
        if t == layer:
            if layer.parent_idx == i-1:
                return True
            else: return False

    return False

def is_bottom_member(layer):

    if layer.parent_idx == -1:
        return False

    tl = layer.id_data.tl

    tex_idx = -1
    last_member_idx = -1
    for i, t in enumerate(tl.layers):
        if t == layer:
            tex_idx = i
        if t.parent_idx == layer.parent_idx:
            last_member_idx = i

    if tex_idx == last_member_idx:
        return True

    return False

#def get_upmost_parent_idx(layer, idx_limit = -1):
#
#    tl = layer.id_data.tl
#
#    cur_tex = layer
#    parent_tex = layer
#    parent_idx = -1
#
#    while True:
#        if cur_tex.parent_idx != -1 and cur_tex.parent_idx != idx_limit:
#
#            try: layer = tl.layers[cur_tex.parent_idx]
#            except: break
#
#            if layer.type == 'GROUP':
#                parent_tex = layer
#                parent_idx = cur_tex.parent_idx
#
#        if parent_tex == cur_tex:
#            break
#
#        cur_tex = parent_tex
#
#    return parent_idx

def get_layer_index(layer):
    tl = layer.id_data.tl

    for i, t in enumerate(tl.layers):
        if layer == t:
            return i

def get_layer_index_by_name(tl, name):

    for i, t in enumerate(tl.layers):
        if name == t.name:
            return i

    return -1

def get_parent_dict(tl):
    parent_dict = {}
    for t in tl.layers:
        if t.parent_idx != -1:
            try: parent_dict[t.name] = tl.layers[t.parent_idx].name
            except: parent_dict[t.name] = None
        else: parent_dict[t.name] = None

    return parent_dict

def get_parent(layer):

    tl = layer.id_data.tl
    
    if layer.parent_idx == -1:
        return None

    return tl.layers[layer.parent_idx]

def is_parent_hidden(layer):

    tl = layer.id_data.tl

    hidden = False
    
    cur_tex = layer
    parent_tex = layer

    while True:
        if cur_tex.parent_idx != -1:

            try: layer = tl.layers[cur_tex.parent_idx]
            except: break

            if layer.type == 'GROUP':
                parent_tex = layer
                if not parent_tex.enable:
                    hidden = True
                    break

        if parent_tex == cur_tex:
            break

        cur_tex = parent_tex

    return hidden

def set_parent_dict_val(tl, parent_dict, name, target_idx):

    if target_idx != -1:
        parent_dict[name] = tl.layers[target_idx].name
    else: parent_dict[name] = None

    return parent_dict

def get_list_of_direct_child_ids(layer):
    tl = layer.id_data.tl

    if layer.type != 'GROUP':
        return []

    tex_idx = get_layer_index(layer)

    childs = []
    for i, t in enumerate(tl.layers):
        if t.parent_idx == tex_idx:
            childs.append(i)

    return childs

def get_list_of_direct_childrens(layer):
    tl = layer.id_data.tl

    if layer.type != 'GROUP':
        return []

    tex_idx = get_layer_index(layer)

    childs = []
    for t in tl.layers:
        if t.parent_idx == tex_idx:
            childs.append(t)

    return childs

def get_list_of_parent_ids(layer):

    tl = layer.id_data.tl

    cur_tex = layer
    parent_tex = layer
    parent_list = []

    while True:
        if cur_tex.parent_idx != -1:

            try: layer = tl.layers[cur_tex.parent_idx]
            except: break

            if layer.type == 'GROUP':
                parent_tex = layer
                parent_list.append(cur_tex.parent_idx)

        if parent_tex == cur_tex:
            break

        cur_tex = parent_tex

    return parent_list

def get_last_chained_up_layer_ids(layer, idx_limit):

    tl = layer.id_data.tl
    tex_idx = get_layer_index(layer)

    cur_tex = layer
    parent_tex = layer
    parent_idx = tex_idx

    while True:
        if cur_tex.parent_idx != -1 and cur_tex.parent_idx != idx_limit:

            try: layer = tl.layers[cur_tex.parent_idx]
            except: break

            if layer.type == 'GROUP':
                parent_tex = layer
                parent_idx = cur_tex.parent_idx

        if parent_tex == cur_tex:
            break

        cur_tex = parent_tex

    return parent_idx

def has_childrens(layer):

    tl = layer.id_data.tl

    if layer.type != 'GROUP':
        return False

    tex_idx = get_layer_index(layer)

    if tex_idx < len(tl.layers)-1:
        neighbor_tex = tl.layers[tex_idx+1]
        if neighbor_tex.parent_idx == tex_idx:
            return True

    return False

def get_last_child_idx(layer): #, very_last=False):

    tl = layer.id_data.tl
    tex_idx = get_layer_index(layer)

    if layer.type != 'GROUP': 
        return tex_idx

    for i, t in reversed(list(enumerate(tl.layers))):
        if i > tex_idx and tex_idx in get_list_of_parent_ids(t):
            return i

    return tex_idx

def get_upper_neighbor(layer):

    tl = layer.id_data.tl
    tex_idx = get_layer_index(layer)

    if tex_idx == 0:
        return None, None

    if layer.parent_idx == tex_idx-1:
        return tex_idx-1, tl.layers[tex_idx-1]

    upper_tex = tl.layers[tex_idx-1]

    neighbor_idx = get_last_chained_up_layer_ids(upper_tex, layer.parent_idx)
    neighbor_tex = tl.layers[neighbor_idx]

    return neighbor_idx, neighbor_tex

def get_lower_neighbor(layer):

    tl = layer.id_data.tl
    tex_idx = get_layer_index(layer)
    last_index = len(tl.layers)-1

    if tex_idx == last_index:
        return None, None

    if layer.type == 'GROUP':
        last_child_idx = get_last_child_idx(layer)

        if last_child_idx == last_index:
            return None, None

        neighbor_idx = last_child_idx + 1
    else:
        neighbor_idx = tex_idx+1

    neighbor_tex = tl.layers[neighbor_idx]

    return neighbor_idx, neighbor_tex

def is_valid_to_remove_bump_nodes(layer, ch):

    if layer.type == 'COLOR' and ((ch.enable_transition_bump and ch.enable) or len(layer.masks) == 0 or ch.transition_bump_chain == 0):
        return True

    return False

def set_uv_neighbor_resolution(entity, uv_neighbor=None, source=None, mapping=None):

    tl = entity.id_data.tl
    m1 = re.match(r'^tl\.layers\[(\d+)\]$', entity.path_from_id())
    m2 = re.match(r'^tl\.layers\[(\d+)\]\.masks\[(\d+)\]$', entity.path_from_id())

    if m1: 
        tree = get_tree(entity)
        if not mapping: mapping = get_layer_mapping(entity)
        if not source: source = get_layer_source(entity)
    elif m2: 
        tree = get_tree(tl.layers[int(m2.group(1))])
        if not mapping: mapping = get_mask_mapping(entity)
        if not source: source = get_mask_source(entity)
    else: return

    if not uv_neighbor: uv_neighbor = tree.nodes.get(entity.uv_neighbor)
    if not uv_neighbor: return

    if entity.type == 'IMAGE' and source.image:
        uv_neighbor.inputs[1].default_value = source.image.size[0] * mapping.scale[0]
        uv_neighbor.inputs[2].default_value = source.image.size[1] * mapping.scale[1]
    else:
        uv_neighbor.inputs[1].default_value = 1000
        uv_neighbor.inputs[2].default_value = 1000

def update_mapping(entity):

    m1 = re.match(r'^tl\.layers\[(\d+)\]$', entity.path_from_id())
    m2 = re.match(r'^tl\.layers\[(\d+)\]\.masks\[(\d+)\]$', entity.path_from_id())

    # Get source
    if m1: 
        source = get_layer_source(entity)
        mapping = get_layer_mapping(entity)
    elif m2: 
        source = get_mask_source(entity)
        mapping = get_mask_mapping(entity)
    else: return

    if not mapping: return

    tl = entity.id_data.tl

    offset_x = entity.translation[0]
    offset_y = entity.translation[1]
    offset_z = entity.translation[2]

    scale_x = entity.scale[0]
    scale_y = entity.scale[1]
    scale_z = entity.scale[2]

    if entity.type == 'IMAGE' and entity.segment_name != '':
        image = source.image
        segment = image.yia.segments.get(entity.segment_name)

        scale_x = segment.width/image.size[0] * scale_x
        scale_y = segment.height/image.size[1] * scale_y

        offset_x = scale_x * segment.tile_x + offset_x * scale_x
        offset_y = scale_y * segment.tile_y + offset_y * scale_y

    mapping.translation = (offset_x, offset_y, offset_z)
    mapping.rotation = entity.rotation
    mapping.scale = (scale_x, scale_y, scale_z)

    set_uv_neighbor_resolution(entity, source=source, mapping=mapping)

    if entity.type == 'IMAGE' and entity.texcoord_type == 'UV':
        if m1 or (m2 and entity.active_edit):
            tl.need_temp_uv_refresh = True

def is_transformed(mapping):
    if (mapping.translation[0] != 0.0 or
        mapping.translation[1] != 0.0 or
        mapping.translation[2] != 0.0 or
        mapping.rotation[0] != 0.0 or
        mapping.rotation[1] != 0.0 or
        mapping.rotation[2] != 0.0 or
        mapping.scale[0] != 1.0 or
        mapping.scale[1] != 1.0 or
        mapping.scale[2] != 1.0
        ):
        return True
    return False

def refresh_temp_uv(obj, entity, use_ops=False):

    #if not entity or entity.segment_name == '' or entity.type != 'IMAGE':
    if not entity or entity.type != 'IMAGE': # or not is_transformed(entity):
        return False

    #tl = entity.id_data.tl
    #tl.need_temp_uv_refresh = False

    m1 = re.match(r'^tl\.layers\[(\d+)\]$', entity.path_from_id())
    m2 = re.match(r'^tl\.layers\[(\d+)\]\.masks\[(\d+)\]$', entity.path_from_id())

    # Get source
    if m1: 
        source = get_layer_source(entity)
        mapping = get_layer_mapping(entity)
    elif m2: 
        source = get_mask_source(entity)
        mapping = get_mask_mapping(entity)
    else: return False

    if bpy.app.version_string.startswith('2.8'):
        uv_layers = obj.data.uv_layers
    else: uv_layers = obj.data.uv_textures

    if uv_layers.active != uv_layers[entity.uv_name]:
        uv_layers.active = uv_layers[entity.uv_name]

    # Delete previous temp uv
    for uv in uv_layers:
        if uv.name == TEMP_UV:
            uv_layers.remove(uv)

    if not is_transformed(mapping):
        return False

    img = source.image
    if not img: return False

    # New uv layers
    temp_uv_layer = uv_layers.new(TEMP_UV)
    uv_layers.active = temp_uv_layer

    # Cannot do this on edit mode
    ori_mode = obj.mode
    if ori_mode == 'EDIT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # Create transformation matrix
    # Scale
    m = Matrix((
        (mapping.scale[0], 0, 0),
        (0, mapping.scale[1], 0),
        (0, 0, mapping.scale[2])
        ))

    # Rotate
    m.rotate(Euler((mapping.rotation[0], mapping.rotation[1], mapping.rotation[2])))

    # Translate
    m = m.to_4x4()
    m[0][3] = mapping.translation[0]
    m[1][3] = mapping.translation[1]
    m[2][3] = mapping.translation[2]

    # Create numpy array to store uv coordinates
    arr = numpy.zeros(len(obj.data.loops)*2, dtype=numpy.float32)
    obj.data.uv_layers.active.data.foreach_get('uv', arr)
    arr.shape = (arr.shape[0]//2, 2)

    # Matrix transformation for each uv coordinates
    for uv in arr:
        vec = Vector((uv[0], uv[1], 0.0))
        vec = m * vec
        uv[0] = vec[0]
        uv[1] = vec[1]

    # Set back uv coordinates
    obj.data.uv_layers.active.data.foreach_set('uv', arr.ravel())

    # Back to edit mode if originally from there
    if ori_mode == 'EDIT':
        bpy.ops.object.mode_set(mode='EDIT')

    return True

#def get_io_index(layer, root_ch, alpha=False):
#    if alpha:
#        return root_ch.io_index+1
#    return root_ch.io_index
#
#def get_alpha_io_index(layer, root_ch):
#    return get_io_index(layer, root_ch, alpha=True)

# Some image_ops need this
#def get_active_image():
#    node = get_active_cpaint_node()
#    if not node: return None
#    tl = node.node_tree.tl
#    nodes = node.node_tree.nodes
#    if len(tl.layers) == 0: return None
#    layer = tl.layers[tl.active_layer_index]
#    if layer.type != 'ShaderNodeTexImage': return None
#    source = nodes.get(layer.source)
#    return source.image
