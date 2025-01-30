from setuptools import setup, find_packages

setup(
    name='retirementTester',
    version='0.1.0',
    description='A retirement portfolio simulation tool',
    author='Jon Errasti',
    author_email='errasti13@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask>=2.0.0',
        'pandas>=1.3.0',
        'numpy>=1.21.0',
        'matplotlib>=3.4.0',
        'yfinance>=0.1.63',
        'streamlit>=0.84.0'
    ],
    entry_points={
        'console_scripts': [
            'run_simulation=scripts.run_simulation:main',
        ],
    },
)
