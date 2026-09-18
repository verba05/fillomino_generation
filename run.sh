xhost +local:docker
docker build -t fillomino .
docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix fillomino > /dev/null
