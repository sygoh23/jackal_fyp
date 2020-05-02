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

echo_and_run cd "/home/ubuntu/ws/jackal_fyp/src/dependencies/unique_identifier/unique_id"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/ubuntu/ws/jackal_fyp/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/ubuntu/ws/jackal_fyp/install/lib/python2.7/dist-packages:/home/ubuntu/ws/jackal_fyp/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/ubuntu/ws/jackal_fyp/build" \
    "/usr/bin/python2" \
    "/home/ubuntu/ws/jackal_fyp/src/dependencies/unique_identifier/unique_id/setup.py" \
    build --build-base "/home/ubuntu/ws/jackal_fyp/build/dependencies/unique_identifier/unique_id" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/ubuntu/ws/jackal_fyp/install" --install-scripts="/home/ubuntu/ws/jackal_fyp/install/bin"
