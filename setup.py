from setuptools import setup, find_packages

setup(
   name='toposort',
   version="0.0.1",
   description="Topological Sort",
   url="https://github.com/vkocubinsky/toposort",
   author="Valery Kocubinsky",
   license="MIT",
   classifiers =[
       'Development Status :: 3 - Alpha'
       'Programming Language :: Python :: 3.5',
        ],
   py_modules=["toposort","test_toposort"],
)
