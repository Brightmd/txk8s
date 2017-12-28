# txk8s.lib module


## **createPVC**
### Description:

Creates a persistant volume claim resource using the kubernetes python client.

See python-client docs for [CoreV1Api.create_namespaced_persistent_volume_claim](https://github.com/kubernetes-incubator/client-python/blob/master/kubernetes/docs/CoreV1Api.md#create_namespaced_persistent_volume_claim) for more details.

### Example 
```python
meta = txcli.V1ObjectMeta(name='my-volume')
spec = txcli.V1PersistentVolumeClaimSpec()
# create the PersistentVolumeClaim
d = txcli.createPVC(meta, spec, 'example-ns')
```

### Parameters
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**V1ObjectMeta**](V1ObjectMeta.md) | Standard object&#39;s metadata. More info: https://git.k8s.io/community/contributors/devel/api-conventions.md#metadata | [required]
**spec** | [**V1PersistentVolumeClaimSpec**](V1PersistentVolumeClaimSpec.md) | Spec defines the desired characteristics of a volume requested by a pod author. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#persistentvolumeclaims | [required]
**namespace** | **str** | The name of the namespace the PVC is created for. | [required] 


### Return type

Returns a Twisted deferred object.

See twisted documentation for details: [**twisted.internet.defer.Deferred**](https://twistedmatrix.com/documents/16.5.0/api/twisted.internet.defer.Deferred.html)


## **createStorageClass**
### Description:

Creates a storageClass resource using the kubernetes python client.

See python-client docs for [StorageV1beta1Api.create_storage_class](https://github.com/kubernetes-incubator/client-python/blob/master/kubernetes/docs/StorageV1beta1Api.md#create_storage_class) for more details.

See Kubernetes docs for [Storage Classes](https://kubernetes.io/docs/concepts/storage/storage-classes/#provisioner) for details.

### Example 
```python
meta = txk8s.V1ObjectMeta()
# create the storageClass
d = txcli.createStorageClass(meta, 'aws-efs')
```

### Parameters
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**V1ObjectMeta**](V1ObjectMeta.md) | Standard object&#39;s metadata. More info: https://git.k8s.io/community/contributors/devel/api-conventions.md#metadata | [required]
**provisioner** | **str** | A provisioner that determines what volume plugin is used | [required]


### Return type

Returns a Twisted deferred object.

See twisted documentation for details: [**twisted.internet.defer.Deferred**](https://twistedmatrix.com/documents/16.5.0/api/twisted.internet.defer.Deferred.html)


## **createDeploymentFromFile**
### Description:

Creates a deployment resource using the kubernetes python client.

See python-client docs for [CoreV1Api.create_namespaced_persistent_volume_claim](https://github.com/kubernetes-incubator/client-python/blob/master/kubernetes/docs/CoreV1Api.md#create_namespaced_persistent_volume_claim) for more details.

### Example 
```python
meta = txcli.V1ObjectMeta(name='my-volume')
spec = txcli.V1PersistentVolumeClaimSpec()
# create the PersistentVolumeClaim
d = txcli.createPVC(meta, spec, 'example-ns')
```

### Parameters
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**filePath** | **str** | Path to the manifest file for this deployment. | [required]

**namespace** | **str** | The name of the namespace the PVC is created for. | [required] 


### Return type

Returns a Twisted deferred object.

See twisted documentation for details: [**twisted.internet.defer.Deferred**](https://twistedmatrix.com/documents/16.5.0/api/twisted.internet.defer.Deferred.html)