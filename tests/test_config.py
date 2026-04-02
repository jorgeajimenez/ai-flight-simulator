import pytest
import os
import logging
from config import GCPConfig, logger

def test_config_initialization():
    assert hasattr(GCPConfig, "PROJECT_ID")
    assert hasattr(GCPConfig, "LOCATION")
    assert isinstance(logger, logging.Logger)