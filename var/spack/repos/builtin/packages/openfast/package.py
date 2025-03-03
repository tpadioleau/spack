# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Openfast(CMakePackage):
    """Wind turbine simulation package from NREL"""

    homepage = "https://openfast.readthedocs.io/en/latest/"
    git = "https://github.com/OpenFAST/openfast.git"

    maintainers("jrood-nrel")

    license("Apache-2.0")

    version("develop", branch="dev")
    version("master", branch="main")
    version("4.0.2", tag="v4.0.2")
    version("3.5.5", tag="v3.5.5")
    version("3.5.4", tag="v3.5.4")
    version("3.5.3", tag="v3.5.3")
    version("3.4.1", tag="v3.4.1")
    version("3.4.0", tag="v3.4.0")
    version("3.3.0", tag="v3.3.0")
    version("3.2.1", tag="v3.2.1")
    version("3.2.0", tag="v3.2.0")
    version("3.1.0", tag="v3.1.0")
    version("3.0.0", tag="v3.0.0")
    version("2.6.0", tag="v2.6.0")
    version("2.5.0", tag="v2.5.0")
    version("2.4.0", tag="v2.4.0")
    version("2.3.0", tag="v2.3.0")
    version("2.2.0", tag="v2.2.0")
    version("2.1.0", tag="v2.1.0")
    version("2.0.0", tag="v2.0.0")
    version("1.0.0", tag="v1.0.0")

    with default_args(deprecated=True):
        version("4.0.1", tag="v4.0.1")
        version("4.0.0", tag="v4.0.0")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    patch("hub_seg_fault.patch", when="@2.7:3.2")

    variant("shared", default=True, description="Build shared libraries")
    variant("double-precision", default=True, description="Treat REAL as double precision")
    variant("dll-interface", default=True, description="Enable dynamic library loading interface")
    variant("cxx", default=False, description="Enable C++ bindings")
    variant("pic", default=True, description="Position independent code")
    variant("openmp", default=False, description="Enable OpenMP support")
    variant("netcdf", default=False, description="Enable NetCDF support")
    variant("rosco", default=False, description="Build ROSCO controller")
    variant("fastfarm", default=False, description="Enable FAST.Farm capabilities")
    variant("fpe-trap", default=False, description="Enable FPE trap in compiler options")

    depends_on("blas")
    depends_on("lapack")
    depends_on("mpi", when="+cxx")
    depends_on("yaml-cpp@0.6.0:0.6.3", when="+cxx")
    depends_on("hdf5+mpi+cxx+hl", when="+cxx")
    depends_on("zlib-api", when="+cxx")
    depends_on("libxml2", when="+cxx")
    depends_on("netcdf-c", when="+cxx+netcdf")
    depends_on("rosco", when="+rosco")

    conflicts("~cxx", when="+netcdf")

    def cmake_args(self):
        spec = self.spec

        options = []

        options.extend(
            [
                self.define("BUILD_DOCUMENTATION", False),
                self.define("BUILD_TESTING", False),
                self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
                self.define_from_variant("DOUBLE_PRECISION", "double-precision"),
                self.define_from_variant("USE_DLL_INTERFACE", "dll-interface"),
                self.define_from_variant("BUILD_OPENFAST_CPP_API", "cxx"),
                self.define_from_variant("BUILD_OPENFAST_CPP_DRIVER", "cxx"),
                self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
                self.define_from_variant("BUILD_FASTFARM", "fastfarm"),
                self.define_from_variant("FPE_TRAP_ENABLED", "fpe-trap"),
            ]
        )

        # Make sure we use Spack's blas/lapack:
        blas_libs = spec["lapack"].libs + spec["blas"].libs
        options.extend(
            [
                self.define("BLAS_LIBRARIES", blas_libs.joined(";")),
                self.define("LAPACK_LIBRARIES", blas_libs.joined(";")),
            ]
        )

        if "+cxx" in spec:
            options.extend(
                [
                    self.define("CMAKE_CXX_COMPILER", spec["mpi"].mpicxx),
                    self.define("CMAKE_C_COMPILER", spec["mpi"].mpicc),
                    self.define("CMAKE_Fortran_COMPILER", spec["mpi"].mpifc),
                    self.define("MPI_CXX_COMPILER", spec["mpi"].mpicxx),
                    self.define("MPI_C_COMPILER", spec["mpi"].mpicc),
                    self.define("MPI_Fortran_COMPILER", spec["mpi"].mpifc),
                    self.define("HDF5_ROOT", spec["hdf5"].prefix),
                    self.define("YAML_ROOT", spec["yaml-cpp"].prefix),
                    # The following expects that HDF5 was built with CMake.
                    # Solves issue with OpenFAST trying to link
                    # to HDF5 libraries with a "-shared" prefix
                    # that do not exist.
                    self.define("HDF5_NO_FIND_PACKAGE_CONFIG_FILE", True),
                ]
            )

            if "+netcdf" in spec:
                options.extend([self.define("NETCDF_ROOT", spec["netcdf-c"].prefix)])

        if "~shared" in spec:
            options.extend([self.define("HDF5_USE_STATIC_LIBRARIES", True)])

        if "+openmp" in spec:
            options.extend([self.define("OPENMP", True)])

        return options

    def flag_handler(self, name, flags):
        spec = self.spec
        if name in ["cflags", "cxxflags", "cppflags", "fflags"]:
            if "+openmp" in spec:
                flags.append(self.compiler.openmp_flag)
            return (None, flags, None)
        return (flags, None, None)
