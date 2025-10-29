from setuptools import setup, find_packages

setup(
    name="smart_server",
    version="0.1.0",
    author="Smart Server Team",
    author_email="",
    license="MIT",
    description="Smart Server for Decision Making Analysis",
    long_description="A server component for smart decision making analysis using FastAPI",
    keywords="server, analytics, decision, fastapi",
    platforms="any",
    provides=["smart_server"],
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "httpx",
        "pydantic",
        "matplotlib",
    ],
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: FastAPI",
    ],
)
