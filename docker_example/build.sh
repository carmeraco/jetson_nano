#!/bin/sh

TAG=python_with_tensorflow
UBUNTU_MIRROR=jp.archive.ubuntu.com

sudo nvidia-docker build \
	--build-arg MIRROR=$UBUNTU_MIRROR \
	-t $TAG \
	.
