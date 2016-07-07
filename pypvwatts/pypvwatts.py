# coding: utf-8
"""
Python wrapper for NREL PVWatt version 4.
"""
from .pvwattsresult import PVWattsResult
from .pvwattserror import PVWattsError, PVWattsValidationError
import requests
from .__version__ import VERSION

import functools


# this decorator lets me use methods as both static and instance methods
class omnimethod(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        return functools.partial(self.func, instance)


class PVWatts():
    '''
    A Python wrapper for NREL PVWatts V5.0.0 API
    '''

    PVWATTS_QUERY_URL = 'http://developer.nrel.gov/api/pvwatts/v5.json'
    api_key = 'DEMO_KEY'

    def __init__(self, api_key='DEMO_KEY', proxies=None):
        PVWatts.api_key = api_key
        self.proxies = proxies

    @omnimethod
    def validate_system_capacity(self, system_capacity):
        if system_capacity is None:
            return

        if not isinstance(system_capacity, (int, float)):
            raise PVWattsValidationError(
                'system_capacity must be int or float')

        if not (0.05 <= system_capacity and system_capacity <= 500000):
            raise PVWattsValidationError(
                'system_capacity must be >= 0.05 and <= 500000')

        return system_capacity

    @omnimethod
    def validate_module_type(self, module_type):
        if module_type is None:
            return

        if not isinstance(module_type, (int)):
            raise PVWattsValidationError(
                'module_type must be int or float')

        if module_type not in (0, 1, 2):
            raise PVWattsValidationError(
                'module_type must be 0, 1 or 2')

        return module_type

    @omnimethod
    def validate_losses(self, losses):
        if losses is None:
            return

        if not isinstance(losses, (int, float)):
            raise PVWattsValidationError('losses must be int or float')

        if not (-5 <= losses and losses <= 99):
            raise PVWattsValidationError('losses must be >= -5\% and <= 99%')

        return losses

    @omnimethod
    def validate_array_type(self, array_type):
        if array_type is None:
            return

        if not isinstance(array_type, (int)):
            raise PVWattsValidationError(
                'array_type must be int or float')

        if array_type not in (0, 1, 2, 3, 4):
            raise PVWattsValidationError(
                'array_type must be 0, 1, 2, 3 or 4')

        return array_type

    @omnimethod
    def validate_tilt(self, tilt):
        if tilt is None:
            return

        if not isinstance(tilt, (int, float)):
            raise PVWattsValidationError('tilt must be int or float')

        if not (0 <= tilt and tilt <= 90):
            raise PVWattsValidationError('tilt must be >= 0 and <= 90')

        return tilt

    @omnimethod
    def validate_azimuth(self, azimuth):
        if azimuth is None:
            return

        if not isinstance(azimuth, (int, float)):
            raise PVWattsValidationError('azimuth must be int or float')

        if not (0 <= azimuth and azimuth <= 360):
            raise PVWattsValidationError('azimuth must be >= 0 and <= 360')

        return azimuth

    @omnimethod
    def validate_lat(self, lat):
        if lat is None:
            return

        if not isinstance(lat, (int, float)):
            raise PVWattsValidationError('lat must be int or float')

        if not (-90 <= lat and lat <= 90):
            raise PVWattsValidationError('lat must be >= -90 and <= 90')

        return lat

    @omnimethod
    def validate_lon(self, lon):
        if lon is None:
            return

        if not isinstance(lon, (int, float)):
            raise PVWattsValidationError('lon must be int or float')

        if not (-180 <= lon and lon <= 180):
            raise PVWattsValidationError('lon must be >= -180 and <= 180')

        return lon

    @omnimethod
    def validate_dataset(self, dataset):
        if dataset is None:
            return

        if not isinstance(dataset, (str)):
            raise PVWattsValidationError('dataset must be str')

        if dataset not in ('tmy2', 'tmy3', 'intl'):
            raise PVWattsValidationError(
                'dataset must be \'tmy2\', \'tmy3\' or \'intl\'')

        return dataset

    @omnimethod
    def validate_radius(self, radius):
        if radius is None:
            return

        if not isinstance(radius, (int, float)):
            raise PVWattsValidationError('radius must be int or float')

        if not (0 <= radius):
            raise PVWattsValidationError('radius must be >= 0')

        return radius

    @omnimethod
    def validate_timeframe(self, timeframe):
        if timeframe is None:
            return

        if not isinstance(timeframe, (str)):
            raise PVWattsValidationError(
                'timeframe must be str')

        if timeframe not in ('hourly', 'monthly'):
            raise PVWattsValidationError(
                'dataset must be \'hourly\' or \'monthly\'')

        return timeframe

    @omnimethod
    def validate_dc_ac_ratio(self, dc_ac_ratio):
        if dc_ac_ratio is None:
            return

        if not isinstance(dc_ac_ratio, (int, float)):
            raise PVWattsValidationError(
                'dc_ac_ratio must be int or float')

        if not (0 < dc_ac_ratio):
            raise PVWattsValidationError(
                'dc_ac_ratio must be positive')

        return dc_ac_ratio

    @omnimethod
    def validate_gcr(self, gcr):
        if gcr is None:
            return

        if not isinstance(gcr, (int, float)):
            raise PVWattsValidationError('gcr must be int or float')

        if not (0 <= gcr and gcr <= 3):
            raise PVWattsValidationError('gcr must be >= 0 and <= 3')

        return gcr

    @omnimethod
    def validate_inv_eff(self, inv_eff):
        if inv_eff is None:
            return

        if not isinstance(inv_eff, (int, float)):
            raise PVWattsValidationError('inv_eff must be int or float')

        if not (90 <= inv_eff and inv_eff <= 99.5):
            raise PVWattsValidationError('inv_eff must be >= 90 and <= 99.5')

        return inv_eff

    @property
    def version(self):
        return VERSION

    @omnimethod
    def get_data(self, params={}):
        """
        Make the request and return the deserialided JSON from the response

        :param params: Dictionary mapping (string) query parameters to values
        :type params: dict
        :return: JSON object with the data fetched from that URL as a
                 JSON-format object.
        :rtype: (dict or array)

        """
        if self and hasattr(self, 'proxies') and self.proxies is not None:
            response = requests.request('GET',
                                        url=PVWatts.PVWATTS_QUERY_URL,
                                        params=params,
                                        headers={'User-Agent': ''.join(
                                                 ['pypvwatts/', VERSION,
                                                  ' (Python)'])},
                                        proxies=self.proxies)
        else:
            response = requests.request('GET',
                                        url=PVWatts.PVWATTS_QUERY_URL,
                                        params=params,
                                        headers={'User-Agent': ''.join(
                                                 ['pypvwatts/', VERSION,
                                                  ' (Python)'])})

        if response.status_code == 403:
            raise PVWattsError("Forbidden, 403")
        return response.json()

    @omnimethod
    def request(self, format=None, system_capacity=None, module_type=0,
                losses=12, array_type=1, tilt=None, azimuth=None,
                address=None, lat=None, lon=None, file_id=None, dataset='tmy3',
                radius=0, timeframe='monthly', dc_ac_ratio=None, gcr=None,
                inv_eff=None, callback=None):

        params = {
            'format': format,
            'system_capacity':
            PVWatts.validate_system_capacity(system_capacity),
            'module_type': PVWatts.validate_module_type(module_type),
            'losses': PVWatts.validate_losses(losses),
            'array_type': PVWatts.validate_array_type(array_type),
            'tilt': PVWatts.validate_tilt(tilt),
            'azimuth': PVWatts.validate_azimuth(azimuth),
            'address': address,
            'lat': PVWatts.validate_lat(lat),
            'lon': PVWatts.validate_lon(lon),
            'file_id': file_id,
            'dataset': PVWatts.validate_dataset(dataset),
            'radius': PVWatts.validate_radius(radius),
            'timeframe': PVWatts.validate_timeframe(timeframe),
            'dc_ac_ratio': PVWatts.validate_dc_ac_ratio(dc_ac_ratio),
            'gcr': PVWatts.validate_gcr(gcr),
            'inv_eff': PVWatts.validate_inv_eff(inv_eff),
            'callback': callback
        }

        params['api_key'] = PVWatts.api_key

        if self is not None:
            return PVWattsResult(self.get_data(params=params))
        return PVWattsResult(PVWatts.get_data(params=params))
