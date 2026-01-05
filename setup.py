from setuptools import setup, find_packages

setup(
    name='attendance-tracker',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'attendance = attendance_tracker.main:cli',
        ],
    },
)
