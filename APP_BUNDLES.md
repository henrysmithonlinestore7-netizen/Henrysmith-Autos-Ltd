# Henrysmith Autos Ltd - Business Banking System
## APP Bundles Documentation

---

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture & Components](#architecture--components)
3. [Core Data Models](#core-data-models)
4. [Feature Bundles](#feature-bundles)
5. [API Endpoints Summary](#api-endpoints-summary)
6. [Configuration & Setup](#configuration--setup)
7. [Security Considerations](#security-considerations)

---

## 🎯 Project Overview

**Project Name:** Henrysmith Autos Ltd - Business Banking Platform
**Purpose:** Complete digital banking solution for Henrysmith Autos Ltd business account management
**Business Type:** Business Banking System
**Target User:** Henrysmith Autos Ltd (CAR BUSINESS)
**Key Features:** Account management, transfers, card issuance, transaction tracking

### Business Profile
- **Business Name:** HENRYSMITH AUTOS LTD
- **RC Number:** 7244864
- **TIN:** 78268428546
- **Industry:** Car Businesses
- **Address:** Iwaro Street, Ado, Ekiti, Nigeria
- **Phone:** 08100987752
- **Email:** ibitoyeakinsola8@gmail.com
- **Date Registered:** 11/30/2023
- **Account Number:** 170620261123596
- **Currency:** Nigerian Naira (NGN)
- **Account Type:** Business Account

---

## 🏗️ Architecture & Components

### System Architecture Layers

```
┌─────────────────────────────────────────────────┐
│         Web Interface (HTML Dashboard)           │
├─────────────────────────────────────────────────┤
│       HenrysmithBankingSystem (Core Logic)       │
├─────────────────────────────────────────────────┤
│  Data Models | Enums | Validators | Generators  │
├─────────────────────────────────────────────────┤
│   JSON Data Persistence | File Management       │
└─────────────────────────────────────────────────┘
```

### Key Components

| Component | Purpose | Type |
|-----------|---------|------|
| **Transaction Types** | Define transaction categories | Enum |
| **Transaction Status** | Track transaction states | Enum |
| **Card Types** | Supported debit card brands | Enum |
| **Card Status** | Card activation/blocking states | Enum |
| **Address** | Business location details | Data Model |
| **BusinessProfile** | Company information & metadata | Data Model |
| **Account** | Main business bank account | Data Model |
| **Transaction** | Financial transaction record | Data Model |
| **DebitCard** | Merchant debit card details | Data Model |
| **Beneficiary** | Saved transfer recipients | Data Model |

---

## 💾 Core Data Models

### 1. **Transaction Types Enum**
```
• CREDIT - Account funding/incoming transfers
• DEBIT - Withdrawals/outgoing payments
• TRANSFER - Inter-bank transfers
• CARD_PAYMENT - Debit card transactions
• AIRTIME - Mobile airtime purchases
• BILL_PAYMENT - Utility/service bill payments
```

### 2. **Transaction Status Enum**
```
• PENDING - Transaction in progress
• SUCCESS - Completed successfully
• FAILED - Transaction declined
• REVERSED - Previously completed transaction cancelled
```

### 3. **Card Types Enum**
```
• VERVE - Local Nigerian card
• MASTERCARD - International card
• VISA - International card
```

### 4. **Card Status Enum**
```
• ACTIVE - Card operational
• FROZEN - Temporarily blocked
• BLOCKED - Permanently blocked
• EXPIRED - Card validity expired
```

### 5. **Address Model**
```python
{
  street: "Iwaro Street",
  city: "Ado",
  state: "Ekiti",
  country: "Nigeria"
}
```

### 6. **BusinessProfile Model**
```python
{
  business_name: "HENRYSMITH AUTOS LTD",
  rc_number: "7244864",
  tin: "78268428546",
  industry: "Car Businesses",
  address: Address,
  phone: "08100987752",
  email: "ibitoyeakinsola8@gmail.com",
  date_registered: "2023/11/30"
}
```

### 7. **Account Model**
```python
{
  account_number: "170620261123596",
  account_name: "HENRYSMITH AUTOS LTD",
  balance: 1,800,000,000.00,
  currency: "NGN",
  account_type: "BUSINESS ACCOUNT",
  bvn: "22465113277",
  status: "ACTIVE",
  daily_limit: 100,000,000.00,
  created_at: ISO 8601 timestamp
}
```

### 8. **Transaction Model**
```python
{
  transaction_id: UUID,
  account_number: "170620261123596",
  type: TransactionType,
  amount: float,
  currency: "NGN",
  description: str,
  status: TransactionStatus,
  reference: str,
  beneficiary_account: optional str,
  beneficiary_name: optional str,
  card_last4: optional str,
  timestamp: ISO 8601,
  fee: float (default 0.0)
}
```

### 9. **DebitCard Model**
```python
{
  card_id: UUID,
  account_number: "170620261123596",
  card_number: "5424374324626378",
  card_type: "Mastercard",
  expiry_year: 2050,
  expiry_month: 12,
  cvv: "643" (hashed),
  pin_hash: "2828" (hashed),
  cardholder_name: "HENRYSMITH AUTOS LTD",
  status: "ACTIVE",
  daily_limit: 50,000,000.00,
  pos_limit: 5,000,000.00,
  web_limit: 10,000,000.00,
  issued_at: ISO 8601
}
```

### 10. **Beneficiary Model**
```python
{
  beneficiary_id: UUID,
  account_number: str,
  account_name: str,
  bank_code: str,
  added_at: ISO 8601
}
```

---

## 📦 Feature Bundles

### Bundle 1: **Core Banking Setup**
**Status:** ✅ Implemented
**Components:**
- Data model initialization
- Enum definitions
- JSON data persistence
- Database file management

**Key Functions:**
- `__init__()` - Initialize banking system
- `ensure_data_dir()` - Setup data storage
- `save_data()` - Persist data to JSON

---

### Bundle 2: **Business Onboarding**
**Status:** ✅ Implemented
**Components:**
- Business profile registration
- NUBAN account generation
- Business validation
- Account creation

**Key Functions:**
- `onboard_business()` - Register business with account
- **Inputs:** business_name, rc_number, tin, industry, address, contact info
- **Outputs:** Account number, bank details, profile confirmation

**NUBAN Generator:**
- Algorithm: CBN standard 10-digit account number
- Validation: Bank code (3 digits) + Serial (9 digits)
- Checksum: Modulo 10 verification

---

### Bundle 3: **Account Management**
**Status:** ✅ Implemented
**Components:**
- Account retrieval
- Balance checking
- Account crediting
- Transaction history

**Key Functions:**
- `get_account(account_number)` - Retrieve account details
- `get_balance(account_number)` - Check current balance
- `credit_account(account_number, amount, description, reference)` - Fund account
- `get_statement(account_number, start_date, end_date)` - Account statement

**Balance Details Returned:**
- Current balance
- Available balance
- Ledger balance
- Currency (NGN)

---

### Bundle 4: **Bank Transfer (NIP System)**
**Status:** ✅ Implemented
**Components:**
- Inter-bank transfer execution
- Destination account validation
- Beneficiary management
- Transfer fee processing

**Key Functions:**
- `validate_bank_account(account_number, bank_code)` - Name enquiry
- `add_beneficiary(account_number, account_name, bank_name, bank_code)` - Save recipient
- `get_beneficiaries()` - List saved beneficiaries
- `transfer(from_account, to_account, to_bank_code, amount, narration, pin)` - Execute transfer

**Supported Banks:** 25+ Nigerian banks
- Access Bank (044)
- First Bank (011)
- GTBank (058)
- Zenith Bank (057)
- UBA (033)
- Virtual Banks: Kuda, Paycom (OPay), PalmPay, Moniepoint

**Transfer Fees:**
- Flat fee: ₦50.00 per transfer
- Daily limit: ₦100,000,000.00

---

### Bundle 5: **Debit Card Management**
**Status:** ✅ Implemented
**Components:**
- Card issuance
- Card number generation
- Card PIN hashing
- Card status management
- Transaction limits per channel

**Key Functions:**
- `issue_debit_card(account_number, card_type, cardholder_name, pin)` - Create card
- `get_cards(account_number)` - List account cards
- `card_payment(card_id, amount, merchant, pin, channel)` - Process payment
- `freeze_card(card_id)` - Temporarily block card
- `block_card(card_id)` - Permanently block card

**Card Specifications:**
- Types: Verve, Mastercard, Visa
- Validity: 3 years
- Daily Limit: ₦5,000,000.00
- POS Limit: ₦500,000.00
- Web Limit: ₦1,000,000.00
- Card Maintenance Fee: ₦1,000.00 annually

**Payment Channels:**
- POS (Point of Sale)
- Web (Online)
- ATM

---

### Bundle 6: **Security & Utilities**
**Status:** ✅ Implemented
**Components:**
- PIN hashing (SHA-256)
- ID generation (UUID-based)
- Card masking
- Reference generation

**Key Functions:**
- `hash_pin(pin)` - Secure PIN storage
- `generate_id()` - Create unique identifiers
- `generate_reference()` - Transaction reference codes
- `mask_card(card_number)` - Hide sensitive data (XXXX XXXX XXXX 1234)

**Security Features:**
- SHA-256 hashing for PINs
- Masked card numbers in responses
- UUID-based transaction IDs
- Transaction reference tracking

---

### Bundle 7: **Transaction Reporting**
**Status:** ✅ Implemented
**Components:**
- Transaction filtering
- Account statement generation
- Date range filtering
- Transaction sorting

**Key Functions:**
- `get_statement(account_number, start_date, end_date)` - Generate statement

**Statement Includes:**
- Account number & name
- Period (date range)
- Opening balance
- Closing balance
- Sorted transaction list
- Timestamps for all transactions

---

### Bundle 8: **Web Dashboard Interface**
**Status:** ✅ Implemented
**Components:**
- Responsive HTML dashboard
- CSS styling (custom CSS variables)
- Business profile display
- Account overview
- Card management UI
- Transaction history table
- Transfer forms
- Beneficiary management

**Key Functions:**
- `generate_html_dashboard()` - Render web interface

**Dashboard Sections:**
1. **Navigation Bar** - Logo & menu links
2. **Sidebar** - Navigation items
3. **Stats Grid** - Key metrics
   - Account balance
   - Daily limit
   - Card count
   - Recent transactions
4. **Account Details** - Full account information
5. **Debit Card Visual** - Card display with chip graphic
6. **Card Management** - List & manage cards
7. **Beneficiaries** - Saved transfer recipients
8. **Transaction History** - Recent 10 transactions
9. **Forms** - Transfer, card payment, beneficiary forms
10. **Bank Selection** - Grid of supported banks

**UI Features:**
- Responsive grid layout
- Color-coded status badges
- Interactive forms
- Masked sensitive data
- Professional styling
- Mobile-friendly design

**Color Scheme:**
- Primary: #1a3a5c (Navy Blue)
- Secondary: #d4af37 (Gold)
- Success: #27ae60 (Green)
- Danger/Alert: #e74c3c (Red)
- Background: #f4f6f8 (Light Gray)

---

## 🔌 API Endpoints Summary

### Business Management
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `onboard_business()` | POST | Register new business |

### Account Operations
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `get_account()` | GET | Retrieve account details |
| `get_balance()` | GET | Check account balance |
| `credit_account()` | POST | Fund account |
| `get_statement()` | GET | Account statement |

### Bank Transfers
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `validate_bank_account()` | GET | Verify recipient account |
| `add_beneficiary()` | POST | Save transfer recipient |
| `get_beneficiaries()` | GET | List beneficiaries |
| `transfer()` | POST | Execute NIP transfer |

### Debit Cards
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `issue_debit_card()` | POST | Create new card |
| `get_cards()` | GET | List account cards |
| `card_payment()` | POST | Process card transaction |
| `freeze_card()` | PUT | Temporary card block |
| `block_card()` | PUT | Permanent card block |

### Reporting
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `get_statement()` | GET | Financial statement |

### Web Interface
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `generate_html_dashboard()` | GET | Render web dashboard |

---

## ⚙️ Configuration & Setup

### System Configuration
```python
BUSINESS_NAME = "Henrysmith AUTOS LTD"
BANK_CODE = "999" (Virtual bank platform code)
TRANSFER_FEE = 50.00 (NGN)
CARD_MAINTENANCE_FEE = 1000.00 (NGN annually)
DATA_DIR = "/mnt/agents/Henrysmith_banking/"
```

### Account Defaults
```python
BUSINESS_ACCOUNT = {
  "account_number": "170620261123596",
  "balance": 1,800,000,000.00,
  "daily_limit": 100,000,000.00,
  "currency": "NGN"
}
```

### Card Limits
```python
DAILY_LIMIT = 5,000,000.00 (NGN)
POS_LIMIT = 500,000.00 (NGN)
WEB_LIMIT = 1,000,000.00 (NGN)
```

### Data Storage
- **Format:** JSON
- **Location:** `/mnt/agents/Henrysmith_banking/`
- **File Structure:**
  ```json
  {
    "business_profile": {...},
    "accounts": {...},
    "transactions": [...],
    "cards": [...],
    "beneficiaries": [...],
    "users": [...],
    "sessions": [...]
  }
  ```

---

## 🔐 Security Considerations

### Authentication & Authorization
- PIN-based verification for transactions
- SHA-256 hashing for sensitive data
- User session management
- Account-based access control

### Data Protection
- **Card Data:**
  - Full card numbers masked in responses
  - CVV hashed and never displayed
  - PIN hashed with salt prefix ("HENRY{PIN}SMITH")
  
- **Transaction Security:**
  - Unique transaction IDs (UUID)
  - Transaction reference tracking
  - Status verification before execution

### Transaction Validation
- Source account verification
- PIN validation
- Daily limit enforcement
- Insufficient funds checking
- Destination account validation

### Best Practices
1. Always hash sensitive data before storage
2. Mask card numbers in all responses (XXXX XXXX XXXX 1234)
3. Verify PIN against hashed value
4. Log all transactions with timestamps
5. Implement rate limiting on transfers
6. Add fraud detection for large amounts
7. Enable transaction alerts
8. Maintain audit trail for compliance

### Recommended Enhancements
- [ ] Implement OAuth 2.0 authentication
- [ ] Add two-factor authentication (2FA)
- [ ] Enable SSL/TLS encryption
- [ ] Implement API rate limiting
- [ ] Add transaction limits per time period
- [ ] Enable email/SMS notifications
- [ ] Add fraud detection algorithms
- [ ] Implement database encryption
- [ ] Enable backup & disaster recovery
- [ ] Add comprehensive audit logging

---

## 📊 Data Flow Diagrams

### Transfer Flow
```
User Request
    ↓
Validate Source Account
    ↓
Verify PIN
    ↓
Check Daily Limit
    ↓
Validate Destination
    ↓
Execute Debit
    ↓
Create Transaction Record
    ↓
Update Account Balance
    ↓
Save Data
    ↓
Return Confirmation
```

### Card Payment Flow
```
Card Payment Request
    ↓
Retrieve Card Details
    ↓
Validate PIN
    ↓
Check Channel Limit (POS/Web/ATM)
    ↓
Verify Account Balance
    ↓
Process Payment
    ↓
Deduct Amount
    ↓
Create Transaction
    ↓
Update Account
    ↓
Return Receipt
```

---

## 📝 File Structure

```
Henrysmith app Folder/
├── banking_system.py (Main implementation)
├── APP_BUNDLES.md (This file)
├── /data/
│   └── henrysmith_banking.json (Persistent storage)
├── /templates/
│   └── dashboard.html (Web interface)
└── /docs/
    ├── API_REFERENCE.md
    ├── SETUP_GUIDE.md
    └── TROUBLESHOOTING.md
```

---

## 🚀 Quick Start Guide

### 1. Initialize System
```python
banking = HenrysmithBankingSystem()
```

### 2. Onboard Business
```python
result = banking.onboard_business(
    business_name="HENRYSMITH AUTOS LTD",
    rc_number="7244864",
    tin="78268428546",
    industry="car businesses",
    street="Iwaro Street",
    city="Ado",
    state="Ekiti",
    phone="08100987752",
    email="ibitoyeakinsola8@gmail.com",
    bvn="22465113277"
)
```

### 3. Fund Account
```python
result = banking.credit_account(
    account_number="170620261123596",
    amount=1000000.00,
    description="Initial funding",
    reference="INV001"
)
```

### 4. Issue Debit Card
```python
result = banking.issue_debit_card(
    account_number="170620261123596",
    card_type="Mastercard",
    cardholder_name="HENRYSMITH AUTOS LTD",
    pin="1234"
)
```

### 5. Execute Transfer
```python
result = banking.transfer(
    from_account="170620261123596",
    to_account="1234567890",
    to_bank_code="058",
    amount=500000.00,
    narration="Payment for goods",
    pin="1234"
)
```

---

## 📞 Support & Contact

**Business Contact:**
- **Email:** ibitoyeakinsola8@gmail.com
- **Phone:** 08100987752
- **Address:** Iwaro Street, Ado, Ekiti, Nigeria

**System Support:**
- Report issues to: admin@henrysmith-autos.com
- Documentation: See /docs/ folder
- Emergency Contact: Available 24/7

---

## 📄 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2023-11-30 | Initial release |
| 1.1.0 | 2024-01-15 | Added web dashboard |
| 1.2.0 | 2024-03-20 | Enhanced security |
| 1.3.0 | 2026-08-05 | APP Bundles documentation |

---

**Document Generated:** 2026-08-05
**Last Updated:** 2026-08-05
**Status:** Active ✅

---

## 🎯 Next Steps

1. Review security considerations for production deployment
2. Implement missing security enhancements
3. Set up comprehensive logging
4. Configure backup systems
5. Create API documentation
6. Develop mobile application
7. Implement admin dashboard
8. Set up compliance reporting

---

*This APP Bundles document provides a complete overview of the Henrysmith Autos Ltd Banking System architecture, features, and implementation.*
