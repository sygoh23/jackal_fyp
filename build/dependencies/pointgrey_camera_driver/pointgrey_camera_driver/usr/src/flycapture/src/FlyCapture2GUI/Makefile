################################################################################
# FlyCapture2GUI_Gtkmm Makefile.
################################################################################
PROJECT_ROOT=../../
OPT_INC=${PROJECT_ROOT}/common/make/common.mk
-include ${OPT_INC}
ifeq ($(wildcard ${OPT_INC}),)
	# Client build.
	BUILD_TYPE = client
	CPP_FILES := $(wildcard *.cpp)
	ODIR = .obj
	SDIR = .
	LIBRARY_SUFFIX = so
	MAJOR_VERSION = 1
	VERSION_NUMBER = 1.2.3.4
	CXX = g++
	CXXFLAGS = -fPIC -shared
	FC2_INC  = -I/usr/include/flycapture
	GTK_INC  = $(shell pkg-config --cflags gtk+-2.0 gtkmm-2.4 libglademm-2.4)
	GTK_LIBS = $(shell pkg-config --libs   gtk+-2.0 gtkmm-2.4 libglademm-2.4)
else
	# Server build.
	BUILD_TYPE = server
	# Nothing to do. Recipe makefiles have already configured the build template
	# provided by the build server.
endif


################################################################################
# Core settings.
################################################################################
BASE_NAME   = libflycapturegui
STATICLIB   = ${BASE_NAME}${D}_static.a
LINKNAME    = ${BASE_NAME}${D}.${LIBRARY_SUFFIX}
SONAME      = ${BASE_NAME}${D}.${LIBRARY_SUFFIX}.${MAJOR_VERSION}
REALNAME    = ${BASE_NAME}${D}.${LIBRARY_SUFFIX}.${VERSION_NUMBER}
OUTDIR      = ../../lib
OUTDIR_FULL = $(shell readlink -f ${OUTDIR})


################################################################################
# Dependencies.
################################################################################
ifeq ($(OS),Linux)
LDFLAGS   = -Wl,-z,defs,-soname,${SONAME}
endif
INC       = -I../../include -I. ${GTK_INC} ${FC2_INC}
LIBS      = -L. -L../../lib                                                    \
			-Wl,-Bdynamic -lflycapture${D} ${GTK_LIBS} -lm -lpthread


################################################################################
# Target files.
################################################################################
_SRC_WANTS     := ${CPP_FILES}
_SRC           =  ${_SRC_WANTS}
_OBJ           =  $(_SRC:.cpp=.o)
SRC            =  $(_OBJ:.o=.cpp)
OBJ            =  $(patsubst %,$(ODIR)/%,$(_OBJ))


# Precompiled header settings.
_PRE_GCHNAME = Precompiled.h
_GCHNAME = ${_PRE_GCHNAME}.gch
GCHNAME = $(_GCHNAME)
GCH_INCLUDES = ${INC}


################################################################################
# Include recipes file for libraries.
################################################################################
ifeq (${BUILD_TYPE},server)
EXTRA_ALL_ARGS = glade
ifeq ($(OS),Linux)
-include ${PROJECT_ROOT}/common/make/lib_recipes.mk
else ifeq ($(OS),mac)
# Don't build for OSX.
clean:
	@echo "Nothing to clean for OSX since we don't build for it."
else
# Don't build for unknown OS type.
endif
else
# Rules for client builds.
.PHONY: all
all: ${LINKNAME}
	@echo "Done building for 'all'."
	@echo "Copying ${LINKNAME} to ${OUTDIR}"
	@cp ${LINKNAME} ${OUTDIR}
	@echo "Copying glade files..."
	@cp *.glade ../../bin
	@echo "You can find your shiny new library at ${OUTDIR_FULL}"

${LINKNAME}: ${OBJ}
	@echo "Linking final binary $@"
	${CXX} -shared -o ${LINKNAME} ${OBJ} ${LIBS}

.PHONY: prebuild
prebuild:
	@echo "Creating output directory ${ODIR}"
	mkdir -p ${ODIR}

${OBJ}: ${ODIR}/%.o : ${SDIR}/%.cpp prebuild
	@echo "Current object: $@"
	${CXX} ${CXXFLAGS} ${INC} -c $< -o $@

.PHONY: clean
clean:
	@echo "Cleaning up intermediate objects: ${OBJ}"
	rm -rf ${ODIR}
	@echo "Cleaning up output binary: ${LINKNAME}"
	rm -f ${LINKNAME}
	@echo "Done cleaning up."

endif

