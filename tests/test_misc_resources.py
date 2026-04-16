"""Tests for broad misc resource coverage endpoints."""

import pytest

from eventyay.models import GenericResource, GenericResourceList


@pytest.mark.parametrize(
    "method_name,args,expected_suffix",
    [
        ("get_activities", (), "/activities"),
        ("get_event_locations", (), "/event-locations"),
        ("get_invoices", (), "/event-invoices"),
        ("get_mails", (), "/mails"),
        ("get_message_settings", (), "/message-settings"),
        ("get_import_jobs", (), "/import-jobs"),
        ("get_video_streams", (), "/video-streams"),
        ("get_user_permissions", (), "/user-permissions"),
        ("get_ticket_fees", (), "/ticket-fees"),
        ("get_custom_placeholders", (), "/custom-placeholders"),
        ("get_groups", (), "/groups"),
        ("get_panel_permissions", (), "/panel-permissions"),
        ("get_custom_system_roles", (), "/custom-system-roles"),
        ("get_event_role_permissions", (), "/event-role-permissions"),
        ("get_email_notifications", (), "/email-notifications"),
    ],
)
def test_misc_list_methods(mock_client, mock_response, sample_generic_resource, method_name, args, expected_suffix):
    mock_client.session.get.return_value = mock_response({"data": [sample_generic_resource]})

    method = getattr(mock_client, method_name)
    result = method(*args)

    assert isinstance(result, GenericResourceList)
    request_url = mock_client.session.get.call_args.args[0]
    assert request_url.endswith(expected_suffix)


@pytest.mark.parametrize(
    "method_name,arg,expected_suffix",
    [
        ("get_activity", "1", "/activities/1"),
        ("get_event_location", "2", "/event-locations/2"),
        ("get_invoice", "3", "/event-invoices/3"),
        ("get_mail", "4", "/mails/4"),
        ("get_message_setting", "5", "/message-settings/5"),
        ("get_import_job", "6", "/import-jobs/6"),
        ("get_video_stream", "7", "/video-streams/7"),
        ("get_user_permission", "8", "/user-permissions/8"),
        ("get_ticket_fee", "9", "/ticket-fees/9"),
        ("get_custom_placeholder", "10", "/custom-placeholders/10"),
        ("get_group", "11", "/groups/11"),
        ("get_panel_permission", "12", "/panel-permissions/12"),
        ("get_custom_system_role", "13", "/custom-system-roles/13"),
        ("get_event_role_permission", "14", "/event-role-permissions/14"),
        ("get_email_notification", "15", "/email-notifications/15"),
    ],
)
def test_misc_get_methods(mock_client, mock_response, sample_generic_resource, method_name, arg, expected_suffix):
    mock_client.session.get.return_value = mock_response(sample_generic_resource)

    method = getattr(mock_client, method_name)
    result = method(arg)

    assert isinstance(result, GenericResource)
    request_url = mock_client.session.get.call_args.args[0]
    assert request_url.endswith(expected_suffix)
