# ⚡ SPIDY AI — SYSTEM TELEMETRY & WEBSOCKET ENGINE

## Telemetry Endpoints & WebSocket Events

### REST Telemetry Endpoint
- **GET** `/api/system`
- **Response:**
```json
{
  "cpu_percent": 24.5,
  "memory_percent": 58.2,
  "disk_percent": 45.1,
  "battery_percent": 88.0,
  "battery_charging": false,
  "volume": 50,
  "network_connected": true,
  "processes": 218,
  "uptime_sec": 420.5
}
```

### WebSocket Event Stream Endpoint
- **WS** `ws://127.0.0.1:8088/ws/spidy`
- **Broadcast Payload Structure:**
```json
{
  "event_type": "VOICE_STATE_CHANGED",
  "state": "LISTENING",
  "timestamp": 1720000000.123,
  "message": "Wake word 'Hey Spidy' detected!",
  "data": {}
}
```
