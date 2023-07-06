# if __name__ == '__main__':
#     consumer = ConfiguredKafkaConsumer(InternalEventConsumerKafkaConfig())
#     runner = BasedConsumerRunner(consumer, INTERNAL_EVENTS, MediatorGetter, MongoRepositoryInjector(),
#                                  worker_name='Long cycle internal event')
#
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(init_collections())
#     loop.run_until_complete(runner.consume())
