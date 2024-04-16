
# Blender 4.1

import os
import sys

import bpy
import bmesh
import mathutils

def create_sphere(subdivisions=3, radius=2, location=mathutils.Vector((0,0,0))):
    # Make empty BMesh.
    bm = bmesh.new()
    # Populate bmesh with shape.
    matrix=mathutils.Matrix.Identity(4)
    calc_uvs=False
    bmesh.ops.create_icosphere(bm, subdivisions=subdivisions, radius=radius, matrix=matrix, calc_uvs=calc_uvs)
    # Transform.
    bmesh.ops.translate(
        bm,
        verts=bm.verts,
        vec=location)
    # Write the bmesh into a new mesh.
    me = bpy.data.meshes.new("Mesh")
    bm.to_mesh(me)
    bm.free()
    # Add the mesh to the scene.
    obj = bpy.data.objects.new("Object", me)
    bpy.context.collection.objects.link(obj)
    return obj

if __name__ == "__main__":

    n_mb_user = sys.argv[2] # TODO: input check
    n_mb = 4 #TODO: specify by user.

    # Create spheres.
    subdivisions=7 # 4MB mesh
    radius=2
    n_spheres = int(n_mb/4)+1
    for i in range(1):
        location=mathutils.noise.random_vector(size=3)*100
        sphere = create_sphere(subdivisions, radius, location)
    print("Created mesh!")

    # Select spheres.
    item='MESH'
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type=item)

    # Export as STL.
    export_dir=os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    export_path=os.path.join(export_dir, "out.stl")
    matrix=mathutils.Matrix.Identity(4)
    print("Exporting to:", export_path)
    bpy.ops.export_mesh.stl(
        filepath=export_path, 
        check_existing=True, 
        filter_glob='*.stl', 
        use_selection=False, 
        global_scale=1.0, 
        use_scene_unit=False, 
        ascii=False, 
        use_mesh_modifiers=True, 
        batch_mode='OFF', 
        global_space=matrix, 
        axis_forward='Y', 
        axis_up='Z')
