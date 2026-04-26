"""
Financial & Commerce Data Provider.

Generates realistic financial data including:
- Credit card numbers (valid format, fake)
- IBAN/SWIFT codes
- Currencies and amounts
- Transactions
- Invoices
- Stock tickers
- Crypto wallets
- Prices
"""

from __future__ import annotations

from typing import Any
from datetime import date, timedelta
import string

from synthgen.core.base import BaseProvider
from synthgen.core.seed_manager import SeedManager


# Credit Card prefixes by type
CARD_PREFIXES = {
    "visa": ["4"],
    "mastercard": ["51", "52", "53", "54", "55"],
    "amex": ["34", "37"],
    "discover": ["6011", "622126", "622127", "622128", "622129", "62213", "62214", "62215", "62216", "62217", "62218", "62219", "6222", "6223", "6224", "6225", "6226", "6227", "6228", "6229", "64", "65"],
    "diners": ["300", "301", "302", "303", "304", "305", "36", "38"],
    "jcb": ["3528", "3529", "353", "354", "355", "356", "357", "358"],
}

CURRENCIES = [
    ("USD", "$", "United States Dollar"),
    ("EUR", "€", "Euro"),
    ("GBP", "£", "British Pound"),
    ("JPY", "¥", "Japanese Yen"),
    ("CNY", "¥", "Chinese Yuan"),
    ("AUD", "A$", "Australian Dollar"),
    ("CAD", "C$", "Canadian Dollar"),
    ("CHF", "Fr", "Swiss Franc"),
    ("INR", "₹", "Indian Rupee"),
    ("BRL", "R$", "Brazilian Real"),
    ("MXN", "$", "Mexican Peso"),
    ("KRW", "₩", "South Korean Won"),
    ("RUB", "₽", "Russian Ruble"),
    ("SGD", "S$", "Singapore Dollar"),
    ("HKD", "HK$", "Hong Kong Dollar"),
]

CRYPTO_CURRENCIES = [
    ("BTC", "Bitcoin"),
    ("ETH", "Ethereum"),
    ("USDT", "Tether"),
    ("BNB", "Binance Coin"),
    ("XRP", "Ripple"),
    ("ADA", "Cardano"),
    ("DOGE", "Dogecoin"),
    ("SOL", "Solana"),
    ("TRX", "Tron"),
    ("DOT", "Polkadot"),
]

STOCK_EXCHANGES = {
    "NYSE": ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "BRK.A", "JPM", "V", "JNJ"],
    "NASDAQ": ["NVDA", "PYPL", "INTC", "CMCSA", "NFLX", "ADBE", "PEP", "CSCO", "AVGO", "TXN"],
    "LSE": ["HSBA", "BP", "SHEL", "AZN", "GSK", "DGE", "ULVR", "RIO", "BHP", "BARC"],
    "TSE": ["7203", "9984", "6861", "9432", "6758", "9983", "8306", "6902", "8035", "4063"],
}

COMPANY_SUFFIXES = [
    "Inc", "LLC", "Corp", "Corporation", "Ltd", "Limited", "Co", "Company",
    "Group", "Holdings", "Partners", "Associates", "Enterprises", "Industries"
]


def luhn_checksum(partial_number: str) -> int:
    """Calculate Luhn checksum digit."""
    def digits_of(n: str) -> list[int]:
        return [int(d) for d in n]
    
    digits = digits_of(partial_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(str(d * 2)))
    return (10 - (checksum % 10)) % 10


class FinancialProvider(BaseProvider):
    """
    Provider for financial and commerce data.

    Generates synthetic financial data for testing and development.
    All generated data is fake and should not be used for real transactions.

    Example:
        >>> provider = FinancialProvider(seed_manager)
        >>> provider.credit_card_number()
        '4532015112830366'
    """

    def __init__(self, seed_manager: SeedManager | None = None) -> None:
        """
        Initialize the financial data provider.

        Args:
            seed_manager: Seed manager for reproducibility.
        """
        super().__init__(seed_manager)
        self._sm = seed_manager

    def _get_sm(self) -> SeedManager:
        """Get seed manager or raise error if not set."""
        if self._sm is None:
            raise RuntimeError("SeedManager not initialized")
        return self._sm

    def credit_card_number(self, card_type: str = "visa") -> str:
        """
        Generate a fake credit card number with valid Luhn checksum.

        Args:
            card_type: Type of card ('visa', 'mastercard', 'amex', 'discover').

        Returns:
            Fake credit card number (valid format, not real).

        Warning:
            This generates syntactically valid but completely fake numbers.
            Never use for actual payment processing.
        """
        sm = self._get_sm()
        prefixes = CARD_PREFIXES.get(card_type.lower(), CARD_PREFIXES["visa"])
        prefix = sm.random_choice(prefixes)

        # Generate remaining digits (16 total for most cards, 15 for Amex)
        if card_type.lower() == "amex":
            length = 15
            remaining_length = length - len(prefix) - 1
        else:
            length = 16
            remaining_length = length - len(prefix) - 1

        remaining = "".join(str(sm.random_int(0, 9)) for _ in range(remaining_length))
        partial = prefix + remaining
        checksum = luhn_checksum(partial)

        return partial + str(checksum)

    def credit_card_expiry(self, years_ahead: int = 5) -> str:
        """
        Generate a credit card expiry date.

        Args:
            years_ahead: Maximum years in the future.

        Returns:
            Expiry date in MM/YY format.
        """
        sm = self._get_sm()
        today = date.today()
        months_ahead = sm.random_int(1, years_ahead * 12)
        expiry = today + timedelta(days=months_ahead * 30)
        return f"{expiry.month:02d}/{expiry.year % 100:02d}"

    def credit_card_cvv(self, card_type: str = "visa") -> str:
        """
        Generate a CVV code.

        Args:
            card_type: Type of card (Amex uses 4 digits, others use 3).

        Returns:
            CVV code.
        """
        sm = self._get_sm()
        if card_type.lower() == "amex":
            return str(sm.random_int(1000, 9999))
        return str(sm.random_int(100, 999))

    def credit_card_full(self, card_type: str = "visa") -> dict[str, str]:
        """
        Generate complete fake credit card details.

        Args:
            card_type: Type of card.

        Returns:
            Dictionary with number, expiry, cvv, and type.
        """
        return {
            "number": self.credit_card_number(card_type),
            "expiry": self.credit_card_expiry(),
            "cvv": self.credit_card_cvv(card_type),
            "type": card_type,
        }

    def iban(self, country_code: str = "DE") -> str:
        """
        Generate a fake IBAN (International Bank Account Number).

        Args:
            country_code: Two-letter country code.

        Returns:
            Fake IBAN string.
        """
        sm = self._get_sm()
        country_code = country_code.upper()[:2]

        # Generate BBAN (Basic Bank Account Number) - varies by country
        bban_length = 18  # Simplified generic length
        bban = "".join(str(sm.random_int(0, 9)) for _ in range(bban_length))

        # Calculate check digits using simplified method
        numeric_country = "".join(str(ord(c) - ord('A') + 10) for c in country_code)
        check_string = bban + numeric_country + "00"
        check_digits = 98 - (int(check_string) % 97)

        return f"{country_code}{check_digits:02d}{bban}"

    def swift_bic(self) -> str:
        """
        Generate a fake SWIFT/BIC code.

        Returns:
            Fake SWIFT code (8 or 11 characters).
        """
        sm = self._get_sm()
        # Format: AAAA BB CC DDD (Bank, Country, Location, Branch)
        bank = "".join(sm.random_sample(list(string.ascii_uppercase), 4))
        country = "".join(sm.random_sample(list(string.ascii_uppercase), 2))
        location = "".join(str(sm.random_int(0, 9)) for _ in range(2))

        if sm.random_bool(0.7):
            # 8 character format
            return f"{bank}{country}{location}"
        else:
            # 11 character format with branch
            branch = "".join(sm.random_sample(list(string.ascii_uppercase), 3))
            return f"{bank}{country}{location}{branch}"

    def currency(self) -> tuple[str, str, str]:
        """
        Generate currency information.

        Returns:
            Tuple of (code, symbol, name).
        """
        sm = self._get_sm()
        return sm.random_choice(CURRENCIES)

    def amount(
        self,
        min_val: float = 0.01,
        max_val: float = 10000.0,
        currency: str | None = None,
        decimal_places: int = 2,
    ) -> dict[str, Any]:
        """
        Generate a monetary amount.

        Args:
            min_val: Minimum amount.
            max_val: Maximum amount.
            currency: Optional currency code (random if not specified).
            decimal_places: Number of decimal places.

        Returns:
            Dictionary with amount, currency, and formatted string.
        """
        sm = self._get_sm()
        amount = sm.random_float(min_val, max_val)
        amount = round(amount, decimal_places)

        curr_info = self.currency() if currency is None else next(
            (c for c in CURRENCIES if c[0] == currency), ("USD", "$", "US Dollar")
        )

        return {
            "value": amount,
            "currency_code": curr_info[0],
            "symbol": curr_info[1],
            "currency_name": curr_info[2],
            "formatted": f"{curr_info[1]}{amount:,.{decimal_places}f}",
        }

    def transaction(self) -> dict[str, Any]:
        """
        Generate a fake transaction record.

        Returns:
            Dictionary with transaction details.
        """
        sm = self._get_sm()
        today = date.today()
        days_ago = sm.random_int(0, 365)
        tx_date = today - timedelta(days=days_ago)

        types = ["debit", "credit", "payment", "refund", "transfer"]
        statuses = ["completed", "pending", "failed", "processing"]
        merchants = [
            "Amazon", "Walmart", "Target", "Best Buy", "Costco", "Home Depot",
            "Starbucks", "McDonald's", "Shell", "Chevron", "Netflix", "Spotify",
            "Apple Store", "Google Play", "Uber", "Lyft", "Airbnb", "Hotel Booking"
        ]

        tx_type = sm.random_choice(types)
        amount_info = self.amount(1.0, 5000.0)

        return {
            "id": self.transaction_id(),
            "date": tx_date.isoformat(),
            "timestamp": f"{tx_date.isoformat()}T{sm.random_int(0, 23):02d}:{sm.random_int(0, 59):02d}:{sm.random_int(0, 59):02d}Z",
            "type": tx_type,
            "amount": amount_info,
            "merchant": sm.random_choice(merchants),
            "status": sm.random_choice(statuses),
            "account_from": self.account_number(),
            "account_to": self.account_number() if tx_type != "debit" else None,
        }

    def transaction_id(self) -> str:
        """Generate a unique transaction ID."""
        sm = self._get_sm()
        prefix = sm.random_choice(["TXN", "PAY", "ORD", "INV"])
        timestamp = "".join(str(sm.random_int(0, 9)) for _ in range(8))
        suffix = "".join(sm.random_sample(list(string.ascii_uppercase), 3))
        return f"{prefix}{timestamp}{suffix}"

    def account_number(self, length: int = 10) -> str:
        """
        Generate a fake bank account number.

        Args:
            length: Length of the account number.

        Returns:
            Fake account number.
        """
        sm = self._get_sm()
        return "".join(str(sm.random_int(0, 9)) for _ in range(length))

    def routing_number(self) -> str:
        """
        Generate a fake US routing number (ABA).

        Returns:
            Fake 9-digit routing number.
        """
        sm = self._get_sm()
        # First two digits must be 00-12, 21-32, 61-72, or 80
        first = sm.random_int(0, 12)
        second = sm.random_int(0, 9)
        remaining = "".join(str(sm.random_int(0, 9)) for _ in range(6))
        # Last digit is checksum (simplified - just random for mock data)
        checksum = sm.random_int(0, 9)
        return f"{first:02d}{second}{remaining}{checksum}"

    def stock_ticker(self, exchange: str | None = None) -> dict[str, str]:
        """
        Generate a fake stock ticker.

        Args:
            exchange: Optional exchange ('NYSE', 'NASDAQ', etc.).

        Returns:
            Dictionary with symbol and exchange.
        """
        sm = self._get_sm()
        if exchange and exchange.upper() in STOCK_EXCHANGES:
            symbols = STOCK_EXCHANGES[exchange.upper()]
            symbol = sm.random_choice(symbols)
        else:
            # Generate random ticker
            length = sm.random_int(3, 5)
            symbol = "".join(sm.random_sample(list(string.ascii_uppercase), length))
            exchange = sm.random_choice(list(STOCK_EXCHANGES.keys()))

        return {
            "symbol": symbol,
            "exchange": exchange or sm.random_choice(list(STOCK_EXCHANGES.keys())),
        }

    def crypto_wallet_address(self, crypto: str = "BTC") -> str:
        """
        Generate a fake cryptocurrency wallet address.

        Args:
            crypto: Cryptocurrency type ('BTC', 'ETH', etc.).

        Returns:
            Fake wallet address.
        """
        sm = self._get_sm()
        crypto = crypto.upper()

        if crypto == "BTC":
            # Bitcoin addresses start with 1, 3, or bc1
            prefix = sm.random_choice(["1", "3", "bc1"])
            length = 33 if prefix in ["1", "3"] else 42
            chars = string.ascii_letters + string.digits
            return prefix + "".join(sm.random_sample(list(chars), length - len(prefix)))
        elif crypto == "ETH":
            # Ethereum addresses are 0x + 40 hex chars
            hex_chars = "0123456789abcdef"
            address = "0x" + "".join(sm.random_sample(list(hex_chars), 40))
            return address
        else:
            # Generic format
            prefix = sm.random_choice(["addr_", "wallet_", "acc_"])
            hex_chars = "0123456789abcdef"
            return prefix + "".join(sm.random_sample(list(hex_chars), 32))

    def invoice_number(self, prefix: str = "INV") -> str:
        """
        Generate an invoice number.

        Args:
            prefix: Invoice number prefix.

        Returns:
            Invoice number string.
        """
        sm = self._get_sm()
        today = date.today()
        year_month = today.strftime("%Y%m")
        seq = sm.random_int(1000, 9999)
        return f"{prefix}-{year_month}-{seq}"

    def company_name(self) -> str:
        """
        Generate a fake company name.

        Returns:
            Company name.
        """
        sm = self._get_sm()
        adjectives = [
            "Global", "Tech", "Smart", "Blue", "Green", "Red", "Golden", "Silver",
            "Prime", "Elite", "Advanced", "Modern", "Digital", "Cloud", "Data"
        ]
        nouns = [
            "Solutions", "Systems", "Services", "Technologies", "Innovations",
            "Dynamics", "Ventures", "Capital", "Resources", "Networks"
        ]

        pattern = sm.random_int(1, 3)
        if pattern == 1:
            return f"{sm.random_choice(adjectives)} {sm.random_choice(nouns)}"
        elif pattern == 2:
            return f"{sm.random_choice(LAST_NAMES)} {sm.random_choice(COMPANY_SUFFIXES)}"
        else:
            return f"{sm.random_choice(adjectives)} {sm.random_choice(nouns)} {sm.random_choice(COMPANY_SUFFIXES)}"

    def generate(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """
        Generate a complete financial profile.

        Returns:
            Dictionary with various financial data.
        """
        return {
            "credit_card": self.credit_card_full(),
            "iban": self.iban(),
            "swift": self.swift_bic(),
            "account_number": self.account_number(),
            "routing_number": self.routing_number(),
            "transaction": self.transaction(),
            "crypto_wallet": {
                "BTC": self.crypto_wallet_address("BTC"),
                "ETH": self.crypto_wallet_address("ETH"),
            },
            "company": self.company_name(),
            "invoice": self.invoice_number(),
        }
