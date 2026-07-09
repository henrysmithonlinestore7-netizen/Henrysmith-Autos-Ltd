// Original text (exactly as provided).
const originalText = `var{-- card-bg}: border-radius:12px: pasddind:1.5rem: box-shadow:0 2px 10 pxrgba(0,0,0,0.05): ]] .section-header[[ displays:flex: justify_content:spaces-between align items: [...]
>div class= "nav-links"> Dashboard">dashboard Transfer < href="//cards">Historya>
dashboard
send money
Airtime & BILLS
statements
settings
security
div class="stat-label">Account Balance
{'{:,>2f}'.format(list(accounts values()[0['balance']if accounts else 0)}
div>
class="stat-card">
Total cards
{:,.2f}'.format(sum(t['amount'] for t in recent_txns if t["type']=='debit'))
Account information
copy
Details
Account name
div style="font-weight:600:margin-top:0.25rem:">{profile.get(business_name' 'Henrysmith Autos ltd')}
div style="font-weight:600: margin-top 0.25rem:">{list(accounts.key(){0} if account else 'N/A'}
>div style="color: // 7f8c8d: font-size: 0.875rem: ">Account type>Business current
> div style=" font-weight:600 margin-top:0.25rem:">business current
select Bank 
{name}>/option>'for code, name in NIGERIAN_BANKS. items())}
class="form-group"> Amount (N) 
0.00></div>   <div class =
 Narration 
 whats this for?> <div><div class=
 pin 
****
 send money
div class="section_header">
merchant debit cards
+ request nnew card {''.join(f''' class= card-visual">
self.mas_card(card_number']}
card holder
div>
{c['cardholder_name']}
expires
{c['expiry-month'_year']}
Type
{c['card_type']}
''' for c in 1ist(cards.values()) [:2] if cards eles '
'}
classs= "section -header">
Transation
875rem:"View ALL>/a> th> Amount {''.join(f''' ltd> {'status,}.title()}span/td ''' for t in reversed(recent_txns)) if recent_txns else 'td colspan "5" style= " text- align: center:color: // 7f8cd8d:"No[...]
date\tdescription
{t['timestamp'][;10]}\t{t['description']}\t{t['type'].replace('_', ' ') .title()}\t
Supported Banks
div class="banks-grid"> {'.join (f
{name}
div>'for code, name in list (NIGERIANS,ITEM()) [:12])}
class="footer"> <@2026 HENRYSMITRH AUTOS LTD. ALL rights reserved./ LIcences by CENTRAL BANK OF NIGERIA /NDIC INSURED
cp style="margin-top: 0.5rem:">securedby 256_bit ssl encryption/p> """ html_path=os.path.join(self.data_dir,dashboard.html") with open (html_path,'w', encoldindings='utf-8')as f: f.write(html-content)[...]
`;

// Load the original text into the <pre> element
const pre = document.getElementById('original');
if (pre) {
  pre.textContent = originalText;
}

// Download original text as .txt when button clicked
const downloadBtn = document.getElementById('downloadTxt');
if (downloadBtn) {
  downloadBtn.addEventListener('click', () => {
    const blob = new Blob([originalText], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'HenrySmith_autos_Ltd.txt';
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  });
}

// Copy to clipboard
const copyBtn = document.getElementById('copyBtn');
if (copyBtn) {
  copyBtn.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(originalText);
      const originalText_btn = copyBtn.textContent;
      copyBtn.textContent = 'Copied!';
      setTimeout(() => {
        copyBtn.textContent = originalText_btn;
      }, 1400);
    } catch (e) {
      alert('Copy failed: ' + e.message);
    }
  });
}

// Open raw text in a new tab
const openRawBtn = document.getElementById('openRaw');
if (openRawBtn) {
  openRawBtn.addEventListener('click', () => {
    const blob = new Blob([originalText], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    window.open(url, '_blank');
    setTimeout(() => {
      URL.revokeObjectURL(url);
    }, 1000 * 10);
  });
}