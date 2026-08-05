"""
Henrysmith Autos Ltd - Business Banking System
Complete banking platform for Henrysmith Autos Ltd
"""

import os
import json
import hashlib
import random
import string
import uuid
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Optional
from enum import Enum


# ============================================================================================
# CORE DATA MODELS & ENUMS
# ============================================================================================

class TransactionType(Enum):
    """Transaction type enumeration"""
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"
    TRANSFER = "TRANSFER"
    CARD_PAYMENT = "CARD_PAYMENT"
    AIRTIME = "AIRTIME"
    BILL_PAYMENT = "BILL_PAYMENT"


class TransactionStatus(Enum):
    """Transaction status enumeration"""
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REVERSED = "REVERSED"


class CardType(Enum):
    """Card type enumeration"""
    VERVE = "VERVE"
    MASTERCARD = "MASTERCARD"
    VISA = "VISA"


class CardStatus(Enum):
    """Card status enumeration"""
    ACTIVE = "ACTIVE"
    FROZEN = "FROZEN"
    BLOCKED = "BLOCKED"
    EXPIRED = "EXPIRED"


@dataclass
class Address:
    """Address data model"""
    street: str
    city: str
    state: str
    country: str = "Nigeria"


@dataclass
class BusinessProfile:
    """Business profile data model"""
    business_name: str
    rc_number: str
    tin: str
    industry: str
    address: Address
    phone: str
    email: str
    date_registered: str


@dataclass
class Account:
    """Account data model"""
    account_number: str
    account_name: str
    balance: float
    currency: str = "NGN"
    account_type: str = "BUSINESS"
    bvn: str = ""
    status: str = "ACTIVE"
    daily_limit: float = 100_000_000.00
    created_at: str = field(default="")

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


@dataclass
class Transaction:
    """Transaction data model"""
    transaction_id: str
    account_number: str
    type: str
    amount: float
    currency: str
    description: str
    status: str
    reference: str
    beneficiary_account: Optional[str] = None
    beneficiary_name: Optional[str] = None
    card_last4: Optional[str] = None
    timestamp: str = field(default="")
    fee: float = 0.0

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


@dataclass
class DebitCard:
    """Debit card data model"""
    card_id: str
    account_number: str
    card_number: str
    card_type: str
    expiry_year: int
    expiry_month: int
    cvv: str
    pin_hash: str
    cardholder_name: str
    status: str = "ACTIVE"
    daily_limit: float = 50_000_000.00
    pos_limit: float = 5_000_000.00
    web_limit: float = 10_000_000.00
    issued_at: str = field(default="")

    def __post_init__(self):
        if not self.issued_at:
            self.issued_at = datetime.now().isoformat()


@dataclass
class Beneficiary:
    """Beneficiary data model"""
    beneficiary_id: str
    account_number: str
    account_name: str
    bank_code: str
    added_at: str = field(default="")

    def __post_init__(self):
        if not self.added_at:
            self.added_at = datetime.now().isoformat()


# ============================================================================================
# NIGERIAN BANK CODES & NUBAN GENERATOR
# ============================================================================================

NIGERIAN_BANKS = {
    "044": "Access Bank",
    "023": "Citibank Nigeria",
    "050": "Ecobank Nigeria",
    "011": "First Bank of Nigeria",
    "214": "First City Monument Bank",
    "070": "Fidelity Bank",
    "058": "Guaranty Trust Bank",
    "030": "Heritage Bank",
    "301": "Jaiz Bank",
    "082": "Keystone Bank",
    "076": "Keystone Bank",
    "221": "Polaris Bank",
    "068": "Standard Chartered Bank",
    "232": "Sterling Bank",
    "100": "SunTrust Bank",
    "032": "Union Bank",
    "033": "United Bank for Africa",
    "215": "Unity Bank",
    "035": "Wema Bank",
    "057": "Zenith Bank",
    "559": "Coronation Merchant Bank",
    "501": "Paycom (Opay)",
    "999991": "Palmpay",
    "999992": "Kuda Bank",
    "999993": "Moniepoint",
}


class NUBANGenerator:
    """Nigeria Uniform Bank Account Number (NUBAN) Generator"""

    @staticmethod
    def generate(bank_code: str, serial: str) -> str:
        """
        Generate valid 10-digit NUBAN using CBN standard algorithm:
        1. bank_code (3 digits) + serial (9 digits) = 12 digits
        2. Multiply by weights: [3, 7, 3, 3, 7, 3, 3, 7, 3, 3, 7, 3]
        3. Sum products, mod 10
        4. Check digit = 10 - (sum % 10), if 10 then 0
        """
        if len(bank_code) != 3 or len(serial) != 9:
            raise ValueError("Bank code must be 3 digits, serial must be 9 digits")

        nuban_12 = bank_code + serial
        weights = [3, 7, 3, 3, 7, 3, 3, 7, 3, 3, 7, 3]

        total = sum(int(digit) * weight for digit, weight in zip(nuban_12, weights))
        check_digit = (10 - (total % 10)) % 10

        return serial + str(check_digit)

    @staticmethod
    def validate(account_number: str, bank_code: str) -> bool:
        """Validate account number against bank code"""
        if len(account_number) != 10 or len(bank_code) != 3:
            return False

        serial = account_number[:9]
        check = account_number[9]
        generated = NUBANGenerator.generate(bank_code, serial)
        return generated == account_number


# ============================================================================================
# HENRYSMITH AUTOS LTD - BUSINESS BANKING SYSTEM
# ============================================================================================

class HenrysmithBankingSystem:
    """Complete Business Banking platform for Henrysmith Autos Ltd"""

    def __init__(self, data_dir: str = "Henrysmith_banking"):
        """Initialize banking system"""
        self.business_name = "Henrysmith Autos Ltd"
        self.bank_code = "999"  # Virtual bank code
        self.transfer_fee = 50.00
        self.card_maintenance_fee = 1000.00
        
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        self.db_file = os.path.join(data_dir, "banking_data.json")
        self.data = self._ensure_data_dir()

    def _ensure_data_dir(self) -> Dict:
        """Load or initialize database"""
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                return json.load(f)
        
        return {
            "business_profile": None,
            "accounts": {},
            "transactions": [],
            "cards": {},
            "beneficiaries": [],
            "users": [],
            "sessions": []
        }

    def save_data(self):
        """Save data to JSON file"""
        with open(self.db_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def hash_pin(self, pin: str) -> str:
        """Hash PIN for security"""
        return hashlib.sha256(f"HENRY{pin}SMITH".encode()).hexdigest()[:16]

    def generate_id(self) -> str:
        """Generate unique transaction ID"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_suffix = random.randint(1000, 9999)
        return f"HSL{timestamp}{random_suffix}"

    def generate_reference(self) -> str:
        """Generate transaction reference"""
        return f"REF{uuid.uuid4().hex[:12].upper()}"

    def mask_card(self, card_number: str) -> str:
        """Mask card number for security"""
        return f"{card_number[:4]}****{card_number[-4:]}"

    # ============================================================================================
    # BUSINESS ONBOARDING
    # ============================================================================================

    def onboard_business(
        self,
        business_name: str,
        rc_number: str,
        tin: str,
        industry: str,
        street: str,
        city: str,
        state: str,
        phone: str,
        email: str,
        bvn: str
    ) -> Dict:
        """Onboard a business and create account"""
        
        # Create business profile
        address = Address(street=street, city=city, state=state)
        profile = BusinessProfile(
            business_name=business_name,
            rc_number=rc_number,
            tin=tin,
            industry=industry,
            address=address,
            phone=phone,
            email=email,
            date_registered=datetime.now().strftime("%Y-%m-%d")
        )

        # Generate NUBAN account
        serial = "".join(random.choices(string.digits, k=9))
        account_number = NUBANGenerator.generate(self.bank_code, serial)

        # Create account
        account = Account(
            account_number=account_number,
            account_name=business_name.upper(),
            balance=0.00,
            bvn=bvn,
            daily_limit=50_000_000.00
        )

        # Save to database
        self.data["business_profile"] = asdict(profile)
        self.data["accounts"][account_number] = asdict(account)
        self.save_data()

        return {
            "status": "success",
            "message": f"Welcome {business_name}! Your business account has been created.",
            "account_number": account_number,
            "bank_name": "Henrysmith Autos Bank",
            "profile": asdict(profile)
        }

    # ============================================================================================
    # ACCOUNT MANAGEMENT
    # ============================================================================================

    def get_account(self, account_number: str) -> Optional[Dict]:
        """Retrieve account details"""
        return self.data["accounts"].get(account_number)

    def get_balance(self, account_number: str) -> Dict:
        """Get account balance"""
        account = self.get_account(account_number)

        if not account:
            return {"status": "error", "message": "Account not found"}

        return {
            "status": "success",
            "account_number": account_number,
            "account_name": account["account_name"],
            "balance": account["balance"],
            "currency": account["currency"],
            "available_balance": account["balance"],
            "ledger_balance": account["balance"]
        }

    def credit_account(
        self,
        account_number: str,
        amount: float,
        description: str,
        reference: str = ""
    ) -> Dict:
        """Credit an account (funding, incoming transfer)"""
        account = self.get_account(account_number)
        
        if not account:
            return {"status": "error", "message": "Account not found"}

        if amount <= 0:
            return {"status": "error", "message": "Invalid amount"}

        account["balance"] += amount

        txn = Transaction(
            transaction_id=self.generate_id(),
            account_number=account_number,
            type=TransactionType.CREDIT.value,
            amount=amount,
            currency="NGN",
            description=description,
            status=TransactionStatus.SUCCESS.value,
            reference=reference or self.generate_reference()
        )

        self.data["transactions"].append(asdict(txn))
        self.data["accounts"][account_number] = account
        self.save_data()

        return {
            "status": "success",
            "message": f"₦{amount:,.2f} credited successfully",
            "new_balance": account["balance"],
            "transaction": asdict(txn)
        }

    def debit_account(
        self,
        account_number: str,
        amount: float,
        description: str,
        reference: str = ""
    ) -> Dict:
        """Debit an account (withdrawal, outgoing transfer)"""
        account = self.get_account(account_number)
        
        if not account:
            return {"status": "error", "message": "Account not found"}

        if amount <= 0:
            return {"status": "error", "message": "Invalid amount"}

        if account["balance"] < amount:
            return {"status": "error", "message": "Insufficient funds"}

        account["balance"] -= amount

        txn = Transaction(
            transaction_id=self.generate_id(),
            account_number=account_number,
            type=TransactionType.DEBIT.value,
            amount=amount,
            currency="NGN",
            description=description,
            status=TransactionStatus.SUCCESS.value,
            reference=reference or self.generate_reference()
        )

        self.data["transactions"].append(asdict(txn))
        self.data["accounts"][account_number] = account
        self.save_data()

        return {
            "status": "success",
            "message": f"₦{amount:,.2f} debited successfully",
            "new_balance": account["balance"],
            "transaction": asdict(txn)
        }

    # ============================================================================================
    # BANK TRANSFER (NIP - Nigeria Inter-Bank Settlement System)
    # ============================================================================================

    def validate_bank_account(self, account_number: str, bank_code: str) -> Dict:
        """Validate destination account (simulated name enquiry)"""
        if bank_code not in NIGERIAN_BANKS:
            return {"status": "error", "message": "Invalid bank code"}

        if len(account_number) != 10:
            return {"status": "error", "message": "Invalid account number"}

        # Simulated name enquiry (in production, call NIBSS API)
        bank_name = NIGERIAN_BANKS[bank_code]
        simulated_name = f"Customer-{bank_name[:4].upper()}{account_number[-4:]}"

        return {
            "status": "success",
            "account_number": account_number,
            "account_name": simulated_name,
            "bank_code": bank_code,
            "bank_name": bank_name,
            "valid": True
        }

    def add_beneficiary(
        self,
        account_number: str,
        beneficiary_account: str,
        beneficiary_name: str,
        bank_code: str
    ) -> Dict:
        """Save frequent transfer beneficiaries"""
        if bank_code not in NIGERIAN_BANKS:
            return {"status": "error", "message": "Invalid bank code"}

        validation = self.validate_bank_account(beneficiary_account, bank_code)
        if validation["status"] == "error":
            return validation

        beneficiary = Beneficiary(
            beneficiary_id=self.generate_id(),
            account_number=beneficiary_account,
            account_name=beneficiary_name,
            bank_code=bank_code
        )

        self.data["beneficiaries"].append(asdict(beneficiary))
        self.save_data()

        return {
            "status": "success",
            "message": "Beneficiary added successfully",
            "beneficiary": asdict(beneficiary)
        }

    def get_beneficiaries(self) -> List[Dict]:
        """Get all beneficiaries"""
        return self.data["beneficiaries"]

    def transfer(
        self,
        from_account: str,
        to_account: str,
        to_bank_code: str,
        amount: float,
        narration: str,
        pin: str
    ) -> Dict:
        """Execute NIP transfer to any Nigerian bank"""
        
        # Validate source account
        source = self.get_account(from_account)
        if not source:
            return {"status": "error", "message": "Source account not found"}

        # Check limits
        if amount > source["daily_limit"]:
            return {
                "status": "error",
                "message": f"Amount exceeds daily limit of ₦{source['daily_limit']:,.2f}"
            }

        total_debit = amount + self.transfer_fee

        if source["balance"] < total_debit:
            return {
                "status": "error",
                "message": "Insufficient funds (including ₦50 fee)"
            }

        # Validate destination
        dest_validation = self.validate_bank_account(to_account, to_bank_code)
        if dest_validation["status"] == "error":
            return dest_validation

        # Execute transfer
        source["balance"] -= total_debit

        # Create debit transaction
        debit_txn = Transaction(
            transaction_id=self.generate_id(),
            account_number=from_account,
            type=TransactionType.TRANSFER.value,
            amount=amount,
            currency="NGN",
            description=narration,
            status=TransactionStatus.SUCCESS.value,
            reference=self.generate_reference(),
            beneficiary_account=to_account,
            beneficiary_name=dest_validation["account_name"],
            fee=self.transfer_fee
        )

        self.data["transactions"].append(asdict(debit_txn))
        self.data["accounts"][from_account] = source
        self.save_data()

        return {
            "status": "success",
            "message": f"₦{amount:,.2f} transferred to {dest_validation['account_name']}",
            "reference": debit_txn.reference,
            "fee": self.transfer_fee,
            "new_balance": source["balance"],
            "transaction": asdict(debit_txn)
        }

    # ============================================================================================
    # MERCHANT DEBIT CARD MANAGEMENT
    # ============================================================================================

    def _generate_card_number(self, card_type: str) -> str:
        """Generate card number based on type"""
        prefixes = {
            "VERVE": "5061",
            "MASTERCARD": "5424",
            "VISA": "4353"
        }
        prefix = prefixes.get(card_type, "5061")
        remaining = "".join(random.choices(string.digits, k=12))
        return prefix + remaining

    def issue_debit_card(
        self,
        account_number: str,
        card_type: str,
        cardholder_name: str,
        pin: str
    ) -> Dict:
        """Issue a new merchant debit card linked to business account"""
        
        account = self.get_account(account_number)
        if not account:
            return {"status": "error", "message": "Account not found"}

        valid_types = [ct.value for ct in CardType]
        if card_type not in valid_types:
            return {
                "status": "error",
                "message": f"Invalid card type. Choose from: {', '.join(valid_types)}"
            }

        # Generate card details
        card_number = self._generate_card_number(card_type)
        expiry = datetime.now() + timedelta(days=3*365)  # 3 years

        card = DebitCard(
            card_id=self.generate_id(),
            account_number=account_number,
            card_number=card_number,
            card_type=card_type,
            expiry_month=expiry.month,
            expiry_year=expiry.year,
            cvv=self.hash_pin(pin)[:3],
            pin_hash=self.hash_pin(pin),
            cardholder_name=cardholder_name.upper(),
            daily_limit=5_000_000.00,
            pos_limit=500_000.00,
            web_limit=1_000_000.00
        )

        self.data["cards"][card.card_id] = asdict(card)
        self.save_data()

        return {
            "status": "success",
            "message": f"{card_type} card issued successfully",
            "card_id": card.card_id,
            "card_number": self.mask_card(card_number),
            "expiry": f"{card.expiry_month:02d}/{card.expiry_year}",
            "cardholder": card.cardholder_name,
            "limits": {
                "daily": card.daily_limit,
                "pos": card.pos_limit,
                "web": card.web_limit
            }
        }

    def get_cards(self, account_number: str) -> List[Dict]:
        """Get all cards linked to an account"""
        cards = [
            c for c in self.data["cards"].values()
            if c["account_number"] == account_number
        ]

        # Mask sensitive data
        for card in cards:
            card["card_number"] = self.mask_card(card["card_number"])
            card["cvv"] = "***"
            card["pin_hash"] = "****"

        return cards

    def card_payment(
        self,
        card_id: str,
        amount: float,
        merchant: str,
        pin: str,
        channel: str = "pos"
    ) -> Dict:
        """Process card payment (POS, Web, ATM)"""
        
        card = self.data["cards"].get(card_id)
        if not card:
            return {"status": "error", "message": "Invalid card"}

        # Check channel limits
        limits = {
            "pos": card["pos_limit"],
            "web": card["web_limit"],
            "atm": card["daily_limit"]
        }

        if amount > limits.get(channel, card["daily_limit"]):
            return {
                "status": "error",
                "message": f"Exceeds {channel.upper()} limit"
            }

        # Check account balance
        account = self.get_account(card["account_number"])
        if account["balance"] < amount:
            return {"status": "error", "message": "Insufficient funds"}

        # Process payment
        account["balance"] -= amount

        txn = Transaction(
            transaction_id=self.generate_id(),
            account_number=card["account_number"],
            type=TransactionType.CARD_PAYMENT.value,
            amount=amount,
            currency="NGN",
            description=f"Card payment to {merchant} via {channel.upper()}",
            status=TransactionStatus.SUCCESS.value,
            reference=self.generate_reference(),
            card_last4=card["card_number"][-4:]
        )

        self.data["transactions"].append(asdict(txn))
        self.data["accounts"][card["account_number"]] = account
        self.save_data()

        return {
            "status": "success",
            "message": f"₦{amount:,.2f} payment processed successfully",
            "reference": txn.reference,
            "new_balance": account["balance"],
            "transaction": asdict(txn)
        }

    def freeze_card(self, card_id: str) -> Dict:
        """Temporarily freeze card"""
        if card_id not in self.data["cards"]:
            return {"status": "error", "message": "Card not found"}

        self.data["cards"][card_id]["status"] = CardStatus.FROZEN.value
        self.save_data()

        return {"status": "success", "message": "Card frozen successfully"}

    def block_card(self, card_id: str) -> Dict:
        """Permanently block card"""
        if card_id not in self.data["cards"]:
            return {"status": "error", "message": "Card not found"}

        self.data["cards"][card_id]["status"] = CardStatus.BLOCKED.value
        self.save_data()

        return {"status": "success", "message": "Card blocked successfully"}

    # ============================================================================================
    # TRANSACTION HISTORY & REPORTING
    # ============================================================================================

    def get_statement(
        self,
        account_number: str,
        start_date: str,
        end_date: str
    ) -> Dict:
        """Generate account statement"""
        
        txns = [
            t for t in self.data["transactions"]
            if t["account_number"] == account_number
            and start_date <= t["timestamp"][:10] <= end_date
        ]

        account = self.get_account(account_number)

        if not account:
            return {"status": "error", "message": "Account not found"}

        return {
            "status": "success",
            "account_number": account_number,
            "account_name": account["account_name"],
            "period": f"{start_date} to {end_date}",
            "opening_balance": 0.00,
            "closing_balance": account["balance"],
            "total_transactions": len(txns),
            "transactions": sorted(txns, key=lambda x: x["timestamp"])
        }

    def get_transactions(
        self,
        account_number: str,
        limit: int = 10
    ) -> List[Dict]:
        """Get recent transactions"""
        txns = [
            t for t in self.data["transactions"]
            if t["account_number"] == account_number
        ]
        return sorted(txns, key=lambda x: x["timestamp"], reverse=True)[:limit]


# ============================================================================================
# MAIN EXECUTION
# ============================================================================================

if __name__ == "__main__":
    # Initialize banking system
    banking_system = HenrysmithBankingSystem()

    # Example: Onboard business
    result = banking_system.onboard_business(
        business_name="Henrysmith Autos Ltd",
        rc_number="7244864",
        tin="78268428546",
        industry="Car Business",
        street="Iwaro Street",
        city="Ado",
        state="Ekiti",
        phone="08100987752",
        email="ibitoyeakinsola8@gmail.com",
        bvn="22465113277"
    )

    print("Onboarding Result:", json.dumps(result, indent=2))

    if result["status"] == "success":
        account_number = result["account_number"]

        # Credit account
        credit_result = banking_system.credit_account(
            account_number=account_number,
            amount=1_800_000_000.00,
            description="Initial business funding"
        )
        print("\nCredit Result:", json.dumps(credit_result, indent=2))

        # Issue debit card
        card_result = banking_system.issue_debit_card(
            account_number=account_number,
            card_type="MASTERCARD",
            cardholder_name="Henrysmith Autos Ltd",
            pin="1234"
        )
        print("\nCard Issue Result:", json.dumps(card_result, indent=2))

        # Get balance
        balance_result = banking_system.get_balance(account_number)
        print("\nBalance Result:", json.dumps(balance_result, indent=2))
