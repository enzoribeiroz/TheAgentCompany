# 🎯 AWS Setup - What YOU Do & What I Need

## PART 1: What YOU Do on AWS Portal (10 minutes)

### Step 1: Go to AWS EC2 Console

1. **Open this link**: https://console.aws.amazon.com/ec2/
   - Login with your AWS account (or create one if needed)
   - If new account, you'll get 12 months free tier! 🎉

### Step 2: Click "Launch Instance"

Look for the orange button that says **"Launch Instance"**

### Step 3: Fill in the Configuration

#### Basic Details:
```
Name: agentbeats-agent
Tags: (leave default)
```

#### Choose Operating System:
```
✅ Select: "Ubuntu Server 22.04 LTS (HVM), SSD Volume Type"
   - Make sure it says "Free tier eligible"
   - Architecture: 64-bit (x86)
```

#### Choose Instance Type:
```
✅ Select: t2.micro
   - Should show "Free tier eligible"
   - 1 vCPU, 1 GiB Memory
```

#### Key Pair (Important!):
```
Click: "Create new key pair"

Key pair settings:
   - Key pair name: agentbeats-key
   - Key pair type: RSA
   - Private key format: .pem
   
Click "Create key pair"

📥 A file will download: agentbeats-key.pem
   ⚠️ SAVE THIS FILE! You'll need it!
```

#### Network Settings:
```
Click: "Edit" button

Under "Firewall (security groups)":
   ✅ Create security group
   
   Security group name: agentbeats-sg
   Description: Security for agent
   
Under "Inbound Security Group Rules", add these 4 rules:

   Rule 1:
   - Type: SSH
   - Protocol: TCP
   - Port: 22
   - Source type: My IP (or Anywhere)
   
   Rule 2:
   - Type: HTTP
   - Protocol: TCP
   - Port: 80
   - Source type: Anywhere (0.0.0.0/0)
   
   Rule 3:
   - Type: HTTPS
   - Protocol: TCP
   - Port: 443
   - Source type: Anywhere (0.0.0.0/0)
   
   Rule 4:
   - Type: Custom TCP
   - Protocol: TCP
   - Port: 8080
   - Source type: Anywhere (0.0.0.0/0)
```

#### Storage:
```
✅ Leave default: 8 GiB gp3
   (Free tier eligible)
```

### Step 4: Launch!

1. **Review** your configuration
2. Click **"Launch instance"** (orange button)
3. Wait ~2 minutes for it to start

### Step 5: Get Instance Information

After instance starts:

1. Click **"View all instances"**
2. Find your instance: `agentbeats-agent`
3. Click on it to see details

---

## PART 2: What I NEED From You (Copy These 3 Things)

### 📋 Give Me These 3 Pieces of Information:

#### 1. Public IPv4 Address
```
Location: In instance details, look for "Public IPv4 address"
Example: 54.123.45.67

YOUR IP: ___________________________
```

#### 2. Public IPv4 DNS (Optional but helpful)
```
Location: In instance details, look for "Public IPv4 DNS"
Example: ec2-54-123-45-67.us-east-1.compute.amazonaws.com

YOUR DNS: ___________________________
```

#### 3. Key File Location
```
Where you saved the .pem file
Default: ~/Downloads/agentbeats-key.pem

YOUR KEY LOCATION: ___________________________
```

---

## PART 3: Tell Me & I'll Do The Rest!

### Just reply with:

```
My EC2 IP: 54.123.45.67
My Key: ~/Downloads/agentbeats-key.pem
```

### Then I will:

✅ Generate personalized deployment commands  
✅ Create a script that will:
   - Setup SSH connection
   - Copy your agent to EC2
   - Install dependencies
   - Start your agent
   - Test it
✅ Give you your permanent agent URL  
✅ Help you register on AgentBeats  

---

## 📸 Visual Guide

### Where to Find Your IP Address:

After clicking on your instance, look for a box that shows:

```
┌─────────────────────────────────────┐
│ Instance Summary                    │
├─────────────────────────────────────┤
│ Instance ID: i-0abc123def456        │
│ Instance state: ● Running           │
│ ...                                 │
│ Public IPv4 address: 54.123.45.67  │ ← THIS ONE!
│ Public IPv4 DNS: ec2-54-123...     │ ← AND THIS!
├─────────────────────────────────────┤
```

---

## ⚠️ Important Notes

### About the Key File:

- **Don't lose it!** You can't download it again
- If lost, you'll need to create a new instance
- Keep it safe in `~/.ssh/` directory

### About Costs:

- **First 12 months**: FREE (750 hours/month of t2.micro)
- **After 12 months**: ~$8-10/month
- You can terminate the instance anytime to stop charges

### Security:

- The SSH key is your only way to access the server
- Keep port 22 (SSH) restricted to "My IP" for security
- Ports 80, 443, 8080 should be open to "Anywhere" so AgentBeats can reach your agent

---

## 🎬 Ready to Start?

### Do This Now:

1. ✅ Go to: https://console.aws.amazon.com/ec2/
2. ✅ Click "Launch Instance"
3. ✅ Follow the configuration above
4. ✅ Download your key file
5. ✅ Get your Public IP address
6. ✅ Reply with:
   ```
   My EC2 IP: [your IP]
   My Key: ~/Downloads/agentbeats-key.pem
   ```

### Then I'll Take Over! 🚀

I'll generate all the commands you need to:
- Connect to your EC2
- Deploy your agent
- Get it running
- Register on AgentBeats

---

## 🆘 Need Help?

### Can't find something?

**EC2 Dashboard**: https://console.aws.amazon.com/ec2/v2/home  
**Instances**: Click "Instances" in left sidebar  
**Launch Instance**: Orange button on top right  

### AWS Account Issues?

- Create account: https://aws.amazon.com/
- Free tier: https://aws.amazon.com/free/
- Support: https://console.aws.amazon.com/support/

---

## 📝 Summary

### You do (10 minutes):
- Launch EC2 instance on AWS
- Download key file
- Get IP address

### I do (automatic):
- Generate deployment commands
- Setup and deploy your agent
- Give you the permanent URL

### Result:
- ✅ Your agent running 24/7 on AWS
- ✅ Permanent URL for AgentBeats registration
- ✅ No more ngrok/tunnel issues!

---

**Ready? Let's launch that EC2 instance!** 🚀

Just reply with your IP when you have it!
