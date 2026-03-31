import pytest
import os
import logging
import importlib
import config


def test_config_values(mocker):
    # Mock environment variables
    mocker.patch.dict(
        os.environ,
        {
            "GOOGLE_CLOUD_PROJECT": "test-project",
            "GOOGLE_CLOUD_LOCATION": "test-location",
        },
    )

    # Reload the config module to reflect mocked environment
    importlib.reload(config)
    from config import GCPConfig

    assert GCPConfig.PROJECT_ID == "test-project"
    assert GCPConfig.LOCATION == "test-location"


def test_config_fallback(mocker):
    # Clear environment variables
    mocker.patch.dict(os.environ, clear=True)

    importlib.reload(config)
    from config import GCPConfig

    # Assuming some reasonable defaults or fallback mechanism
    assert GCPConfig.PROJECT_ID == "rnd-geocoding-1538682427772"
    assert GCPConfig.LOCATION == "us-central1"


def test_setup_logging(mocker):
    from config import GCPConfig

    logger = GCPConfig.setup_logging()

    assert isinstance(logger, logging.Logger)
    assert logger.name == "InfiniteLoop"
