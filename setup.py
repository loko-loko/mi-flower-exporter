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
    install_requires=["loguru", "pyyaml", "prometheus_client", "btlewrap", "miflora"],
    entry_points={
        "console_scripts": [
            "mi-flower-exporter=mi_flower_exporter.__main__:main",
        ]
    },
)
