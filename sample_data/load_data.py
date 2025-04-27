import asyncio
import csv

import httpx


URL = "http://0.0.0.0:5321/crude-oil-imports/bulk"
BATCH_SIZE = 1000


async def main():
    async with httpx.AsyncClient() as client:
        with open("data.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            batch = []
            for row in reader:
                params = {
                    "year": row["year"],
                    "month": row["month"],
                    "originName": row["originName"],
                    "originTypeName": row["originTypeName"],
                    "destinationName": row["destinationName"],
                    "destinationTypeName": row["destinationTypeName"],
                    "gradeName": row["gradeName"],
                    "quantity": row["quantity"],
                }
                batch.append(params)
                if len(batch) == BATCH_SIZE:
                    resp = await client.post(url=URL, json=batch)
                    resp.raise_for_status()
                    batch = []

            # Send the final batch
            resp = await client.post(url=URL, json=batch)
            resp.raise_for_status()


asyncio.run(main())
