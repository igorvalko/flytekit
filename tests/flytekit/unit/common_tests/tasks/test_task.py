from __future__ import absolute_import

import pytest as _pytest
import os as _os
from mock import patch as _patch, MagicMock as _MagicMock

from flytekit.configuration import TemporaryConfiguration
from flytekit.common.exceptions import user as _user_exceptions
from flytekit.common.tasks import task as _task
from flytekit.common.types import primitives
from flytekit.models import task as _task_models
from flytekit.models.core import identifier as _identifier
from flytekit.sdk.tasks import python_task, inputs, outputs
from flyteidl.admin import task_pb2 as _admin_task_pb2


@_patch("flytekit.engines.loader.get_engine")
def test_fetch_latest(mock_get_engine):
    admin_task = _task_models.Task(
        _identifier.Identifier(_identifier.ResourceType.TASK, "p1", "d1", "n1", "v1"),
        _MagicMock(),
    )
    mock_engine = _MagicMock()
    mock_engine.fetch_latest_task = _MagicMock(
        return_value=admin_task
    )
    mock_get_engine.return_value = mock_engine
    task = _task.SdkTask.fetch_latest("p1", "d1", "n1")
    assert task.id == admin_task.id


@_patch("flytekit.engines.loader.get_engine")
def test_fetch_latest_not_exist(mock_get_engine):
    mock_engine = _MagicMock()
    mock_engine.fetch_latest_task = _MagicMock(
        return_value=None
    )
    mock_get_engine.return_value = mock_engine
    with _pytest.raises(_user_exceptions.FlyteEntityNotExistException):
        _task.SdkTask.fetch_latest("p1", "d1", "n1")


def get_sample_task():
    """
    :rtype: flytekit.common.tasks.task.SdkTask
    """
    @inputs(a=primitives.Integer)
    @outputs(b=primitives.Integer)
    @python_task()
    def my_task(wf_params, a, b):
        b.set(a + 1)

    return my_task


def test_task_serialization():
    t = get_sample_task()
    with TemporaryConfiguration(
            _os.path.join(_os.path.dirname(_os.path.realpath(__file__)), '../../../common/configs/local.config'),
            internal_overrides={
                'image': 'myflyteimage:v123',
                'project': 'myflyteproject',
                'domain': 'development'
            }
    ):
        s = t.serialize()

    assert isinstance(s, _admin_task_pb2.TaskSpec)
    assert s.template.id.name == 'tests.flytekit.unit.common_tests.tasks.test_task.my_task'
    assert s.template.container.image == 'myflyteimage:v123'
