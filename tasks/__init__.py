from event_bus import EventBus
from tasks.bus import bus, NullEventBus, DefaultEventBus
from tasks.handler.collection import UpdateCollectionThumbnailEventHandler
from tasks.handler.email import IncomingRatingEventHandler, IncomingDishRequestEventHandler, \
    IncomingRegistrationEventHandler
from tasks.handler.fidelity import RatingCreditEventHandler
from tasks.handler.history import SearchHistoryEventHandler, ViewHistoryEventHandler
from tasks.handler.media import RenameMediaEventHandler
from tasks.model.collection import UpdateCollectionThumbnailEventData
from tasks.model.email import IncomingRatingEventData, IncomingDishRequestEventData, \
    IncomingRegistrationEventData
from tasks.model.fidelity import RatingCreditEventData
from tasks.model.history import SearchHistoryEventData, ViewHistoryEventData
from tasks.model.media import RenameMediaEventData
from tasks.queue import queue

bus.init(EventBus())

bus.register(SearchHistoryEventData, [SearchHistoryEventHandler.handle_event])
bus.register(ViewHistoryEventData, [ViewHistoryEventHandler.handle_event])
bus.register(IncomingRatingEventData, [IncomingRatingEventHandler.handle_event])
bus.register(IncomingDishRequestEventData, [IncomingDishRequestEventHandler.handle_event])
bus.register(IncomingRegistrationEventData, [IncomingRegistrationEventHandler.handle_event])
bus.register(UpdateCollectionThumbnailEventData, [UpdateCollectionThumbnailEventHandler.handle_event])
bus.register(RenameMediaEventData, [RenameMediaEventHandler.handle_event])
bus.register(RatingCreditEventData, [RatingCreditEventHandler.handle_event])


def init_app(app):
    queue.init_app(app)