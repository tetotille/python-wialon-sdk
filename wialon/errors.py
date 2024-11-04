class InvalidSession(Exception):
    """Error code 1: Invalid session"""
    pass

class InvalidServiceName(Exception):
    """Error code 2: Invalid service name"""
    pass

class InvalidResult(Exception):
    """Error code 3: Invalid result"""
    pass

class InvalidInput(Exception):
    """Error code 4: Invalid input"""
    pass

class ErrorPerformingRequest(Exception):
    """Error code 5: Error performing request"""
    pass

class UnknownError(Exception):
    """Error code 6: Unknown error"""
    pass

class AccessDenied(Exception):
    """Error code 7: Access denied"""
    pass

class InvalidUserNameOrPassword(Exception):
    """Error code 8: Invalid user name or password"""
    pass

class AuthorizationServerUnavailable(Exception):
    """Error code 9: Authorization server is unavailable"""
    pass

class ReachedLimitOfConcurrentRequests(Exception):
    """Error code 10: Reached limit of concurrent requests"""
    pass

class PasswordResetError(Exception):
    """Error code 11: Password reset error"""
    pass

class BillingError(Exception):
    """Error code 14: Billing error"""
    pass

class NoMessagesForSelectedInterval(Exception):
    """Error code 1001: No messages for selected interval"""
    pass

class ItemAlreadyExists(Exception):
    """Error code 1002: Item with such unique property already exists or Item cannot be created according to billing restrictions"""
    pass

class LimitOfMessagesExceeded(Exception):
    """Error code 1004: Limit of messages has been exceeded"""
    pass

class ExecutionTimeExceeded(Exception):
    """Error code 1005: Execution time has exceeded the limit"""
    pass

class ExceedingLimitOfTwoFactorAttempts(Exception):
    """Error code 1006: Exceeding the limit of attempts to enter a two-factor authorization code"""
    pass

class IpChangedOrSessionExpired(Exception):
    """Error code 1011: Your IP has changed or session has expired"""
    pass

class TransferUnitNotPossible(Exception):
    """Error code 2006: No possible to transfer unit to this account"""
    pass

class NoAccessToUnit(Exception):
    """Error code 2008: User doesn't have access to unit (due transferring to new account)"""
    pass

class UserIsCreator(Exception):
    """Error code 2014: Selected user is a creator for some system objects, thus this user cannot be bound to a new account"""
    pass

class SensorDeletingForbidden(Exception):
    """Error code 2015: Sensor deleting is forbidden because of using in another sensor or advanced properties of the unit"""
    pass

class SessionException(Exception):
    """No session has been logged down and there is no sessionId"""

def validate_error(response):
    if "error" in response:
        error_code = response["error"]
        if error_code == 1:
            raise InvalidSession
        elif error_code == 2:
            raise InvalidServiceName
        elif error_code == 3:
            raise InvalidResult
        elif error_code == 4:
            raise InvalidInput
        elif error_code == 5:
            raise ErrorPerformingRequest
        elif error_code == 6:
            raise UnknownError
        elif error_code == 7:
            raise AccessDenied
        elif error_code == 8:
            raise InvalidUserNameOrPassword
        elif error_code == 9:
            raise AuthorizationServerUnavailable
        elif error_code == 10:
            raise ReachedLimitOfConcurrentRequests
        elif error_code == 11:
            raise PasswordResetError
        elif error_code == 14:
            raise BillingError
        elif error_code == 1001:
            raise NoMessagesForSelectedInterval
        elif error_code == 1002:
            raise ItemAlreadyExists
        elif error_code == 1004:
            raise LimitOfMessagesExceeded
        elif error_code == 1005:
            raise ExecutionTimeExceeded
        elif error_code == 1006:
            raise ExceedingLimitOfTwoFactorAttempts
        elif error_code == 1011:
            raise IpChangedOrSessionExpired
        elif error_code == 2006:
            raise TransferUnitNotPossible
        elif error_code == 2008:
            raise NoAccessToUnit
        elif error_code == 2014:
            raise UserIsCreator
        elif error_code == 2015:
            raise SensorDeletingForbidden