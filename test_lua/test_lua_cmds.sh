# build so file
INSTALL_DIR="/usr/local"
BUILD_FLAGS="-O2 -dynamiclib -undefined dynamic_lookup -I $INSTALL_DIR/include -L $INSTALL_DIR/lib"
gcc $BUILD_FLAGS -o "$INSTALL_DIR/lib/lua/$LUAV/socket/core.dylib" \
src/{auxiliar.c,buffer.c,except.c,inet.c,io.c,luasocket.c,options.c,select.c,tcp.c,timeout.c,udp.c,usocket.c}

# install luasocket
git clone -b unstable git://github.com/diegonehab/luasocket.git
cd luasocket
make macosx
sudo make install
