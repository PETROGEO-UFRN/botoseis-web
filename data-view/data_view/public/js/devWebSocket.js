// dev WebSocket to detect server restart
const ws = new WebSocket(`ws://${location.host}/ws-autoreload`)
ws.onclose = () => location.reload()