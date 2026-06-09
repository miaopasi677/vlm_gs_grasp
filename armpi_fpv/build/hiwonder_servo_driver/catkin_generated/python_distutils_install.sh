#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/armpi/桌面/ros/armpi_fpv/src/hiwonder_servo_driver"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/armpi/桌面/ros/armpi_fpv/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/armpi/桌面/ros/armpi_fpv/install/lib/python3/dist-packages:/home/armpi/桌面/ros/armpi_fpv/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/armpi/桌面/ros/armpi_fpv/build" \
    "/usr/bin/python3" \
    "/home/armpi/桌面/ros/armpi_fpv/src/hiwonder_servo_driver/setup.py" \
     \
    build --build-base "/home/armpi/桌面/ros/armpi_fpv/build/hiwonder_servo_driver" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/armpi/桌面/ros/armpi_fpv/install" --install-scripts="/home/armpi/桌面/ros/armpi_fpv/install/bin"
