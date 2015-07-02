import os, sys
postcards_home = '/home/postcards/digital-postcards'
sys.path.insert(0, postcards_home)

activate_this = os.path.join(postcards_home, 'bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

from digitalpostcards.app import app as application