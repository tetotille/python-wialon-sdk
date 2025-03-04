"""Errors for Wialon API."""


from typing import Any


class InvalidSessionError(Exception):
    """Error code 1: Invalid session."""


class InvalidServiceNameError(Exception):
    """Error code 2: Invalid service name."""


class InvalidResultError(Exception):
    """Error code 3: Invalid result."""


class InvalidInputError(Exception):
    """Error code 4: Invalid input."""


class PerformingRequestError(Exception):
    """Error code 5: Error performing request."""


class UnknownError(Exception):
    """Error code 6: Unknown error."""


class AccessDeniedError(Exception):
    """Error code 7: Access denied."""


class InvalidUserNameOrPasswordError(Exception):
    """Error code 8: Invalid user name or password."""


class AuthorizationServerUnavailableError(Exception):
    """Error code 9: Authorization server is unavailable."""


class ReachedLimitOfConcurrentRequestsError(Exception):
    """Error code 10: Reached limit of concurrent requests."""


class PasswordResetError(Exception):
    """Error code 11: Password reset error."""


class BillingError(Exception):
    """Error code 14: Billing error."""


class NoMessagesForSelectedIntervalError(Exception):
    """Error code 1001: No messages for selected interval."""


class ItemAlreadyExistsError(Exception):
    """Error code 1002.

    Item with such unique property already exists or
    Item cannot be created according to billing restrictions.
    """


class EncodingError(Exception):
    """Error code 1003: Accept-encoding is not gzip."""


class LimitOfMessagesExceededError(Exception):
    """Error code 1004: Limit of messages has been exceeded."""


class ExecutionTimeExceededError(Exception):
    """Error code 1005: Execution time has exceeded the limit."""


class ExceedingLimitOfTwoFactorAttemptsError(Exception):
    """Error code 1006.

    Exceeding the limit of attempts to enter a two-factor authorization code.
    """


class IpChangedOrSessionExpiredError(Exception):
    """Error code 1011: Your IP has changed or session has expired."""


class TransferUnitNotPossibleError(Exception):
    """Error code 2006: No possible to transfer unit to this account."""


class NoAccessToUnitError(Exception):
    """Error code 2008.

    User doesn't have access to unit (due transferring to new account).
    """


class UserIsCreatorError(Exception):
    """Error code 2014.

    Selected user is a creator for some system objects, thus this user cannot be bound
    to a new account
    """


class SensorDeletingForbiddenError(Exception):
    """Error code 2015.

    Sensor deleting is forbidden because of using in another sensor or
    advanced properties of the unit
    """


class SessionExceptionError(Exception):
    """No session has been logged down and there is no sessionId."""


class FormatError(Exception):
    """Error code 2015: Invalid format. Only Exchange."""


class NoFileReturnedError(Exception):
    """Wheen the exchange does not return a file."""


class ParameterError(Exception):
    """Parameter error."""


ERROR_CODES = {
    1: InvalidSessionError,
    2: InvalidServiceNameError,
    3: InvalidResultError,
    4: InvalidInputError,
    5: PerformingRequestError,
    6: UnknownError,
    7: AccessDeniedError,
    8: InvalidUserNameOrPasswordError,
    9: AuthorizationServerUnavailableError,
    10: ReachedLimitOfConcurrentRequestsError,
    11: PasswordResetError,
    14: BillingError,
    1001: NoMessagesForSelectedIntervalError,
    1002: ItemAlreadyExistsError,
    1003: EncodingError,
    1004: LimitOfMessagesExceededError,
    1005: ExecutionTimeExceededError,
    1006: ExceedingLimitOfTwoFactorAttemptsError,
    1011: IpChangedOrSessionExpiredError,
    2006: TransferUnitNotPossibleError,
    2008: NoAccessToUnitError,
    2014: UserIsCreatorError,
    2015: SensorDeletingForbiddenError,
}


def validate_error(response: dict[str, int | str]|list[dict[str,Any]]) -> None:
    """Validate error in response.

    :param response: Response from Wialon API.
    :type response: dict[str, int | str]
    :raises InvalidSessionError: Error code 1: Invalid session.
    :raises InvalidServiceNameError: Error code 2: Invalid service name.
    :raises InvalidResultError: Error code 3: Invalid result.
    :raises InvalidInputError: Error code 4: Invalid input.
    :raises PerformingRequestError: Error code 5: Error performing request.
    :raises UnknownError: Error code 6: Unknown error.
    :raises AccessDeniedError: Error code 7: Access denied.
    :raises InvalidUserNameOrPasswordError: Error code 8: Invalid user name or password.
    :raises AuthorizationServerUnavailableError: Error code 9: Authorization server is
                                                 unavailable.
    :raises ReachedLimitOfConcurrentRequestsError: Error code 10: Reached limit of
                                                   concurrent requests.
    :raises PasswordResetError: Error code 11: Password reset error.
    :raises BillingError: Error code 14: Billing error.
    :raises NoMessagesForSelectedIntervalError: Error code 1001: No messages for selected
                                                interval.
    :raises ItemAlreadyExistsError: Error code 1002: Item with such unique property
                                    already exists or Item cannot be created according to
                                    billing restrictions.
    :raises EncodingError: Error code 1003: Accept-encoding is not gzip.
    :raises LimitOfMessagesExceededError: Error code 1004: Limit of messages has been
                                          exceeded.
    :raises ExecutionTimeExceededError: Error code 1005: Execution time has exceeded the
                                        limit.
    :raises ExceedingLimitOfTwoFactorAttemptsError: Error code 1006: Exceeding the limit
                                                    of attempts to enter a two-factor
                                                    authorization code.
    :raises IpChangedOrSessionExpiredError: Error code 1011: Your IP has changed or
                                            session has expired.
    :raises TransferUnitNotPossibleError: Error code 2006: No possible to transfer unit
                                          to this account.
    :raises NoAccessToUnitError: Error code 2008: User doesn't have access to unit (due
                                 transferring to new account).
    :raises UserIsCreatorError: Error code 2014: Selected user is a creator for some
                                system objects, thus this user cannot be bound to a
                                new account.
    :raises SensorDeletingForbiddenError: Error code 2015: Sensor deleting is forbidden
                                          because of using in another sensor or advanced
                                          properties of the unit.
    :raises SessionExceptionError: No session has been logged down and there is no
                                   sessionId.
    """
    if isinstance(response, list):
        [validate_error(item) for item in response]
        return
    error_code = response.get("error")
    if error_code is None:
        return
    error_code = int(error_code)
    error_class = ERROR_CODES.get(error_code)
    if error_class:
        if error_code == ERROR_CODES[4] and "reason" in response:
            raise error_class(response["reason"])
        raise error_class
