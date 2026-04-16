from ._transport import SyncTransportBase
from .models import GenericResource, GenericResourceList
from .utils import parse_jsonapi_list, parse_jsonapi_resource


class MiscResourcesMixin(SyncTransportBase):
    """Broad read/list coverage for additional Eventyay API domains."""

    def _list_generic(self, endpoint: str, page: int = 1, page_size: int = 25) -> GenericResourceList:
        params = {"page[number]": page, "page[size]": page_size}
        response_data = self._get(endpoint, params=params)
        return GenericResourceList(
            **parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    def _get_generic(self, endpoint: str) -> GenericResource:
        response_data = self._get(endpoint)
        return GenericResource(
            **parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    def get_activities(self, page: int = 1, page_size: int = 25) -> GenericResourceList:
        return self._list_generic("activities", page, page_size)

    def get_activity(self, activity_id: str) -> GenericResource:
        return self._get_generic(f"activities/{activity_id}")

    def get_event_locations(self, page: int = 1, page_size: int = 25) -> GenericResourceList:
        return self._list_generic("event-locations", page, page_size)

    def get_event_location(self, event_location_id: str) -> GenericResource:
        return self._get_generic(f"event-locations/{event_location_id}")

    def get_invoices(self, page: int = 1, page_size: int = 25) -> GenericResourceList:
        return self._list_generic("event-invoices", page, page_size)

    def get_invoice(self, invoice_id: str) -> GenericResource:
        return self._get_generic(f"event-invoices/{invoice_id}")

    def get_mails(self, page: int = 1, page_size: int = 25) -> GenericResourceList:
        return self._list_generic("mails", page, page_size)

    def get_mail(self, mail_id: str) -> GenericResource:
        return self._get_generic(f"mails/{mail_id}")

    def get_message_settings(self, page: int = 1, page_size: int = 25) -> GenericResourceList:
        return self._list_generic("message-settings", page, page_size)

    def get_message_setting(self, message_setting_id: str) -> GenericResource:
        return self._get_generic(f"message-settings/{message_setting_id}")

    def get_import_jobs(self, page: int = 1, page_size: int = 25) -> GenericResourceList:
        return self._list_generic("import-jobs", page, page_size)

    def get_import_job(self, import_job_id: str) -> GenericResource:
        return self._get_generic(f"import-jobs/{import_job_id}")

    def get_video_streams(self, page: int = 1, page_size: int = 25) -> GenericResourceList:
        return self._list_generic("video-streams", page, page_size)

    def get_video_stream(self, video_stream_id: str) -> GenericResource:
        return self._get_generic(f"video-streams/{video_stream_id}")

    def get_user_permissions(self, page: int = 1, page_size: int = 25) -> GenericResourceList:
        return self._list_generic("user-permissions", page, page_size)

    def get_user_permission(self, user_permission_id: str) -> GenericResource:
        return self._get_generic(f"user-permissions/{user_permission_id}")

    def get_ticket_fees(self, page: int = 1, page_size: int = 25) -> GenericResourceList:
        return self._list_generic("ticket-fees", page, page_size)

    def get_ticket_fee(self, ticket_fee_id: str) -> GenericResource:
        return self._get_generic(f"ticket-fees/{ticket_fee_id}")

    def get_custom_placeholders(self, page: int = 1, page_size: int = 25) -> GenericResourceList:
        return self._list_generic("custom-placeholders", page, page_size)

    def get_custom_placeholder(self, custom_placeholder_id: str) -> GenericResource:
        return self._get_generic(f"custom-placeholders/{custom_placeholder_id}")

    def get_groups(self, page: int = 1, page_size: int = 25) -> GenericResourceList:
        return self._list_generic("groups", page, page_size)

    def get_group(self, group_id: str) -> GenericResource:
        return self._get_generic(f"groups/{group_id}")

    def get_panel_permissions(self, page: int = 1, page_size: int = 25) -> GenericResourceList:
        return self._list_generic("panel-permissions", page, page_size)

    def get_panel_permission(self, panel_permission_id: str) -> GenericResource:
        return self._get_generic(f"panel-permissions/{panel_permission_id}")

    def get_custom_system_roles(self, page: int = 1, page_size: int = 25) -> GenericResourceList:
        return self._list_generic("custom-system-roles", page, page_size)

    def get_custom_system_role(self, custom_system_role_id: str) -> GenericResource:
        return self._get_generic(f"custom-system-roles/{custom_system_role_id}")

    def get_event_role_permissions(self, page: int = 1, page_size: int = 25) -> GenericResourceList:
        return self._list_generic("event-role-permissions", page, page_size)

    def get_event_role_permission(self, event_role_permission_id: str) -> GenericResource:
        return self._get_generic(f"event-role-permissions/{event_role_permission_id}")

    def get_email_notifications(self, page: int = 1, page_size: int = 25) -> GenericResourceList:
        return self._list_generic("email-notifications", page, page_size)

    def get_email_notification(self, email_notification_id: str) -> GenericResource:
        return self._get_generic(f"email-notifications/{email_notification_id}")
