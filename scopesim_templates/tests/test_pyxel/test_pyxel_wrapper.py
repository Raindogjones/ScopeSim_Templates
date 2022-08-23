import pytest

from pyxel.detectors import Detector, Environment
from scopesim import Source

from scopesim_templates import pyxel_wrapper


class TestPyxelWrapperWorks:
    @pytest.mark.parametrize("function_name", ["scopesim_templates.calibration.calibration.empty_sky",
                                               "calibration.calibration.empty_sky",
                                               "empty_sky"])
    def test_works_for_all_combinations_of_empty_sky(self, function_name):
        det = Detector(Environment())
        pyxel_wrapper(det, function_name)
        assert isinstance(det.source3d, Source)
        assert len(det.source3d.spectra) == 1

    def test_elliptical_function_works(self):
        det = Detector(Environment())
        pyxel_wrapper(det, function_name="elliptical", r_eff=2., pixel_scale=0.1, filter_name="J", amplitude=10)
        assert isinstance(det.source3d, Source)
        assert det.source3d.fields[0].header["NAXIS1"] == 512