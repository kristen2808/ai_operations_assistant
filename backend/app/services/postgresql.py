from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def get_connection_stats(db: AsyncSession) -> dict:
    result = await db.execute(
        text(
            """
            SELECT
                COUNT(*) AS total,
                COUNT(*) FILTER (WHERE state = 'active') AS active,
                COUNT(*) FILTER (WHERE state = 'idle') AS idle,
                COUNT(*) FILTER (
                    WHERE state = 'idle in transaction'
                ) AS idle_in_transaction
            FROM pg_stat_activity
            WHERE backend_type = 'client backend'
            """
        )
    )
    return dict(result.mappings().one())
