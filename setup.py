import setuptools

with open('README.md','r') as fh:
	long_description = file.read()


setuptools.setup(
	name = 'preprocess_victen18', #this should be unique name
	version = '0.0.1',
	author = 'Vikram Nimmakuri',
	author_email = 'vikramnimmakuri@gmail.com',
	description = 'This is pre-processing package for NLP',
	long_description = long_description,	
	long_description_content_type = 'text/markdown',
	packages = setuptools.find_packages(),
	classifiers = [
	'Programming Language :: Python :: 3',
	'License :: OSI Aproved :: MIT License',
	'Operating System :: OS Independent'],
	python_requires = '>=3.5'

	)