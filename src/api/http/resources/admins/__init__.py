from .account_resource import AccountResource
from .login import LoginResource
from .organization_resource import OrganizationResource
from .organization_account_resource import OrganizationAccountResource
from .role_resource import RoleResource
from .storage_resource import AdminStorageResource as StorageResource

resources = [
    RoleResource(),
    LoginResource(),
    AccountResource(),
    StorageResource(),
    OrganizationResource(),
    OrganizationAccountResource()]
