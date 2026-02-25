import pytest

from gsed.conversion import UnitConversion

# Feedback: it would be good to test
# routines where it is more likely to introduce bugs
# I would add a few tests for the routines you use to carry
# out the sed analysis, rather than just the conversion.
# Think about how would you check that your analysis is performed correctly.
class TestConversion:

    def test_mag_to_jy(self):
        """Tests the conversion of AB magnitude 23 to mJy."""

        # 1. Instantiate the class (required for instance methods)
        converter = UnitConversion()

        # 2. Call the method with the test value
        result = converter.magToJy(23)

        # 3. CORRECTED EXPECTED VALUE:
        # The true value is 0.0022910061178075852 mJy.

        # Use the calculated value:
        expected_mJy = 0.0022910061178075852

        assert result == pytest.approx(expected_mJy, rel=1e-6)
