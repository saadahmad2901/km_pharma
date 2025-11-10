from sqlalchemy.orm import Session
from sqlalchemy import join
from app import schemas, models
from typing import List


def create_distributer_product(
    distributer_product: schemas.DistributerProductsCreate, db: Session
) -> models.DistributerProducts:
    db_distributer_product = models.DistributerProducts(**distributer_product.dict())
    db.add(db_distributer_product)
    db.commit()
    db.refresh(db_distributer_product)
    return db_distributer_product


def get_distributer_products(db: Session) -> List[schemas.DistributerProducts]:
    """Return all distributer products with distributer_name and product_name"""
    records = (
        db.query(
            models.DistributerProducts.id,
            models.DistributerProducts.distributer_id,
            models.DistributerProducts.product_id,
            models.DistributerProducts.created_at,
            models.DistributerProducts.updated_at,
            models.Distributers.name.label("distributer_name"),
            models.VeterinaryProduct.name.label("product_name"),
        )
        .join(
            models.Distributers,
            models.DistributerProducts.distributer_id == models.Distributers.id,
        )
        .join(
            models.VeterinaryProduct,
            models.DistributerProducts.product_id == models.VeterinaryProduct.id,
        )
        .all()
    )

    # Convert each record (SQLAlchemy Row) into schema object
    return [
        schemas.DistributerProducts(
            id=r.id,
            distributer_id=r.distributer_id,
            product_id=r.product_id,
            created_at=r.created_at,
            updated_at=r.updated_at,
            distributer_name=r.distributer_name,
            product_name=r.product_name,
        )
        for r in records
    ]


def get_distributer_product_by_id(
    db: Session, distributer_product_id: int
) -> schemas.DistributerProducts | None:
    """Return one distributer product with distributer_name and product_name"""
    r = (
        db.query(
            models.DistributerProducts.id,
            models.DistributerProducts.distributer_id,
            models.DistributerProducts.product_id,
            models.DistributerProducts.created_at,
            models.DistributerProducts.updated_at,
            models.Distributers.name.label("distributer_name"),
            models.VeterinaryProduct.name.label("product_name"),
        )
        .join(
            models.Distributers,
            models.DistributerProducts.distributer_id == models.Distributers.id,
        )
        .join(
            models.VeterinaryProduct,
            models.DistributerProducts.product_id == models.VeterinaryProduct.id,
        )
        .filter(models.DistributerProducts.id == distributer_product_id)
        .first()
    )

    if not r:
        return None

    return schemas.DistributerProducts(
        id=r.id,
        distributer_id=r.distributer_id,
        product_id=r.product_id,
        created_at=r.created_at,
        updated_at=r.updated_at,
        distributer_name=r.distributer_name,
        product_name=r.product_name,
    )
def distributer_product_by_distributer_id(
    distributer_id: int, db: Session
) -> List[schemas.DistributerProducts]:
    """Return all products linked to a specific distributer with names"""
    records = (
        db.query(
            models.DistributerProducts.id,
            models.DistributerProducts.distributer_id,
            models.DistributerProducts.product_id,
            models.DistributerProducts.created_at,
            models.DistributerProducts.updated_at,
            models.Distributers.name.label("distributer_name"),
            models.VeterinaryProduct.name.label("product_name"),
        )
        .join(
            models.Distributers,
            models.DistributerProducts.distributer_id == models.Distributers.id,
        )
        .join(
            models.VeterinaryProduct,
            models.DistributerProducts.product_id == models.VeterinaryProduct.id,
        )
        .filter(models.DistributerProducts.distributer_id == distributer_id)
        .all()
    )

    # Convert query results into schema list
    return [
        schemas.DistributerProducts(
            id=r.id,
            distributer_id=r.distributer_id,
            product_id=r.product_id,
            created_at=r.created_at,
            updated_at=r.updated_at,
            distributer_name=r.distributer_name,
            product_name=r.product_name,
        )
        for r in records
    ]

def update_distributer_product(
    db: Session, distributer_product_id: int, distributer_product: schemas.DistributerProductsUpdate
) -> models.DistributerProducts:
    db_distributer_product = (
        db.query(models.DistributerProducts)
        .filter(models.DistributerProducts.id == distributer_product_id)
        .first()
    )
    if db_distributer_product:
        for key, value in distributer_product.dict().items():
            setattr(db_distributer_product, key, value)
        db.commit()
        db.refresh(db_distributer_product)
    return db_distributer_product


def delete_distributer_product(
    db: Session, distributer_product_id: int
) -> models.DistributerProducts:
    db_distributer_product = (
        db.query(models.DistributerProducts)
        .filter(models.DistributerProducts.id == distributer_product_id)
        .first()
    )
    if db_distributer_product:
        db.delete(db_distributer_product)
        db.commit()
    return db_distributer_product
