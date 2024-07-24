"""
Utils and example of how to generate desdf for localization
"""

import os

import cv2
import numpy as np
import tqdm

from utils.utils import ray_cast


def raycast_desdf(occ, orn_slice=36, max_dist=10, original_resolution=0.01, resolution=0.1):
    """
    Get desdf from occupancy grid through brute force raycast
    Input:
        occ: the map as occupancy
        orn_slice: number of equiangular orientations
        max_dist: maximum raycast distance, [m]
        original_resolution: the resolution of occ input [m/pixel]
        resolution: output resolution of the desdf [m/pixel]
    Output:
        desdf: the directional esdf of the occ input in meter
    """
    # assume occ resolution is 0.01
    ratio = resolution / original_resolution
    desdf = np.zeros(list((np.array(occ.shape) // ratio).astype(int)) + [orn_slice])
    # iterate through orientations
    for o in tqdm.tqdm(range(orn_slice)):
        theta = o / orn_slice * np.pi * 2
        # iterate through all pixels
        for row in tqdm.tqdm(range(desdf.shape[0])):
            for col in range(desdf.shape[1]):
                pos = np.array([row, col]) * ratio
                desdf[row, col, o] = ray_cast(occ, pos, theta, max_dist / original_resolution)

    return desdf * original_resolution


if __name__ == "__main__":
    from argparse import ArgumentParser

    arg_parser = ArgumentParser(description="Generate DESDF (precomputed raycasts) for your map")
    arg_parser.add_argument("--scene_name", type=str, required=True, help="Name of the scene. Required.")
    arg_parser.add_argument("--data_dir", type=str, default="./data", help="Directory to save the DESDF. Default is ./data.")
    arg_parser.add_argument("--map_path", type=str, default="./data/map.png")
    arg_parser.add_argument("--yaw_resolution", type=int, default=36, help="Discretization of yaw. Default is 36 discrete orientations.")
    arg_parser.add_argument("--max_dist", type=int, default=10, help="Maximum distance to raycast. Default is 10 meters.")
    arg_parser.add_argument("--map_scale", type=float, default=0.01, help="Resolution of the map in meters per pixel. Default is 0.01.")
    arg_parser.add_argument("--desdf_scale", type=float, default=0.1, help="Resolution of the DESDF in meters per pixel. Default is 0.1.")

    args = arg_parser.parse_args()
    scene_name = args.scene_name
    data_dir = args.data_dir
    map_path = args.map_path
    yaw_resolution = args.yaw_resolution
    map_scale = args.map_scale
    desdf_scale = args.desdf_scale

    if desdf_scale != 0.1:
        # TODO: add DESDF scale in file name to support multiple scales
        NotImplementedError("Only desdf_scale=0.1 (default) is supported for now.")

    # read occupancy grid map
    # TODO: apply thresholding or raise error if values are not binary
    occ = cv2.imread(map_path)[:, :, 0]
    desdf = {}
    # ray cast desdf
    desdf["desdf"] = raycast_desdf(occ, orn_slice=yaw_resolution, max_dist=15, original_resolution=map_scale, resolution=desdf_scale)
    # save desdf
    scene_dir = os.path.join(data_dir, scene_name)
    if not os.path.exists(scene_dir):
        os.mkdir(scene_dir)
    save_path = os.path.join(scene_dir, "desdf.npy")
    np.save(save_path, desdf)
