"""Feedback:
These conversions don't involve anything complex,
so they don't necessarily have to be a separate class.
This module could be just a set of simple routines.

def mag_to_Jy(magnitude):
    return (10**(-magnitude / 2.5)) * 3631 * 1e3
"""
class UnitConversion:

    def __init__(self, magnitude=None):
        """
        A simple class to convert AB magnitudes to mJy.

        Parameters
        ----------
        magnitude : float, optional
            Magnitude of a source in the AB system.
        """
        self.magnitude = magnitude

    def magToJy(self, magnitude=None):
        """
        Convert AB magnitude to mJy.

        Parameters
        ----------
        magnitude : float, optional
            AB magnitude. If not provided, uses the stored class magnitude.

        Returns
        -------
        float
            Flux in mJy.
        """
        # Use provided magnitude or the object's stored magnitude
        if magnitude is None:
            magnitude = self.magnitude
        if magnitude is None:
            raise ValueError("No magnitude provided.")

        # AB magnitude to mJy conversion
        jy_milli = (10**(-magnitude / 2.5)) * 3631 * 1e3
        return jy_milli


#conv = UnitConversion()
# print(conv.magToJy(20.0))  Uses the stored magnitude

#print("flux is in mJy", conv.magToJy(0))
