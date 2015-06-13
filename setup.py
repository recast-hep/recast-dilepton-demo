from setuptools import setup, find_packages

setup(
  name = 'recast-dilepton-demo',
  version = '0.0.1',
  description = 'recast-dilepton-demo',
  url = '',
  author = 'Lukas Heinrich',
  author_email = 'lukas.heinrich@cern.ch',
  packages = find_packages(),
  include_package_data = True,
  install_requires = [
    'Flask',
    'adage',
    'click',
    'pyyaml',
  ],
  entry_points = {
      'console_scripts': ['recastworkflow-dilepton=recastdilepton.dileptoncli:dileptoncli'],
  },
  dependency_links = [
  ]
)
