import requests
import sys
from .cities import CITY
from math import cos, radians
sys.path.append('./opensky_avt')

class ASV: 
    """Airplanes State Vector"""
    
    ASV_URL = 'https://opensky-network.org/api/states/all'
    FACTOR = 40000/360


    def __init__(self, city='moscow'):
        try:
            self.city = CITY[city]
        except KeyError:
            raise Exception("City '{}' is not in database.".format(city))
    

    def getinfo(self, rng=100):
        """Try to get the state vector in specified range.
        Args:
            rng: The region around the city (km).
        """
        self.params = { 'lamin': self.city['la'] - rng/self.FACTOR,
                        'lomin': self.city['lo'] - rng/self.FACTOR/cos(radians(self.city['la'])),
                        'lamax': self.city['la'] + rng/self.FACTOR,
                        'lomax': self.city['lo'] + rng/self.FACTOR/cos(radians(self.city['la']))}

        self.resp = requests.get(self.ASV_URL, params=self.params).json()   
   

    @property
    def count(self):
        """Return number of of aircraft."""
        try:
            self.result = len(self.resp['states'])
        except TypeError:
            self.result = 0
        return self.result


    def __repr__(self):
        return str(self.resp['states'])
