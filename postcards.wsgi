import os, sys
# define our home dir
postcards_home = '/home/postcards'
# add the app dir to the path
sys.path.insert(0, os.path.join(postcards_home, '/digital-postcards'))
# activate the virtual environement
activate_this = os.path.join(postcards_home, 'virtualenv/bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))
# import the app
from digitalpostcards.app import app as application