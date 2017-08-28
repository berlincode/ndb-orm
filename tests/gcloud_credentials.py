#!./virtualenv/bin/python3
# coding: utf-8

import google.auth.credentials

# from https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/test_utils/test_utils/system.py
class EmulatorCredentials(google.auth.credentials.Credentials):
    """A mock credential object.
    Used to avoid unnecessary token refreshing or reliance on the network
    while an emulator is running.
    """

    def __init__(self):  # pylint: disable=super-init-not-called
        self.token = b'seekrit'
        self.expiry = None

    @property
    def valid(self):
        """Would-be validity check of the credentials.
        Always is :data:`True`.
        """
        return True

    def refresh(self, unused_request):  # pylint: disable=unused-argument
        """Off-limits implementation for abstract method."""
        raise RuntimeError('Should never be refreshed.')
