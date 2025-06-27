from model.order import OrderDetail, Order
from model.product import Product
from utils.indexing import indexing
from database import db


class OrderService:
    @classmethod
    def order_product(cls, user_id, address, order_list):
        order = Order(user_id=user_id, address=address)
        db.session.add(order)
        db.session.flush()

        product_ids = [order["product_id"] for order in order_list]
        products = Product.query.filter(Product.id.in_(product_ids)).all()
        indexed_product = indexing(products, key=lambda x: x.id)

        order_details = OrderDetailService.create_order_detail(
            order_list, indexed_product, order
        )

        db.session.add_all(order_details)
        db.session.commit()

    @classmethod
    def order_product_with_pessimistic_lock(cls, user_id, address, order_list):
        try:
            with db.session.begin():
                order = Order(user_id=user_id, address=address)
                db.session.add(order)
                db.session.flush()

                product_ids = [order["product_id"] for order in order_list]
                products = (
                    Product.query.filter(Product.id.in_(product_ids))
                    .with_for_update()
                    .all()
                )
                indexed_product = indexing(products, key=lambda x: x.id)

                order_details = OrderDetailService.create_order_detail(
                    order_list, indexed_product, order
                )

                db.session.add_all(order_details)
                db.session.commit()
        except:
            db.session.rollback()
            raise

    @classmethod
    def order_product_with_redis_lock(cls, user_id, address, order_list):
        order = Order(user_id=user_id, address=address)
        db.session.add(order)
        db.session.flush()

        product_ids = [order["product_id"] for order in order_list]
        products = Product.query.filter(Product.id.in_(product_ids)).all()
        indexed_product = indexing(products, key=lambda x: x.id)

        order_details = OrderDetailService.create_order_detail(
            order_list, indexed_product, order
        )

        db.session.add_all(order_details)
        db.session.commit()

    @classmethod
    def order_product_correct_lock(cls, user_id, address, order_list):
        order = Order(user_id=user_id, address=address)
        db.session.add(order)
        db.session.flush()

        product_ids = [order["product_id"] for order in order_list]
        products = (
            Product.query.filter(Product.id.in_(product_ids)).with_for_update().all()
        )
        indexed_product = indexing(products, key=lambda x: x.id)

        order_details = OrderDetailService.create_order_detail_with_redis_lock(
            order_list, indexed_product, order
        )

        db.session.add_all(order_details)
        db.session.commit()


class OrderDetailService:

    @classmethod
    def create_order_detail(cls, order_list, indexed_product, order):
        order_details = []

        for order_detail in order_list:
            order_product = indexed_product[order_detail["product_id"]]
            if order_product.stock < order_detail["count"]:
                raise Exception("재고가 부족합니다.")

            order_details.append(
                OrderDetail(
                    order_id=order.id,
                    product_id=order_detail["product_id"],
                    count=order_detail["count"],
                    price=order_detail["price"],
                )
            )

            order_product.decrease_stock(order_detail["count"])
            db.session.add(order_product)

        return order_details

    @classmethod
    def create_order_detail_with_redis_lock(cls, order_list, indexed_product, order):
        order_details = []

        for order_detail in order_list:
            order_product = indexed_product[order_detail["product_id"]]
            from infra.redis import create_order_redlock
            from time import sleep

            with create_order_redlock(order_product.id):
                if order_product.stock < order_detail["count"]:
                    raise Exception("재고가 부족합니다.")

                order_details.append(
                    OrderDetail(
                        order_id=order.id,
                        product_id=order_detail["product_id"],
                        count=order_detail["count"],
                        price=order_detail["price"],
                    )
                )

                order_product.decrease_stock(order_detail["count"])
                db.session.add(order_product)
                sleep(1)  # 커밋되는 시간에 다른 쓰레드가 접근하여 DB접근이 성공되어버림

        return order_details
