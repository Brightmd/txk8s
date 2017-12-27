"""
Tests for osteoblaster's twisted kubernetes module.
"""
import pytest

from kubernetes import client

from mock import Mock, mock_open, patch

from twisted.python import log

from txk8s import lib


def test_initClient(txclient):
    """
    Do I initialize with the correct attributes?
    """
    for attr in ("client", "_apiClient", "coreV1"):
        assert getattr(txclient, attr)


def test_initClientInCluster(txclientInCluster):
    """
    Do I initialize with the correct attributes?
    """
    for attr in ("client", "_apiClient", "coreV1"):
        assert getattr(txclientInCluster, attr)


def test_getAttr(txclient):
    """
    Do I get attributes from the k8s python api client?
    """
    expected = "<class 'kubernetes.client.models.v1_namespace.V1Namespace'>"
    assert str(txclient.__getattr__("V1Namespace")) == expected


@pytest.inlineCallbacks
def test_clientCallSuccess(kubeConfig):
    """
    Check that the `call` method does the following when successful:
    - adds callback to the kwargs passed to the apiMethod
    - calls the apiMethod it is passed
    - does not call the errback handler when successful
    - returns a deferred
    """
    def fakeReadNamespaceSecret(callback):
        callback('happy')
        return

    pApiMethod = patch.object(client,
        'CoreV1Api',
        return_value=Mock(
            read_namespaced_secret=fakeReadNamespaceSecret,
        ),
        autospec=True,
    )
    pErr = patch.object(log, 'err', autospec=True)

    with pErr as mErr, pApiMethod as mApiMethod:
        txclient = lib.TxKubernetesClient()
        res = yield txclient.call(txclient.coreV1.read_namespaced_secret)
        assert mApiMethod.call_count == 1
        assert 'happy' == res
        assert mErr.call_count == 0


@pytest.inlineCallbacks
def test_clientCallError(kubeConfig):
    """
    Check that the `call` method does the following when unsuccessful:
    - when the timeout is triggered the errback is triggered which logs the message about the failure
    """
    pApiMethod = patch.object(client,
        'CoreV1Api',
        return_value=Mock(
            read_namespaced_secret=Mock(),
        ),
        autospec=True,
    )
    pErr = patch.object(log, 'err', autospec=True)
    pTimeout = patch.object(lib, 'TIMEOUT', 0)

    with pErr as mErr, pApiMethod, pTimeout:
        txclient = lib.TxKubernetesClient()
        d = txclient.call(txclient.coreV1.read_namespaced_secret)
        def _check(fail):
            return
        d.addErrback(_check)
        yield d
        assert mErr.call_count == 1


@pytest.inlineCallbacks
def test_createPVC(kubeConfig):
    """
    Do I create a Persistent Volume Claim kubernetes resource in a namespace?
    """
    meta = 'happy'
    spec = 'days'
    namespace = 'grn-se-com'
    pCall = patch.object(lib.TxKubernetesClient, 'call')
    pPVC = patch.object(client, 'V1PersistentVolumeClaim')
    pApiMethod = patch.object(client,'CoreV1Api')
    with pPVC as mPVC, pApiMethod, pCall as mCall:
        yield lib.createPVC('a', meta, spec, namespace)
        mPVC.assert_called_once_with(api_version='v1', kind='PersistentVolumeClaim', metadata=meta, spec=spec)
        mCall.assert_called_once()


@pytest.inlineCallbacks
def test_createStorageClass(kubeConfig):
    """
    Do I create a Storage Class kubernetes resource?
    """
    meta = 'happy'
    provisioner = 'aws-efs'
    pCall = patch.object(lib.TxKubernetesClient, 'call')
    pStorage = patch.object(client, 'V1beta1StorageClass')
    pApiMethod = patch.object(client,'StorageV1beta1Api')
    with pStorage as mStorage, pApiMethod, pCall as mCall:
        yield lib.createStorageClass('a', meta, provisioner)
        mStorage.assert_called_once_with(api_version='storage.k8s.io/v1beta1', kind='StorageClass', metadata=meta, provisioner=provisioner)
        mCall.assert_called_once()


@pytest.inlineCallbacks
def test_createDeploymentFromFile(kubeConfig):
    """
    Do I create a Deployment kubernetes resource from a yaml manifest file?
    """
    pOpen = patch("__builtin__.open", mock_open(read_data="data"))
    pCall = patch.object(lib.TxKubernetesClient, 'call')
    pApiMethod = patch.object(client,
        'ExtensionsV1beta1Api',
        return_value=Mock(
            create_namespaced_deployment='a',
        ),
        autospec=True,
    )
    with pApiMethod as mApiMethod, pCall as mCall, pOpen:
        yield lib.createDeploymentFromFile('a', '/path')
        mApiMethod.assert_called_once()
        mCall.assert_called_once_with('a', body='data', namespace='default')


@pytest.inlineCallbacks
def test_createConfigMap(kubeConfig):
    """
    Do I create a configmap kubernetes resources in a namespace?
    """
    meta = 'happy'
    data = 'days'
    namespace = 'grn-se-com'
    pCall = patch.object(lib.TxKubernetesClient, 'call')
    pPVC = patch.object(client, 'V1ConfigMap', return_value='thing')
    pApiMethod = patch.object(client,
        'CoreV1Api',
        return_value=Mock(
            create_namespaced_config_map='a',
        ),
        autospec=True,
    )
    with pApiMethod, pPVC, pCall as mCall:
        yield lib.createConfigMap(meta, data, namespace)
        mCall.assert_called_once_with('a', 'grn-se-com', 'thing')


@pytest.inlineCallbacks
def test_createService(kubeConfig):
    """
    Do I create a namespaced Service kubernetes resource from a yaml manifest file?
    """
    namespace = 'grn-se-com'
    fileData = 'data'
    pOpen = patch("__builtin__.open", mock_open(read_data=fileData))
    pCall = patch.object(lib.TxKubernetesClient, 'call')
    pApiMethod = patch.object(client,
        'CoreV1Api',
        return_value=Mock(
            create_namespaced_service='a',
        ),
        autospec=True,
    )
    with pApiMethod as mApiMethod, pCall as mCall, pOpen:
        yield lib.createService('/path', namespace)
        mApiMethod.assert_called_once()
        mCall.assert_called_once_with('a', namespace, fileData)


@pytest.inlineCallbacks
def test_createServiceAccount(kubeConfig):
    """
    Do I create a Service Account kubernetes resource from a yaml manifest file?
    """
    namespace = 'grn-se-com'
    fileData = 'data'
    pOpen = patch("__builtin__.open", mock_open(read_data=fileData))
    pCall = patch.object(lib.TxKubernetesClient, 'call')
    pApiMethod = patch.object(client,
        'CoreV1Api',
        return_value=Mock(
            create_namespaced_service_account='a',
        ),
        autospec=True,
    )
    with pApiMethod as mApiMethod, pCall as mCall, pOpen:
        yield lib.createServiceAccount('a', '/path', namespace)
        mApiMethod.assert_called_once()
        mCall.assert_called_once_with('a', namespace, fileData)


@pytest.inlineCallbacks
def test_createClusterRole(kubeConfig):
    """
    Do I create a Cluster Role kubernetes resource from a yaml manifest file?
    """
    fileData = 'data'
    pOpen = patch("__builtin__.open", mock_open(read_data=fileData))
    pCall = patch.object(lib.TxKubernetesClient, 'call')
    pApiMethod = patch.object(client,
        'RbacAuthorizationV1beta1Api',
        return_value=Mock(
            create_cluster_role='a',
        ),
        autospec=True,
    )
    with pApiMethod as mApiMethod, pCall as mCall, pOpen:
        yield lib.createClusterRole('a', '/path')
        mApiMethod.assert_called_once()
        mCall.assert_called_once_with('a', fileData)


@pytest.inlineCallbacks
def test_createClusterRoleBind(kubeConfig):
    """
    Do I create a Cluster Role Binding kubernetes resource from a yaml manifest file?
    """
    fileData = 'data'
    pOpen = patch("__builtin__.open", mock_open(read_data=fileData))
    pCall = patch.object(lib.TxKubernetesClient, 'call')
    pApiMethod = patch.object(client,
        'RbacAuthorizationV1beta1Api',
        return_value=Mock(
            create_cluster_role_binding='a',
        ),
        autospec=True,
    )
    with pApiMethod as mApiMethod, pCall as mCall, pOpen:
        yield lib.createClusterRoleBind('a', '/path')
        mApiMethod.assert_called_once()
        mCall.assert_called_once_with('a', fileData)


@pytest.inlineCallbacks
def test_createIngress(kubeConfig):
    """
    Do I create a Ingress kubernetes resource from a yaml manifest file?
    """
    namespace = 'g-se-com'
    fileData = 'data'
    pOpen = patch("__builtin__.open", mock_open(read_data=fileData))
    pCall = patch.object(lib.TxKubernetesClient, 'call')
    pApiMethod = patch.object(client,
        'ExtensionsV1beta1Api',
        return_value=Mock(
            create_namespaced_ingress='a',
        ),
        autospec=True,
    )
    with pApiMethod as mApiMethod, pCall as mCall, pOpen:
        yield lib.createIngress('a', '/path', namespace)
        mApiMethod.assert_called_once()
        mCall.assert_called_once_with('a', namespace, fileData)


def test_createEnvVar(kubeConfig):
    """
    Do I create a environment variable kubernetes resource that references
    a value in a configmap?
    """
    actual = str(lib.createEnvVar('fun!', 'cmName', 'cmKey'))
    assert "'key': 'cmKey'" in actual
    assert "'name': 'cmName'" in actual
    assert "'name': 'fun!'" in actual
