"""
Shared fixtures for txk8s pytests.
"""
import os

from pytest import fixture

from mock import patch

from kubernetes import config

from txk8s import lib


@fixture
def kubeConfig():
    """
    Fixture for kubernetes config patch.
    """
    pInCluster = patch.object(config, 'load_incluster_config')
    pKube = patch.object(config, 'load_kube_config')
    with pInCluster, pKube:
        yield


@fixture
def txclient(kubeConfig):
    """
    Fixture to return an instance of the TxKubernetesClient
    class.
    """
    pEnv = patch.dict(os.environ, {'KUBERNETES_PORT': ''})
    with pEnv:
        return lib.TxKubernetesClient()


@fixture
def txclientInCluster(kubeConfig):
    """
    Fixture to return an instance of the TxKubernetesClient
    class.
    """
    pEnv = patch.dict(os.environ, {'KUBERNETES_PORT': 'tcp://hello'})
    with pEnv:
        return lib.TxKubernetesClient()
