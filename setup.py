from setuptools import setup, find_packages


setup (
    name             = "cyberbox",
    version          = "1.0",
    description      = "Test",
    packages         = find_packages(),
    install_requires = ["gunicorn"],
)
