from setuptools import find_packages, setup

setup(
    name="river-levels",
    version="0.1",
    description="UK river level data analysis",
    author="Matt Beckers",
    packages=find_packages("."),
    entry_points={
        "console_scripts": [
            "download_station_data = src.stations:main",
            "download_catchment_readings = src.catchment_readings:main",
        ]
    },
)
