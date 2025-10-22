# How to Upgrade Ngrok (Remove Warning Page)

## Why Upgrade?

The **ngrok free tier shows an interstitial warning page** to first-time visitors. This breaks AgentBeats registration because their backend gets HTML instead of JSON.

**Paid plans remove this warning page** and provide additional benefits.

---

## Ngrok Pricing Plans

### 1. **Free Plan** (Current)
- ✅ 1 online ngrok process
- ✅ 4 tunnels/ngrok process
- ❌ **Interstitial warning page** (this is the problem!)
- ❌ No custom domains
- Price: **$0/month**

### 2. **Personal Plan** (Recommended)
- ✅ **No warning page** ⭐
- ✅ 3 online ngrok processes
- ✅ 10 tunnels/process
- ✅ Custom domains (1 included)
- ✅ Reserved subdomains (3)
- ✅ Basic authentication
- Price: **$8/month** or **$96/year** (save $0)

### 3. **Pro Plan**
- ✅ Everything in Personal
- ✅ 5 online ngrok processes
- ✅ More custom domains (3)
- ✅ IP allowlisting
- ✅ TCP/TLS tunnels
- Price: **$20/month** or **$240/year**

### 4. **Enterprise Plan**
- ✅ Custom pricing
- ✅ Unlimited everything
- ✅ SLA guarantees
- Price: **Contact sales**

---

## How to Upgrade

### Step 1: Go to Ngrok Dashboard
1. Visit: https://dashboard.ngrok.com/
2. Log in with your account

### Step 2: Navigate to Billing
1. Click on your profile (top right)
2. Select **"Billing"** or **"Upgrade"**
3. Or go directly to: https://dashboard.ngrok.com/billing/subscription

### Step 3: Choose Plan
1. Select **"Personal"** plan ($8/month)
2. Click **"Subscribe"** or **"Upgrade"**

### Step 4: Enter Payment Information
1. Enter credit card details
2. Confirm billing information
3. Complete purchase

### Step 5: Restart Ngrok
After upgrading, restart your tunnel:
```bash
# Kill current ngrok
pkill ngrok

# Start new tunnel (warning page will be gone)
ngrok http 8080
```

---

## Quick Upgrade Steps (Command Line)

```bash
# 1. Open ngrok dashboard in browser
open https://dashboard.ngrok.com/billing/subscription

# 2. After upgrading, restart ngrok
pkill ngrok
ngrok http 8080

# 3. Get new URL
curl -s http://localhost:4040/api/tunnels | python3 -c "import sys, json; data = json.load(sys.stdin); print(data['tunnels'][0]['public_url'] if data.get('tunnels') else 'No tunnels')"

# 4. Test (no bypass header needed anymore!)
curl https://YOUR-NEW-URL/health
```

---

## Alternative: Use Custom Domain (Included in Personal Plan)

With Personal plan, you get 1 custom domain:

### Option A: Use Your Own Domain
1. Buy a domain from Namecheap, GoDaddy, etc. (~$10-15/year)
2. In ngrok dashboard, add custom domain
3. Update DNS records (CNAME)
4. Start tunnel: `ngrok http --domain=youragent.yourdomain.com 8080`

### Option B: Use Ngrok Reserved Domain
1. In ngrok dashboard, reserve a subdomain (e.g., `theagentcompany.ngrok.app`)
2. Start tunnel: `ngrok http --domain=theagentcompany.ngrok.app 8080`
3. URL stays consistent: `https://theagentcompany.ngrok.app`

---

## Cost Comparison

| Solution | Monthly Cost | Setup Time | Reliability |
|----------|-------------|------------|-------------|
| **Ngrok Free** | $0 | ✅ 5 min | ⚠️ Warning page issue |
| **Ngrok Personal** | $8 | ✅ 5 min | ✅ No warning page |
| **AWS EC2** | ~$0-5 | ⚠️ 30 min | ✅ Professional setup |
| **AWS + Domain + SSL** | ~$15-20 | ⚠️ 1-2 hours | ✅✅ Production-ready |

---

## Recommendation

### For Quick Testing/Demo
**Upgrade to Ngrok Personal ($8/month)**
- Fastest solution
- No warning page
- Cancel anytime
- Good for temporary/testing

### For Production/Long-term
**Use AWS EC2 (Already Deployed!)**
- You already have it running at `http://50.18.84.152:8080`
- Free tier eligible (12 months)
- More professional
- No monthly fees after free tier

---

## What to Do Right Now

### Option 1: Upgrade Ngrok (5 minutes)
```bash
# 1. Go to ngrok billing page
open https://dashboard.ngrok.com/billing/subscription

# 2. Select Personal plan ($8/month)
# 3. Enter payment info
# 4. Restart ngrok after upgrade
```

### Option 2: Use AWS EC2 (Already Working!)
```bash
# Your agent is already deployed and working:
# URL: http://50.18.84.152:8080

# Test it:
curl http://50.18.84.152:8080/health

# Register with AgentBeats using this URL
```

---

## After Upgrading Ngrok

Once you upgrade, the warning page disappears:

```bash
# Test without bypass header (this will now work!)
curl https://ruby-nondoctrinaire-cohen.ngrok-free.dev/health

# Register with AgentBeats:
# agent_url: https://ruby-nondoctrinaire-cohen.ngrok-free.dev
# launcher_url: https://ruby-nondoctrinaire-cohen.ngrok-free.dev
# is_green: ✓
```

---

## Links

- **Ngrok Pricing**: https://ngrok.com/pricing
- **Ngrok Dashboard**: https://dashboard.ngrok.com/
- **Ngrok Billing**: https://dashboard.ngrok.com/billing/subscription
- **Ngrok Docs**: https://ngrok.com/docs

---

## My Recommendation

**For this project: Use AWS EC2** (http://50.18.84.152:8080)
- ✅ Already deployed and working
- ✅ No monthly costs (free tier)
- ✅ No warning page issues
- ✅ More professional for registration
- ✅ Permanent URL

**Only upgrade ngrok if**:
- You need HTTPS immediately and don't want to set up SSL on EC2
- You're doing a quick demo/test
- You want the convenience of ngrok's automatic SSL

The EC2 solution you already have is actually better for long-term use!
