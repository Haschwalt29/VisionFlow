#!/usr/bin/env python3
"""
VisionFlow API Key Setup Helper
This script helps you quickly set up your OpenAI API key
"""

import os
import sys

def set_api_key_interactive():
    """Interactive API key setup"""
    print("=" * 60)
    print("🔑 VisionFlow OpenAI API Key Setup")
    print("=" * 60)
    
    print("\n📝 To use VisionFlow's AI extraction features, you need an OpenAI API key.")
    print("\n1. Visit: https://platform.openai.com/account/api-keys")
    print("2. Sign in to your OpenAI account")
    print("3. Create a new API key")
    print("4. Copy the key (starts with sk-proj-)")
    
    api_key = input("\n🔑 Enter your OpenAI API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Exiting.")
        return False
    
    if not api_key.startswith('sk-'):
        print("⚠️  Warning: API key doesn't look like a valid OpenAI key (should start with 'sk-')")
        confirm = input("Continue anyway? (y/n): ").strip().lower()
        if confirm != 'y':
            print("❌ Setup cancelled.")
            return False
    
    # Method 1: Create .env file
    env_file = os.path.join('backend', '.env')
    try:
        with open(env_file, 'w') as f:
            f.write(f"OPENAI_API_KEY={api_key}\n")
            f.write("FLASK_DEBUG=True\n")
            f.write("PORT=5000\n")
        print(f"✅ API key saved to {env_file}")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        
        # Method 2: Set environment variable
        print("\n🔄 Trying alternative method - environment variable...")
        try:
            os.environ['OPENAI_API_KEY'] = api_key
            print("✅ API key set as environment variable for this session")
            print("🔄 Please restart the backend server to use the new key")
            return True
        except Exception as e2:
            print(f"❌ Failed to set environment variable: {e2}")
            return False

def check_current_status():
    """Check current API key status"""
    print("\n🔍 Checking current configuration...")
    
    # Check .env file
    env_file = os.path.join('backend', '.env')
    if os.path.exists(env_file):
        try:
            with open(env_file, 'r') as f:
                content = f.read()
                if 'OPENAI_API_KEY=' in content and 'sk-' in content:
                    print("✅ Found API key in .env file")
                    return True
        except:
            pass
    
    # Check environment variable
    if os.getenv('OPENAI_API_KEY'):
        print("✅ Found API key in environment variables")
        return True
    
    print("❌ No API key found")
    return False

def main():
    """Main setup function"""
    print("🤖 VisionFlow Setup Assistant")
    
    if check_current_status():
        print("\n🎉 API key already configured!")
        choice = input("Do you want to reconfigure? (y/n): ").strip().lower()
        if choice != 'y':
            print("✅ Setup complete - you're ready to use VisionFlow!")
            return
    
    print("\n🚀 Starting API key setup...")
    
    if set_api_key_interactive():
        print("\n" + "=" * 60)
        print("🎉 Setup Complete!")
        print("=" * 60)
        print("✅ Your OpenAI API key has been configured")
        print("🚀 You can now use VisionFlow's AI extraction features")
        print("\n📋 Next steps:")
        print("1. Restart the backend server: cd backend && python app.py")
        print("2. Open your browser to: http://localhost:3000")
        print("3. Try extracting data from any website!")
        print("\n💡 Example URLs to try:")
        print("   - https://openai.com")
        print("   - https://github.com")
        print("   - https://www.apple.com")
    else:
        print("\n❌ Setup failed. Please try again manually.")
        print("📝 Manual setup: Create backend/.env file with:")
        print("   OPENAI_API_KEY=your_key_here")

if __name__ == '__main__':
    main()
