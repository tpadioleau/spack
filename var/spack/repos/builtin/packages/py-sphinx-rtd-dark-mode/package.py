# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxRtdDarkMode(PythonPackage):
    """A Sphinx extension for adding a toggleable dark mode to the Read the Docs theme."""

    homepage = "https://github.com/MrDogeBro/sphinx_rtd_dark_mode"
    pypi = "sphinx-rtd-dark-mode/sphinx_rtd_dark_mode-1.2.4.tar.gz"

    license("MIT")

    version("1.3.0", sha256="0272bf3d9ef620921adc67e5634a66969419e744da84ea18830adacfdb160ea8")
    version("1.2.4", sha256="935bc1f3e62fc76eadd7d2760ac7f48bab907a97e44beda749a48a2706aeed63")

    depends_on("py-setuptools", type="build")
    depends_on("py-sphinx-rtd-theme", type=("build", "run"))
    depends_on("python@3.4:", type=("build", "run"))
