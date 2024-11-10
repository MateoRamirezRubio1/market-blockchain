from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from app.infrastructure.database.db_connection import db_dependency
from app.domain.models.sale import Sale
from app.domain.models.sale import SaleStatus
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


async def sales_verifier(db):
    result = await db.execute(
        select(Sale)
        .options(selectinload(Sale.offer))
        .filter(Sale.status != SaleStatus.penalized)
    )
    sales = result.scalars().all()

    for sale in sales:
        await sale.verify_sales_compliance()

    await db.commit()


async def sales_verifier_task():
    db_gen = db_dependency()  # Crear el generador manualmente
    db = await anext(db_gen)  # Obtener la primera instancia de AsyncSession
    try:
        await sales_verifier(db)
    finally:
        # Asegurarse de cerrar la sesión de la base de datos
        await db.close()
        await db_gen.aclose()


def scheduler_inicializer():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(sales_verifier_task, "interval", minutes=1)
    scheduler.start()
