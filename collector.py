import asyncio
import json
import websockets

API_KEY = "API-KEY"

# Caixa delimitadora para a zona de Lisboa / Tejo
BOUNDING_BOX = [
    [38.45, -9.55],  # Canto inferior esquerdo (Sul/Oeste)
    [38.80, -9.00]   # Canto superior direito (Norte/Este)
]

SUBSCRIBE_MESSAGE = {
    "APIKey": API_KEY,
    "BoundingBoxes": [BOUNDING_BOX],
    "FilterMessageTypes": ["PositionReport"]
}

async def connect_ais_stream():
    url = "wss://stream.aisstream.io/v0/stream"
    
    async with websockets.connect(url) as ws:
        await ws.send(json.dumps(SUBSCRIBE_MESSAGE))
        print("Ligado à AISStream. A aguardar tráfego...")

        while True:
            message = await ws.recv()
            data = json.loads(message)

            if data.get("MessageType") == "PositionReport":
                report = data["Message"]["PositionReport"]
                metadata = data.get("MetaData", {})

                ship_info = {
                    "mmsi": report.get("UserID"),
                    "name": metadata.get("ShipName", "Desconhecido").strip(),
                    "lat": report.get("Latitude"),
                    "lon": report.get("Longitude"),
                    "sog": report.get("Sog"),       # Velocidade sobre o solo (nós)
                    "cog": report.get("Cog"),       # Rumo (graus)
                    "time": metadata.get("time_utc")
                }
                print(f"Navio: {ship_info['name']} (MMSI: {ship_info['mmsi']}) | Lat: {ship_info['lat']}, Lon: {ship_info['lon']} | Vel: {ship_info['sog']} kts")

if __name__ == "__main__":
    asyncio.run(connect_ais_stream())