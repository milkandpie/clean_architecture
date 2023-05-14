from .artifact import ArtifactResource
from .category import CategoryResource
from .document import DocumentResource
from .event import EventResource
from .extra import ExtraResource
from .file import FileResource
from .notable import NotableResource
from .project import ProjectResource
from .project_items import ProjectItemResource
from .storage_origin import StorageOriginResource
from .storage_state import StorageStateResource
from .tag_resource import TagResource
from .translation import TranslationResource
from .storage_resource import ManagementStorageResource
from .aproved_order import ApprovedOrderResource
from .order_status import OrderStatusResource

resources = [
    ApprovedOrderResource(),
    CategoryResource(),
    ExtraResource(),
    ArtifactResource(),
    DocumentResource(),
    EventResource(),
    FileResource(),
    NotableResource(),
    StorageOriginResource(),
    StorageStateResource(),
    TagResource(),
    TranslationResource(),
    ProjectResource(),
    ProjectItemResource(),
    ManagementStorageResource(),
    OrderStatusResource()
]
