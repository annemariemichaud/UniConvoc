"""Fichier d'installation uniconvoc.py."""

from cx_Freeze import setup, Executable

setup(
    name = "UniConvoc",
    version = "0.1",
    description = "scinder un ensemble de convocations",
    executables = [Executable("UniConvoc.py")],
)
