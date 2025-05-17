from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from .models import User, Auction, Order, OrderStatus, OrderType
from .database import SessionLocal

class DatabaseManager:
    def __init__(self):
        self.db = SessionLocal()

    def get_user_by_address(self, address: str) -> Optional[User]:
        return self.db.query(User).filter(User.address == address).first()

    def create_user(self, address: str) -> User:
        user = User(address=address)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_or_create_user(self, address: str) -> User:
        user = self.get_user_by_address(address)
        if not user:
            user = self.create_user(address)
        return user

    def create_auction(self, creator_address: str, nft_token_id: str, title: str, 
                      description: str, starting_price: float, min_bid_increment: float,
                      start_time: datetime, end_time: datetime) -> Auction:
        creator = self.get_or_create_user(creator_address)
        auction = Auction(
            creator_id=creator.id,
            nft_token_id=nft_token_id,
            title=title,
            description=description,
            starting_price=starting_price,
            min_bid_increment=min_bid_increment,
            start_time=start_time,
            end_time=end_time,
            status=OrderStatus.ACTIVE
        )
        self.db.add(auction)
        self.db.commit()
        self.db.refresh(auction)
        return auction

    def get_active_auctions(self) -> List[Auction]:
        return self.db.query(Auction).filter(
            Auction.status == OrderStatus.ACTIVE,
            Auction.end_time > datetime.utcnow()
        ).all()

    def get_user_bids(self, address: str) -> List[Order]:
        user = self.get_user_by_address(address)
        if not user:
            return []
        return self.db.query(Order).filter(
            Order.bidder_id == user.id,
            Order.order_type == OrderType.BID
        ).all()

    def get_user_asks(self, address: str) -> List[Order]:
        user = self.get_user_by_address(address)
        if not user:
            return []
        return self.db.query(Order).filter(
            Order.seller_id == user.id,
            Order.order_type == OrderType.ASK
        ).all()

    def place_bid(self, auction_id: int, bidder_address: str, price: float) -> Order:
        bidder = self.get_or_create_user(bidder_address)
        auction = self.db.query(Auction).filter(Auction.id == auction_id).first()
        
        if not auction or auction.status != OrderStatus.ACTIVE:
            raise ValueError("Auction not found or not active")

        if price < auction.starting_price:
            raise ValueError("Bid price below starting price")

        # Vérifier si le prix est supérieur au dernier bid + min_increment
        last_bid = self.db.query(Order).filter(
            Order.auction_id == auction_id,
            Order.order_type == OrderType.BID,
            Order.status == OrderStatus.ACTIVE
        ).order_by(Order.price.desc()).first()

        if last_bid and price <= last_bid.price + auction.min_bid_increment:
            raise ValueError("Bid price must be higher than last bid + minimum increment")

        order = Order(
            auction_id=auction_id,
            bidder_id=bidder.id,
            order_type=OrderType.BID,
            price=price,
            status=OrderStatus.ACTIVE
        )
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def get_auction_bids(self, auction_id: int) -> List[Order]:
        return self.db.query(Order).filter(
            Order.auction_id == auction_id,
            Order.order_type == OrderType.BID,
            Order.status == OrderStatus.ACTIVE
        ).order_by(Order.price.desc()).all()

    def get_auction_winner(self, auction_id: int) -> Optional[Order]:
        return self.db.query(Order).filter(
            Order.auction_id == auction_id,
            Order.order_type == OrderType.BID,
            Order.status == OrderStatus.ACTIVE
        ).order_by(Order.price.desc()).first()

    def close_auction(self, auction_id: int) -> Optional[Order]:
        auction = self.db.query(Auction).filter(Auction.id == auction_id).first()
        if not auction:
            return None

        winner = self.get_auction_winner(auction_id)
        if winner:
            winner.status = OrderStatus.COMPLETED
            auction.status = OrderStatus.COMPLETED
            self.db.commit()
            self.db.refresh(winner)
            return winner
        return None 