################################################################################
# FlyCap2_GTKmm makefile
################################################################################
# To compile the debug verison need to overwrite CXXFLAGS variable to include -ggdb
PROJECT_ROOT=../../
OPT_INC = ${PROJECT_ROOT}/common/make/common.mk
-include ${OPT_INC}
# Handle environment variables
ifeq ($(wildcard ${OPT_INC}),) 
	CXX = g++
	ODIR = .obj/build${D}
	SDIR = .
	MKDIR = mkdir -p
	MV = mv
	CPP_FILES := $(wildcard *.cpp)
	C_FILES := $(wildcard *.c)
	STRIP = strip
endif

BASE_NAME  = FlyCap2
NAME       = ${BASE_NAME}${D}
OUTDIR     = ${PROJECT_ROOT}/bin
XMLNAME    = FlyCap2_GTKmm

GTK_INCLUDE = `pkg-config --cflags gtkmm-2.4` `pkg-config --cflags giomm-2.4` `pkg-config --cflags libglademm-2.4` `pkg-config --cflags gtkglextmm-1.2`
GTK_LIBS = `pkg-config --libs gtkmm-2.4` `pkg-config --libs giomm-2.4` `pkg-config --libs libglademm-2.4` `pkg-config --libs gthread-2.0` `pkg-config --libs gtkglextmm-1.2`

# Precompiled header.
_GCHNAME     = Precompiled.h.gch
#GCHNAME      = $(patsubst %,$(ODIR)/%,$(_GCHNAME))
GCHNAME      = $(_GCHNAME)
GCH_INCLUDES = -I../../include ${GTK_INCLUDE}
# Master deps.
INC          = -I/usr/include/flycapture ${GCH_INCLUDES}
LIBS         = -L../../lib -lflycapture${D} -lflycapturegui${D} ${GTK_LIBS}

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
_OBJ = $(CPP_FILES:.cpp=.o)
SRC  = $(_OBJ:.o=.cpp)
OBJ  = $(patsubst %,$(ODIR)/%,$(_OBJ))

# Master rule
.PHONY: all
all: ${GCHNAME} ${NAME} glade

# Precompiled header generation
${GCHNAME}: Precompiled.h
	${CXX} ${CXXFLAGS} ${GCH_INCLUDES} -Wall -c Precompiled.h

# Output binary
${NAME}: ${OBJ} glade
	${CXX} ${OBJ} -o ${NAME} ${LIBS} -export-dynamic
ifneq (${D}, d)
	${STRIP} --strip-unneeded ${NAME}
endif
	-@${MV} ${NAME} ${OUTDIR}/${NAME}

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

glade:
	@echo Copying glade files...
	cp ${XMLNAME}.glade ${OUTDIR}/${XMLNAME}.glade


