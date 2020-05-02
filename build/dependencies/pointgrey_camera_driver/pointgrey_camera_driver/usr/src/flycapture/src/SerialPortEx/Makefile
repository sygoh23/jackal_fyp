################################################################################
# SerialPortEx Makefile
################################################################################
# To compile the debug verison need to overwrite CXXFLAGS variable to include -ggdb
PROJECT_ROOT=../../
OPT_INC = ${PROJECT_ROOT}/common/make/common.mk
-include ${OPT_INC}
# Handle environment variables
ifeq ($(wildcard ${OPT_INC}),)
	CXX   = g++
	ODIR  = .obj/build${D}
	SDIR  = .
	MKDIR = mkdir -p
	MV    = mv
endif

BASE_NAME    = SerialPortEx
NAME         = ${BASE_NAME}${D}
OUTDIR       = ${PROJECT_ROOT}/bin
XMLNAME      = SerialPortEx
_GCHNAME     = Precompiled.h.gch
GCHNAME      = $(patsubst %,$(ODIR)/%,$(_GCHNAME))
GCH_INCLUDES = `pkg-config --cflags gtkmm-2.4`                                 \
			   `pkg-config --cflags libglademm-2.4`                            \
			   `pkg-config --cflags giomm-2.4`
INC          = -I../../include -I/usr/include/flycapture ${GCH_INCLUDES}
LIBS         = -L../../lib -lflycapture${D} ${FC2_DEPS} -lflycapturegui${D}    \
			   -lpthread `pkg-config --libs gthread-2.0`                       \
			   `pkg-config --libs giomm-2.4` `pkg-config gtkmm-2.4 --libs`     \
			   `pkg-config libglademm-2.4 --libs` ${FC2_DEPS}

UNAME=$(shell uname)
ifeq ($(UNAME),Darwin)
	# Apple Mac OS
	LIBS += -Wl,-rpath,../../lib
else ifeq ($(UNAME),Linux)
	# Linux
	LIBS += -Wl,-rpath-link=../../lib
else
	# Unsupported
endif

# Objects to link and corresponding source files
_OBJ = main.o SerialPortWindow.o
SRC  = $(_OBJ:.o=.cpp)
OBJ  = $(patsubst %,$(ODIR)/%,$(_OBJ))

# Master rule
.PHONY: all
all: ${GCHNAME} ${NAME} glade

# Precompiled header
${GCHNAME}: Precompiled.h
	${CXX} ${CXXFLAGS} ${GCH_INCLUDES} -Wall -c Precompiled.h

# Output binary
${NAME}: ${OBJ}
	${CXX} ${OBJ} -o ${NAME} ${LIBS}
	-@${MV} ${NAME} ${OUTDIR}/${NAME}

# Glademm Files
glade:
	cp ${XMLNAME}.glade ${OUTDIR}/${XMLNAME}.glade

# Intermediate object files
${OBJ}: ${ODIR}/%.o : ${SDIR}/%.cpp
	@${MKDIR} ${ODIR}
	${CXX} ${CXXFLAGS} ${LINUX_DEFINES} ${INC} -Wall -c $< -o $@

# Cleanup intermediate objects
.PHONY: clean_obj
clean_obj:
	rm -f ${OBJ}
	@echo "obj cleaned up!"

# Cleanup everything
.PHONY: clean
clean: clean_obj
	rm -f ${OUTDIR}/${NAME} ${OBJ}
	@echo "all cleaned up!"

