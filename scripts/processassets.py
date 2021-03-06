import sys
import os
import argparse
import bpy
from math import pi

def main():
    argv = sys.argv
    argv = argv[argv.index("--") + 1:] # get rid of blender args

    parser = argparse.ArgumentParser(description='Process assets for DesktopHero.')
    parser.add_argument('mesh_filename', type=str, help='File to process')
    parser.add_argument('--px', type=float)
    parser.add_argument('--py', type=float)
    parser.add_argument('--pz', type=float)
    parser.add_argument('--rx', type=float)
    parser.add_argument('--ry', type=float)
    parser.add_argument('--rz', type=float)
    parser.add_argument('--sx', type=float)
    parser.add_argument('--sy', type=float)
    parser.add_argument('--sz', type=float)
    parser.add_argument('--rigid', help='Whether asset should remain rigid when bones move', action='store_true', required=False)
    parser.add_argument('--attach_to_group', type=str, help='Bone group that asset should be attached to')
    parser.add_argument('--attach_to_bone', type=str, help='Bone that asset should be attached to (only valid if rigid == true)')

    args = parser.parse_args(argv)

    bpy.ops.wm.addon_enable(module='io_three')

    # bpy.ops.import_scene.obj(filepath=args.mesh_filename)
    bpy.ops.import_mesh.stl(filepath=args.mesh_filename)
    bpy.ops.wm.save_as_mainfile(filepath="tsaved.blend")

    mesh = bpy.context.selected_objects[0]
    mesh.rotation_mode = 'YZX'

    #mesh.rotation_euler[0] = pi * 90 / 180 # rotate 90 degrees around axis to match blender to three.js. (For obj only?)
    #bpy.ops.object.transform_apply( rotation = True )

    mesh.location[0] = args.px
    mesh.location[1] = -args.pz
    mesh.location[2] = args.py
    mesh.rotation_euler[0] = pi * args.rx / 180
    mesh.rotation_euler[1] = pi * -args.rz / 180
    mesh.rotation_euler[2] = pi * args.ry / 180
    mesh.scale[0] = args.sx
    mesh.scale[1] = args.sz
    mesh.scale[2] = args.sy

    armature_name = '{} armature'.format(args.attach_to_group)
    if not armature_name in bpy.data.objects:
        print('Error: No armature found named {}.'.format(armature_name))
        sys.exit(1)

    armature = bpy.data.objects[armature_name]
    bpy.ops.object.select_all(action='DESELECT')
    armature.select = True
    bpy.context.scene.objects.active = armature

    print('Rigid: ', args.rigid)
    # if args.rigid:
    #     bpy.ops.object.mode_set(mode='EDIT')
    #     if not args.attach_to_bone in armature.data.edit_bones:
    #         print('Error: No bone found named {}.'.format(args.attach_to_bone))
    #         sys.exit(1)

    #     bone = armature.data.edit_bones[args.attach_to_bone]
    #     armature.data.edit_bones.active = bone

    #     bpy.ops.object.mode_set(mode='OBJECT')

    #     bpy.ops.object.select_all(action='DESELECT')
    #     mesh.select = True
    #     armature.select = True
    #     bpy.context.scene.objects.active = armature
    #     bpy.ops.object.parent_set(type='BONE')
    # else:
    mesh.select = True
    bpy.context.scene.objects.active = armature
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')

    if args.rigid:
        # If asset is rigid, manually assign weight 100% to the selected bone,
        # and set weights for other bones to 0.
        bpy.ops.object.select_all(action='DESELECT')
        mesh.select = True
        bpy.context.scene.objects.active = mesh
        mesh_data = mesh.data
        to_delete = []
        for group in mesh.vertex_groups:
            group.add(range(0, len(mesh_data.vertices)), 1.0, 'REPLACE')
            if group.name != args.attach_to_bone:
                to_delete.append(group.name)

        for group_name in to_delete:
            group = mesh.vertex_groups.get(group_name)
            mesh.vertex_groups.remove(group)

    # Move armature to 0, 0, 0 and clear origin.
    bpy.ops.object.select_all(action='DESELECT')
    armature.select = True
    bpy.context.scene.objects.active = armature
    bpy.ops.object.location_clear()
    bpy.ops.object.origin_clear()

    # Add modifiers for low, medium and high resolution and export for each
    bpy.ops.object.select_all(action='DESELECT')
    mesh.select = True
    bpy.context.scene.objects.active = mesh

    TARGET_NUM_VERTS = {
        'lowres': 1000,
        'medres': 2000,
        'hires': 3500
    }
    filename_base = args.mesh_filename[:-4] # strip .obj file type
    for res in ['lowres', 'medres', 'hires']:
        num_vertices = len(mesh.data.vertices)
        modifier = mesh.modifiers.new(name='decimate', type='DECIMATE')
        modifier.ratio = TARGET_NUM_VERTS[res] / num_vertices
        
        filename = "{}_{}.json".format(filename_base.replace(' ', '_'), res)
        filename_js = "{}_{}.js".format(filename_base.replace(' ', '_'), res)
        if os.path.exists(filename):
            os.remove(filename)
        if os.path.exists(filename_js):
            os.remove(filename_js)
        bpy.ops.export.three(filepath=filename, option_apply_modifiers=True, option_face_materials=False, option_bones=True, option_influences=4, option_skinning=True, option_embed_animation=False, option_round_value=3, option_uv_coords=False)
        os.rename(filename, filename_js)
        
        mesh.modifiers.remove(modifier)

    # Render image
    bpy.ops.object.select_all(action='DESELECT')
    mesh.select = True
    bpy.context.scene.objects.active = mesh

    bpy.ops.view3d.camera_to_view_selected() # Point camera at object
    img_filename = "{}.png".format(filename_base.replace(' ', '_'))
    bpy.data.scenes['Scene'].render.filepath = img_filename
    bpy.ops.render.render(write_still=True)

    #bpy.ops.wm.save_as_mainfile(filepath="saved.blend")

    return 0

if __name__ == '__main__':
    main()
