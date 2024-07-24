# About
The Gibson Floorplan Localization Dataset is supplement to the folowing paper:
> **F<sup>3</sup>Loc : Fusion and Filtering for Floorplan Localization**<br>
> Authors: Changan Chen, [Rui Wang](https://rui2016.github.io), [Christoph Vogel](https://www.microsoft.com/en-us/research/people/chvogel), [Marc Pollefeys](https://people.inf.ethz.ch/marc.pollefeys/)<br>
> [Paper](https://arxiv.org/pdf/2403.03370.pdf) | [arXiv](https://arxiv.org/abs/2403.03370) | [Project Page](https://felix-ch.github.io/f3loc-page/)
 | [code](https://github.com/felix-ch/f3loc.git)

The data is collected in [Gibson Environment](https://github.com/StanfordVL/GibsonEnv).


# Data Organization
The three datasets gibson_f, gibson_g and gibson_t have the same folder structure (taking gibson_f as an example):
```
├── gibson_X
│   ├── split.yaml  # contains the train, valid, test split
│   ├── scene_1
│       ├── rgb
│           ├── 00000-0.png
│           ├── 00000-1.png
│           ├── 00000-2.png
│           ├── 00000-3.png
│           ├── 00001-0.png
│           ├── 00001-1.png
│           ├── 00001-2.png
│           ├── 00001-3.png
│           ├── ...
│       ├── (depth40.txt)
│       ├── (depth160.txt)
│       ├── poses.txt
│       ├── map.png
│   ├── scene_2
│   ...
```
## rgb
In gibson_f and gibson_g, the image names are &lt;chunk number&gt;-&lt;view number&gt;.png, e.g., 00003-2.png for the second view of the third chunk.

In gibson_t, the image names are simply the step number, e.g., 00228.png for the image at step 228.

## map.png
map.png is the floorplan as occupancy map. The resolution of the flooplan is 0.01m/pixel. The origin of the world coordinate system is at the center of the map, i.e., [W/2, H/2] .

## poses.txt
Each line of the poses.txt corresponds to an SE2 camera pose [x, y, yaw] in world frame. x, y are in meter and the yaw is in radians form -pi to pi.

The transform from world to map is
```
x_map = x_world / map_scale + W / 2
y_map = y_world / map_scale + H / 2
```

where, by default `map_scale=0.01`.
When using custom data, you can set it in `eval_filtering.py`. 

The poses are in the ascending order of their rgb names.

## depth
These are the ground truth floorplan depth values used for training the networks. Each line in the .txt file corresponds to the groundtruth floorplan depth values of an image, sampled from left to right. The lines are in the ascending order of their rgb names. depth40 is used for training the monocular floorplan depth estimation while depth160 is for the multi-view case.

## intrinsics
The camera intrinsics for all images are the same:
```
K = [[240,   0, 320],
     [  0, 240, 240],
     [  0,   0,   1]]
```

## DESDF
For each test scene, we precopmute the rays on a 2d grid, which we refere to as DESDF (Directional Euclidean Signed Distance Fields) where each grid point contains its euclidean distance to the nearest obstacle along every predifined directions. They are used to localize the camera with the predicted floorplan rays.
```
├── desdf
│   ├── scene_1
│       ├── desdf.npy
│   ├── scene_2
│   ...
```
The desdf has a resolution of 0.1m/pixel.
Each desdf.npy contains a dictionary of the following field.


```
desdf['l']        # int, the left offset to the corresponding map.png
desdf['t']        # int, the top offset to the corresponding map.png
desdf['desdf']    # ndarray, [H, W, 36], the actual desdf with 36 equiangular rays from 0 to 2*pi
```
The transformation from coordinate in desdf to the given map (0.01m/pixel) is
```
x_map = x_desdf * 0.1 / map_scale + l
y_map = y_desdf * 0.1 / map_scale + t
```

# Citation
If you use this data for your research, please cite our paper:
```
@inproceedings{chen2024f3loc,
  title={F $\^{3}$ Loc: Fusion and Filtering for Floorplan Localization},
  author={Chen, Changan and Wang, Rui and Vogel, Christoph and Pollefeys, Marc},
  booktitle={IEEE/CVF Conference on Computer Vision and Pattern Recognition},
  year={2024}
}
```

# License
This dataset is licensed under the CC BY-NC-SA 4.0 License.