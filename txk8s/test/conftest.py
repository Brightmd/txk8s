"""
Shared fixtures for txk8s pytests.
"""
import pytest

from mock import patch

from kubernetes import config


@pytest.fixture
def kubeConfig():
    """
    Fixture for kubernetes config patch.
    """
    return patch.object(config, 'load_incluster_config')



