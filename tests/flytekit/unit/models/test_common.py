from __future__ import absolute_import

from flytekit.models import common as _common
from flytekit.models.core import execution as _execution


def test_notification_email():
    obj = _common.EmailNotification(['a', 'b', 'c'])
    assert obj.recipients_email == ['a', 'b', 'c']
    obj2 = _common.EmailNotification.from_flyte_idl(obj.to_flyte_idl())
    assert obj2 == obj


def test_notification_pagerduty():
    obj = _common.PagerDutyNotification(['a', 'b', 'c'])
    assert obj.recipients_email == ['a', 'b', 'c']
    obj2 = _common.PagerDutyNotification.from_flyte_idl(obj.to_flyte_idl())
    assert obj2 == obj


def test_notification_slack():
    obj = _common.SlackNotification(['a', 'b', 'c'])
    assert obj.recipients_email == ['a', 'b', 'c']
    obj2 = _common.SlackNotification.from_flyte_idl(obj.to_flyte_idl())
    assert obj2 == obj


def test_notification():
    phases = [_execution.WorkflowExecutionPhase.FAILED, _execution.WorkflowExecutionPhase.SUCCEEDED]
    recipients = ['a', 'b', 'c']

    obj = _common.Notification(phases, email=_common.EmailNotification(recipients))
    assert obj.phases == phases
    assert obj.email.recipients_email == recipients
    obj2 = _common.Notification.from_flyte_idl(obj.to_flyte_idl())
    assert obj == obj2
    assert obj2.phases == phases
    assert obj2.email.recipients_email == recipients

    obj = _common.Notification(phases, pager_duty=_common.PagerDutyNotification(recipients))
    assert obj.phases == phases
    assert obj.pager_duty.recipients_email == recipients
    obj2 = _common.Notification.from_flyte_idl(obj.to_flyte_idl())
    assert obj == obj2
    assert obj2.phases == phases
    assert obj2.pager_duty.recipients_email == recipients

    obj = _common.Notification(phases, slack=_common.SlackNotification(recipients))
    assert obj.phases == phases
    assert obj.slack.recipients_email == recipients
    obj2 = _common.Notification.from_flyte_idl(obj.to_flyte_idl())
    assert obj == obj2
    assert obj2.phases == phases
    assert obj2.slack.recipients_email == recipients


def test_labels():
    obj = _common.Labels({"my": "label"})
    assert obj.values == {"my": "label"}
    obj2 = _common.Labels.from_flyte_idl(obj.to_flyte_idl())
    assert obj2 == obj


def test_annotations():
    obj = _common.Annotations({"my": "annotation"})
    assert obj.values == {"my": "annotation"}
    obj2 = _common.Annotations.from_flyte_idl(obj.to_flyte_idl())
    assert obj2 == obj
