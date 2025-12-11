#
# Copyright (c) 2023, Takahiro Miki. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#
"""
可视化生成的 terrain mesh 文件
使用方法:
    python examples/visualize_mesh.py --mesh_path results/generated_terrain/mesh_0/mesh.obj
    python examples/visualize_mesh.py --mesh_dir results/generated_terrain/mesh_0
"""
import os
import argparse
import trimesh
import open3d as o3d
from terrain_generator.utils.mesh_utils import visualize_mesh


def visualize_mesh_file(mesh_path: str):
    """加载并可视化单个 mesh 文件"""
    if not os.path.exists(mesh_path):
        raise FileNotFoundError(f"Mesh file not found: {mesh_path}")
    
    print(f"Loading mesh from: {mesh_path}")
    mesh = trimesh.load(mesh_path)
    print(f"Mesh loaded: {len(mesh.vertices)} vertices, {len(mesh.faces)} faces")
    
    # 使用 Open3D 可视化
    visualize_mesh(mesh)


def visualize_mesh_directory(mesh_dir: str):
    """可视化目录中的 mesh 文件"""
    if not os.path.exists(mesh_dir):
        raise FileNotFoundError(f"Directory not found: {mesh_dir}")
    
    # 查找常见的 mesh 文件名
    mesh_files = [
        os.path.join(mesh_dir, "mesh.obj"),
        os.path.join(mesh_dir, "terrain_mesh.obj"),
        os.path.join(mesh_dir, "overhanging_mesh.obj"),
        os.path.join(mesh_dir, "mesh_terrain.obj"),
    ]
    
    meshes_to_show = []
    for mesh_file in mesh_files:
        if os.path.exists(mesh_file):
            print(f"Found mesh: {mesh_file}")
            mesh = trimesh.load(mesh_file)
            meshes_to_show.append(mesh)
    
    if not meshes_to_show:
        # 查找所有 .obj 文件
        obj_files = [f for f in os.listdir(mesh_dir) if f.endswith('.obj')]
        if obj_files:
            mesh_file = os.path.join(mesh_dir, obj_files[0])
            print(f"Loading first .obj file found: {mesh_file}")
            mesh = trimesh.load(mesh_file)
            meshes_to_show.append(mesh)
        else:
            raise FileNotFoundError(f"No mesh files found in: {mesh_dir}")
    
    # 合并所有 mesh（如果有多个）
    if len(meshes_to_show) == 1:
        visualize_mesh(meshes_to_show[0])
    else:
        # 合并多个 mesh 并可视化
        combined_mesh = trimesh.util.concatenate(meshes_to_show)
        print(f"Combined mesh: {len(combined_mesh.vertices)} vertices, {len(combined_mesh.faces)} faces")
        visualize_mesh(combined_mesh)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="可视化生成的 terrain mesh")
    parser.add_argument(
        "--mesh_path",
        type=str,
        default=None,
        help="单个 mesh 文件的路径 (例如: results/generated_terrain/mesh_0/mesh.obj)"
    )
    parser.add_argument(
        "--mesh_dir",
        type=str,
        default=None,
        help="包含 mesh 文件的目录 (例如: results/generated_terrain/mesh_0)"
    )
    args = parser.parse_args()
    
    if args.mesh_path:
        visualize_mesh_file(args.mesh_path)
    elif args.mesh_dir:
        visualize_mesh_directory(args.mesh_dir)
    else:
        # 默认尝试查找最近生成的文件
        default_dirs = [
            "results/generated_terrain",
            "results/mountains",
            "results/primitive_separated",
        ]
        
        found = False
        for base_dir in default_dirs:
            if os.path.exists(base_dir):
                # 查找最新的子目录
                subdirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
                if subdirs:
                    latest_dir = max(subdirs, key=lambda x: os.path.getmtime(os.path.join(base_dir, x)))
                    mesh_dir = os.path.join(base_dir, latest_dir)
                    print(f"Auto-detected mesh directory: {mesh_dir}")
                    visualize_mesh_directory(mesh_dir)
                    found = True
                    break
        
        if not found:
            print("错误: 请指定 --mesh_path 或 --mesh_dir 参数")
            print("示例:")
            print("  python examples/visualize_mesh.py --mesh_path results/generated_terrain/mesh_0/mesh.obj")
            print("  python examples/visualize_mesh.py --mesh_dir results/generated_terrain/mesh_0")

