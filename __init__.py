# TODO (Immediate):
# - Musgrave texture (V)
# - Color layer (V)
# - Transparent/Background layer (V)
# - Eevee support (V)
# - Masking (V)
#   - Replace total mask node and implement transition bump/ramp chain system (V)
#   - Active Mask switcher on the list (V)
#   - Make sure mask has blending option consistency (X, Meh, its consistent enough)
#   - Mask transition factor (X, can be kinda replaced by out of chain mask)
#   - Mask modifiers
#       - Ramp (V)
#       - Invert (V)
# - Transition effects (V)
#   - Bump (V)
#   - Ramp (V)
#   - Flip bump mode (V)
#   - AO (V)
#   - Make transition effect option hidden in add modifier menu (V)
#   - Option for transition ao link with channel intensity (V)
#   - Per channel transition edge intensity (V)
#   - AO option to exclude area within intensity (V)
#   - AO and ramp contribute to alpha (V)
#   - AO works with background layer (V)
#   - Crease (V)
#   - Non flip bump background layer (V, still miss bump and ramp effect)
# - More modifier
#   - Intensity ramp (X, useless)
# - Layer group/folder
#   - Basic multilevel implementation (V)
#   - Works with mask and transition effects (V)
#   - Change layer type as group or vice versa (can be very very useful if working on mask first) (V)
# - New layer/mask improvements
#   - Open Image as Mask (V)
#   - Open Vcol as Mask/Layer (V)
#   - Add mask option when creating new layer (V)
#   - Remove RGB to Intensity when creating new layer bc its no longer necessary (X, why remove a feature?)
# - Lazy channel nodes (?)
#   - Nodes won't exists until it's enabled (X, replaced with next point)
#   - Blend nodes will be muted at default if not enabled (X, replaced with disable quick toggles)
#   - Add option to Optimize the entire yp nodes (X, replaced with disable quick toggles)
#   - Add Disable quick toggle options (V)
# - Very large image (UDIM like) to prevent number of image limits
#   - Basic implementation (Add/Delete/Edit UV) (V)
#   - Support for HDR (V)
#   - Dealing with layer name (V, good enough)
# - lib.blend
#   - Prefix for node group lib  (V)
#   - Create automatic frame node (V)
#   - Make better node group library update system (V)
#   - Update duplicated/single user library (V)
# - Bake
#   - Basic implementation (V)
#   - Bake layer group (X, mostly useless)
#   - Blender 2.8 normal bug workaround (V)
#   - Folder for auto save bake results (~, replaced by standard/pack menu)
#   - Dealing with multiple yp tree users (~, just implemented better fix duplicate layers operator) (V)
#   - Pointiness (V)
#   - AO (V)
#   - Overwrite AO or Pointiness (V)
#   - AO Distance (V)
# - Make sure background layer blending and its ui is consistent (V)
# - Make sure there's no duplicate group when appending (V)
# - Every modifiers has intensity value for muting to prevent recompilation (V)
# - Fix change blend type behavior where it always delete previous node (V)
# - Add intensity multiplier to non transition bump (X, transition already do the job)
# - Oveeride color should be override value for value channel (V)
# - Make sure ui is expanded if modifier or transition is added (V)
# - Multiple yp node selector from ui (V)
# - Replace new node can detect duplicated node group (V)
# - Transfer UV (V)
# - Add more comments to blender bug report about reflection fix (It should be only calculated on glossy/reflection code, not on diffuse)
# - Refactor for more consistent class names and properties (V)
# - Fix backface consistency with Blender 2.8 & 2.7 (V)
# - Height based bump channel (similar to substance) (V)
# - Per layer preview (V)
# - Duplicate layer (V)
# - Merge layer/mask (~V, still a simple implementation but useful)
# - Show warning if active uv isn't the transformed one (~V, don't remember exactly)
# - Add Emission Quick Node Setup (V)
# - Prevent unused channel bake (V)
# - Add simple vertex color editor on layer manager (V)
# - Temporary bake hemi/fake lighting so it can works with bump on cycles (V)
# - Add support for baking vertex color to image (X, kinda not needed)
# - Add clamp color option on root channel (V)
# - FXAA option when baking (V)
# - FXAA should not be a default because of the slowness (X, now, it's faster by hiding other objects)
# - Fake lighting type should be added on create fake lighting dialog box (V)
# - Mask blending should be added on create new mask dialog box (V)
# - Add Mask Preview Mode (V)
# - Image atlas should be not at default, so maximum images warning is needed (X)
# - ..or, check the possibility of not updating temp uv except on paint mode (check paint mode event perhaps?) (V)
# - Fake lighting should take account previous normal output (V)
# - Create image container node outside yp group to make layer images linked to mesh, especially on edit mode (X)
#   (doesn't need since image editor automatically update even with pinned image on 'UV Editing' workspace
# - Remove yp node and keep baked images (V)
# - Make rebake as an option on layer source (V)
# - Clean up bake codes (Erase double prepare bake codes) (V)
# - Normal map should not display bump height (V)
# - Object index mask should not generate neighbor uv (V)
# - Override value should be more accessible for layer value channel (V)
# - Add option to use own image/texture as layer channel (V)
# - Add option to add multiple images all at once as one layer (V)
# - Parallax height tweak (V)
# - Replace override color modifier with new override system (V)
# - Add option to move baked images to outside of yp node so it can be recognized by exporters (V)
# - Add option to save all baked images to folder (V)
# - Quick setup should use already used inputs to bsdf as inputs for yp node (V)
# - Still baking channel with connected input even if there are no layers using it (V)
# - Blender 2.80+ should use vertex paint transparency (V)
# - Use new blender own resize image operator (V)
# - Normal channel should be able to override both normal and bump at the same time (V)
# - Image editor should be able to show srgb color (V)
# - Add quick Flip Y toggle to normal image override (Y)
# - Add normal map strength slider (V)
# - Need ability to edit height channel main uv (V)
# - Add operator to create new UV map on multiple objects using the same material
# - Change link inside group to github insted of patreon

# TODO:
# - Make every node name unique (using hash?)
# - Deals with blender 2.8 vertex color alpha
# - Eraser brush (check for ypanel implementation)
# - Using only one channel on layer mask
# - Node Group Layer (Smart Material?)
# - Upper layer affect below layer (?):
#   - Refraction
#   - Blur (X?, Already covered by native SSS)
# - Matcap view on Normal preview
# - Transition
#   - Ramp works with non flip background (V, too complicated and has little use)
#   - Bump works with non flip background (V, too complicated and has little use)
# - Bake extra
#   - Highpoly
#   - Blur (can be only applied on select layer channel)
#   - 'Ignore below' blend for bake channel result
# - Armory support (X, proper bake system is better be the solution)
# - FXAA image operator to remove jagged pixels from baking or bucket fill (V)
# - Blur image operator
# - Add greater than and less than operation to object index mask (?)
# - Add option to bake generated textures to improve performance (X, too much hassle to implement)
# - Optimize hidden layer, maybe create a trash nodes to collect unused layers (?, Need to investigate the effeciveness more)
# - Support for opening UDIM images (?)
# - Support for baking to UDIM images (?)
# - Some texture should be able to use transparency
# - Combine objects before bake all channel to improve speed and fix margin issue
# - Merge layers should work on any type of layers (just convert them to standard image)
# - Add options to change neighbor uv value when using smooth bump
# - Add override normal on group node
#
# TODO OPT:
# - Lazy node calling (can be useful to prevent missing error)
#
# BUGS:
# - Fine bump still produces wrong result when using non UV texture mapping (V)
# - Sharp bump can cause bleed on color channel (V)
# - Value channel should output only grayscale (V)
# - Wrong result after adding layer modifier (V, need more testing)
# - Transition AO at flip produce wrong result (V)
# - Bring back modifier on normal channel at Color layer (V)
# - Childen layers produce wrong result after delete parent only (V)
# - Float image still lose precision after packed (its very apparent on bump effect) (V, not a problem on Blender 2.8)
# - Musgrave fine bump cannot read below 0.0 (??)
# - Bake result is slightly darker when using emission shader (or any shader?? not thoroughly tested yet)
# - UV overlay on image editor is not transformed if uv is transformed (V)
# - Standard image layer fails to use image atlas (V)
# - Layer preview mode does not change to missing color when enabling/disabling layer (V)
# - Bake crashes on Blender 2.90.1 (V, Blender 2.91 fixes it)
# - Wrong temp UV if layer selected again (V, maybe)
# - Alpha fails to connect to original target socket when toggling channel use alpha
# - No number suffix when creating new image mask
# - No number suffix when duplicate layers
# - Rename vcol that used in other layer caused missing data
# - Refresh Neighbor UV sometimes appear on layer Normal channel that uses second UV
# - Transfer UV does not work
# - Bake will throw error if there's no unwrapped object using same material (V)
# - Bake will throw error if there's object using same material with render/view turned off (V)
# - Changed color after unpack image (V)
# - Invert image can cause crash (~, Cannot fix, actual blender bug)
# - Image atlas should not be unpacked (~)
# - Bake multires without multires or with disabled multires will cause error (V)
# - Bake to layer overwrite always on despite already turning it off (V)
# - Overwrite option always showed up when baking other object (~, probably already fixed, cannot reproduce again)
# - Normal override channel possibly have issue with different uv than main uv (V)
# - Move channel modifier will cause error (V)
# - Blender 2.80 until 2.91 cannot use vertex color alpha (V)
# - Duplicate solid color with mask can cause error (V)
# - Using ucupaint on non-mesh object can cause error (V)
# - Resize image with image atlas does not work (V)
# - Baking object with no vertex will cause error (V)
# - Baked channel images sometimes dissapeared after save all
#
# KNOWN ISSUES:
# - Cycles has limit of 32 images per material, NOT per node_tree (V) Can be get around by using image atlas
# - Limit decrease to 20 images if alpha is used (V) Can be get around by using image atlas
# - Use of cineon images will cause crash (??)
# - Hemi/fake lighting layer doesn't work with bump/normal on cycles, no known workaround found (~V, hemi temp bake is already implemeted)
# - Baking object with multi materials need temporary uv manipulation, without that all uv will be baked, which is not ideals (V)

bl_info = {
    "name": "Ucupaint",
    "author": "Yusuf Umar, Agni Rakai Sahakarya",
    "version": (0, 9, 9),
    "blender": (2, 80, 0),
    "location": "Node Editor > Properties > Ucupaint",
    "description": "Special node to manage painting layers for Cycles and Eevee materials",
    "warning" : "This is alpha version, incompability to future releases might happen",
    #"wiki_url": "http://patreon.com/ucupumar",
    "category": "Node",
}

if "bpy" in locals():
    import imp
    imp.reload(image_ops)
    imp.reload(common)
    imp.reload(bake_common)
    imp.reload(mesh_ops)
    imp.reload(lib)
    imp.reload(ui)
    imp.reload(subtree)
    imp.reload(node_arrangements)
    imp.reload(node_connections)
    imp.reload(preferences)
    imp.reload(vcol_editor)
    imp.reload(transition)
    imp.reload(BakeInfo)
    imp.reload(ImageAtlas)
    imp.reload(MaskModifier)
    imp.reload(Mask)
    imp.reload(Modifier)
    imp.reload(NormalMapModifier)
    imp.reload(Blur)
    imp.reload(Layer)
    imp.reload(Bake)
    imp.reload(BakeToLayer)
    imp.reload(Root)
    #print("Reloaded multifiles")
else:
    from . import image_ops, common, bake_common, mesh_ops, lib, ui, subtree, node_arrangements, node_connections, preferences
    from . import vcol_editor, transition, BakeInfo, ImageAtlas, MaskModifier, Mask, Modifier, NormalMapModifier, Blur, Layer, Bake, BakeToLayer, Root
    #print("Imported multifiles")

import bpy 
#from bpy.app.translations import pgettext_iface as iface_

def register():
    #import bpy.utils.previews
    # Register classes
    #bpy.utils.register_module(__name__)
    image_ops.register()
    mesh_ops.register()
    preferences.register()
    lib.register()
    ui.register()
    vcol_editor.register()
    transition.register()
    BakeInfo.register()
    ImageAtlas.register()
    MaskModifier.register()
    Mask.register()
    Modifier.register()
    NormalMapModifier.register()
    Blur.register()
    Layer.register()
    Bake.register()
    BakeToLayer.register()
    Root.register()

    print('INFO: ' + bl_info['name'] + ' ' + common.get_current_version_str() + ' is registered!')

def unregister():
    # Remove classes
    #bpy.utils.unregister_module(__name__)
    image_ops.unregister()
    mesh_ops.unregister()
    preferences.unregister()
    lib.unregister()
    ui.unregister()
    vcol_editor.unregister()
    transition.unregister()
    BakeInfo.unregister()
    ImageAtlas.unregister()
    MaskModifier.unregister()
    Mask.unregister()
    Modifier.unregister()
    NormalMapModifier.unregister()
    Blur.unregister()
    Layer.unregister()
    Bake.unregister()
    BakeToLayer.unregister()
    Root.unregister()

    print('INFO: ' + bl_info['name'] + ' ' + common.get_current_version_str() + ' is unregistered!')

if __name__ == "__main__":
    register()
