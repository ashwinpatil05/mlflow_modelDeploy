import logging
import posixpath

from mlflow.models import Model
from mlflow.models.flavor_backend_registry import get_flavor_backend
from mlflow.tracking.artifact_utils import _download_artifact_from_uri
from mlflow.utils.file_utils import TempDir



_logger = logging.getLogger(__name__)

def serve(model_uri, port, host, workers, no_conda=True, install_mlflow=False):
    """
    Serve a model saved with MLflow by launching a webserver on the specified host and port. For
    information about the input data formats accepted by the webserver, see the following
    documentation: https://www.mlflow.org/docs/latest/models.html#built-in-deployment-tools.
    You can make requests to ``POST /invocations`` in pandas split- or record-oriented formats.
    Example:
    .. code-block:: bash
        $ mlflow models serve -m runs:/my-run-id/model-path &
        $ curl http://127.0.0.1:5000/invocations -H 'Content-Type: application/json' -d '{
            "columns": ["a", "b", "c"],
            "data": [[1, 2, 3], [4, 5, 6]]
        }'
    """
    return _get_flavor_backend(model_uri,
                               no_conda=no_conda,
                               workers=workers,
                               install_mlflow=install_mlflow).serve(model_uri=model_uri, port=port,
                                                                    host=host)




def _get_flavor_backend(model_uri, **kwargs):
    with TempDir() as tmp:
        local_path = _download_artifact_from_uri(posixpath.join(model_uri, "MLmodel"),
                                                 output_path=tmp.path())
        model = Model.load(local_path)
    flavor_name, flavor_backend = get_flavor_backend(model, **kwargs)
    if flavor_backend is None:
        raise Exception("No suitable flavor backend was found for the model.")
    _logger.info("Selected backend for flavor '%s'", flavor_name)
    return flavor_backend