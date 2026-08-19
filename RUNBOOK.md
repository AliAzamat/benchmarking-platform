# Platform runbook

## Health
- Gateway live: `GET :8001/metrics` returns 200.
- Watch `stream_latency_ms` p99 in Grafana — if it climbs, the live view lags.
- Watch `runs_streamed_total` rate — flat during a batch means runs aren't
  reaching the gateway (check Redis pub/sub and worker logs).
- Postgres row growth: `SELECT count(*) FROM runs;` should rise during a run.

## Common incidents
- **Dashboards show nothing**: confirm the matrix calls `publish_run`, the
  gateway subscribed to `runs:events`, and the load balancer allows WebSocket
  upgrades.
- **Stream latency climbing**: check Redis CPU and gateway event-loop lag; scale
  out gateway replicas — they all subscribe to Redis, so fan-out is shared.
- **Leaderboard disagrees with Postgres**: the live table is a running average
  in the browser; reconnect to rebuild it, and reconcile against `leaderboard.sql`.
- **Rate-limit (429) storms**: lower `max_concurrency` in `run_matrix`; raise it
  back once the provider's limits recover.

## Deploy to AWS
- Push `gateway` and `worker` images to ECR; run on ECS/Fargate.
- ElastiCache for Redis (pub/sub + queue), RDS for Postgres (runs).
- Terminate TLS at an ALB and use `wss://`; allow long idle timeouts for sockets.
- Scale workers for throughput and gateway replicas for connected dashboards —
  independently, because Redis decouples them.
