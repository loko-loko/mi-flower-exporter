from setuptools import setup

setup(
    name="mi-flower-exporter",
    version="1.0.0",
    description="Exports to Prometheus Xiaomi Flower metrics",
    url="https://github.com/loko-loko/mi-flower-exporter.git",
    author="loko-loko",
    author_email="loko-loko@github.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["mi_flower_exporter"],
    include_package_data=True,
    install_requires=[
        "btlewrap==0.0.10",
        "bluepy==1.3.0",
        "loguru==0.5.0",
        "miflora==0.6",
        "prometheus-client==0.7.1",
        "PyYAML==5.4"
    ],
    entry_points={
        "console_scripts": [
            "mi-flower-exporter=mi_flower_exporter.__main__:main",
        ]
    },
)
