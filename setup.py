import setuptools

setuptools.setup(
    name="py-escan-walkentalk",
    version="0.0.1",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)
