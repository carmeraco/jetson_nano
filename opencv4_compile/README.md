# OpenCV 4.1.0 Compile demo on Jetson Nano

## What is this ?

This is an environment to compile OpenCV 4.1.0 using docker.
This example is tested on Jetson Nano with JetPack 4.2.

- Dockerfile              ... Dockerfile to create an image for build environment
- build_docker_image.sh   ... build script to make Docker image
- run.sh                  ... create docker container
- home/                   ... home directory mounted to /home/foo in the container
- /home/build_opencv4.sh  ... build script to make OpenCV 4.1.0

## Prerequisties

- Model: Jetson Nano
- Environment: JetPack 4.2
- Storage: at least 10GB of disk space

## Download example from github

```bash:terminal
git clone https://github.com/yamamo-to/jetson_nano.git
```

## Build Docker Image

```bash:terminal
cd jetson_nano/opencv4_compile
./build_docker_image.sh
```

## Launch Docker Container

```bash:terminal
./run.sh
```

## Run build script

Notice: The following command took three hours in my environment.

```bash:container
./build_opencv4.sh
```

You can find out binaries in the following directory:
`/opt/opencv-4.1.0`.

## Export outside container

After executing the build script `build_opencv4.sh`, the file `/home/foo/opencv-4.1.0.sfs`
is created in the container. Outside condainer, the path is
`jetson_nano/opencv4_compile/home/opencv-4.1.0.sfs`.

This is a SquashFS compressed file, and you can use this file as below:

```bash:container
sudo mkdir /opt/opencv-4.1.0
sudo mount -o loop /path/to/opencv-4.1.0.sfs /opt/opencv-4.1.0
```

And set the environment variables:

```bash:container
export PYTHONPATH=/opt/opencv-4.1.0/lib/python3.6/dist-packages:$PYTHONPATH
export LD_LIBRARY_PATH=/opt/opencv-4.1.0/lib:$LD_LIBRARY_PATH
```

Finally, install dependent packages:

```bash:container
sudo apt install libatlas3-base libhdf5-100
```
