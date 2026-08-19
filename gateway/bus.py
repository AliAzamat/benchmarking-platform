import redis.asyncio as redis

from agent.run_event import RunEvent

# Two clients: one to publish, one to subscribe (subscriber mode is exclusive).
pub = redis.from_url("redis://localhost:6379")
sub = redis.from_url("redis://localhost:6379")

CHANNEL = "runs:events"


async def publish_run(event: RunEvent) -> None:
    """A worker publishes every finished run onto the shared channel."""
    await pub.publish(CHANNEL, event.to_json())


async def subscribe_runs(on_event) -> None:
    """The gateway subscribes and forwards every run to a handler."""
    pubsub = sub.pubsub()
    await pubsub.subscribe(CHANNEL)
    async for message in pubsub.listen():
        if message["type"] == "message":
            on_event(message["data"])
