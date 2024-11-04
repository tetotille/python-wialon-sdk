from setuptools import setup, find_packages

setup(
  name='wialon-sdk',
  version='0.1.0',
  packages=find_packages(),
  install_requires=[
    'requests>=2.32.3'
  ],
  entry_points={
    'console_scripts': [
      'wialon-sdk=wialon_sdk.__main__:main'
    ],
  },
  author='Jorge Tillería',
  author_email='jltilleriam@gmail.com',
  description='Python SDK for Wialon API',
  long_description=open('README.md').read(),
  long_description_content_type='text/markdown',
  url='https://github.com/tetotille/wialon-sdk',
  classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: OS Independent',
  ],
  python_requires='>=3.9',
)