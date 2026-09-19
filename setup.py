from setuptools import setup, find_packages

setup(
    name="axiom",
    version="0.1.0",
    description="Deterministic policy gate and capability registry for a local agentic AI system",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=["pyyaml"],
    python_requires=">=3.10",
)
