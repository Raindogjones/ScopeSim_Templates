import importlib

import pyxel
from pyxel.detectors import Detector

import scopesim_templates as st


def pyxel_wrapper(detector, function_name, **kwargs):
    """
    Wraps the scopesim_template functions for use with pyxel

    Parameters
    ----------
    detector : pyxel.Detector
    function_name : str

    Examples
    --------
    Example Pyxel yaml file input::

        pipeline:
        # -> photon
        photon_generation:
        - name: globular_cluster
          func: scopesim_templates.pyxel_wrapper
          enabled: true
          arguments:
            function_name: stellar.clusters.cluster
            mass: 10000
            distance: 8300
            core_radius: 2

    """
    if not isinstance(detector, Detector):
        raise ValueError(f"detector must be pyxel.Detector object: {type(detector)}")

    if "scopesim_templates." not in function_name:
        function_name = "scopesim_templates." + function_name

    mod_path, func_name = function_name.rsplit(".", 1)
    sub_module = importlib.import_module(mod_path)

    func = getattr(sub_module, func_name)
    src = func(**kwargs)
    detector.source3d = src

    return None
