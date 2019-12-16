import setuptools


setuptools.setup(
    name="python_plsql",
    author="LatvianPython",
    version="0.1.1",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 2 - Pre-Alpha",
    ],
    python_requires=">=3.8",
    install_requires=["cx_Oracle"],
)
