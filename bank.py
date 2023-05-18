import pickle
import json
import logging
from argparse import ArgumentParser
from abc import ABC, abstractmethod

#logging.config.fileConfig("log.ini")
pattern = logging.Formatter("%(levelname)s - %(lineno)d - %(msg)s")


logger = logging.getLogger("MyLogger")
logger.setLevel(level=logging.INFO)

file_handler = logging.FileHandler("accounts.log", mode="a")
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
console_handler.setFormatter(pattern)
file_handler.setFormatter(pattern)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


class BankAccount(ABC):
    def __init__(self, owner_name: str, balance: int):
        self.owner_name, self.balance = owner_name, balance

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, balance: int):
        if balance < 10_000:
            raise ValueError("Invalid balance")

        self._balance = balance

    def __repr__(self) -> str:
        dictionary = vars(self)
        dictionary["rial"] = self.to_rial(self._balance)
        return str(dictionary)

    def __str__(self) -> str:
        return f"{self.owner_name}: {self._balance:,}"


class ShahrBankAccount(BankAccount):

    __MINIMUM = 10_000
    __accounts = []

    def __init__(self, owner_name: str, balance: int):
        super().__init__(owner_name, balance)
        type(self).__accounts.append(self)

        
    def __add__(self, amount: int):
        if self._balance + amount < self.MINIMUM:
            raise ValueError("Invalid balance")

        return super().__add__(amount)

    def __sub__(self, amount: int):
        if self._balance + amount < self.MINIMUM:
            raise ValueError("Invalid balance")

        return super().__sub__(amount)

    def transfer(self, other: "BankAccount", amount: int):
        if amount < 0:
            logger.error("Raised")
            raise ValueError("Invalid amount")

        self - (amount - 600)
        other + amount
        logger.info("successfully transferred")

    @staticmethod
    def to_rial(balance):
        return balance * 10
    
    @classmethod
    def maximum(cls) -> int:
        return max(
            [account._balance for account in cls.__accounts]
        )

    @classmethod
    def save(cls):
        with open("account.pickle", "wb") as file:
            pickle.dump(cls.__accounts, file)

    @classmethod
    def load(cls):
        with open("account.pickle", "rb") as file:
            cls.__accounts.extend(pickle.load(file))


# parser = ArgumentParser(description="Bank Account Manager")
# parser.add_argument("-f", "--first", metavar="FIRST", required=True, type=int)
# parser.add_argument("-s", "--second", metavar="Second", default=50_000, type=int)
# parser.add_argument("-a", "--amount", metavar="AMOUNT", type=int, help="Value")
# if __name__ == "__main__":
#     args = parser.parse_args()
#     t = args.amount
#     account1.transfer(account2, t)
#     print(account1.balance)
#     print(account2.balance)

account1 = ShahrBankAccount("Sepehr", 100_000)
account2 = ShahrBankAccount("Farzane", 50_000)
account3 = ShahrBankAccount("aria", 150_000)
#print(ShahrBankAccount._SharBankAccount__accounts)
ShahrBankAccount.save()
ShahrBankAccount.load()
print(ShahrBankAccount._ShahrBankAccount__accounts)
print(ShahrBankAccount._ShahrBankAccount__accounts[0].balance)
print(ShahrBankAccount._ShahrBankAccount__accounts[1].balance)
print(ShahrBankAccount._ShahrBankAccount__accounts[2].balance)
