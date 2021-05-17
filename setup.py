from setuptools import setup, find_packages


setup (
    name             = "cyberbox",
    version          = "1.01",
    description      = "Test",
    packages         = find_packages(),
    install_requires = ["gunicorn"],
)
