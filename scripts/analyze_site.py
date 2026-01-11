#!/usr/bin/env python3
"""
WebIPTV Site Analysis Tool
This script analyzes the structure of webiptv.site
"""
import os
import json
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    """Setup Chrome driver for GitHub Actions"""
    chrome_options = Options()
    
    # GitHub Actions specific settings
    if os.getenv('GITHUB_ACTIONS') == 'true':
        chrome_options.add_argument("--headless=new")  # NEW: Use new headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
    else:
        chrome_options.add_argument("--start-maximized")
    
    # Common options
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Add user agent
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Disable some features that might interfere
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Execute CDP commands
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        return driver
    except Exception as e:
        print(f"❌ Failed to setup driver: {e}")
        return None

def analyze_site_structure(driver):
    """Analyze the structure of webiptv.site"""
    print("🔍 Starting WebIPTV Site Analysis")
    print("=" * 50)
    
    try:
        # 1. Load the site
        print("📡 Loading https://webiptv.site/")
        start_time = time.time()
        driver.get("https://webiptv.site/")
        
        # Wait for page to load with multiple strategies
        time.sleep(10)  # Initial wait
        
        # Check if page loaded
        page_title = driver.title
        current_url = driver.current_url
        print(f"📄 Page Title: {page_title}")
        print(f"🔗 Current URL: {current_url}")
        print(f"⏱️  Load time: {time.time() - start_time:.2f}s")
        
        # 2. Save page source
        page_source = driver.page_source
        source_length = len(page_source)
        
        if source_length < 100:
            print("⚠️  Warning: Page source is very short. Site might be blocking access.")
        
        with open("site_analysis.html", "w", encoding="utf-8") as f:
            f.write(page_source)
        print(f"✅ Saved: site_analysis.html ({source_length:,} characters)")
        
        # 3. Take screenshot
        try:
            driver.save_screenshot("site_homepage.png")
            print("✅ Saved: site_homepage.png")
        except Exception as e:
            print(f"⚠️  Could not save screenshot: {e}")
        
        # 4. Look for specific elements
        findings = {
            "page_info": {
                "title": page_title,
                "url": current_url,
                "source_length": source_length,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            },
            "elements": {}
        }
        
        # Test selectors for different elements
        test_selectors = {
            "login_buttons": [
                "//button[contains(., 'Login') or contains(., 'login')]",
                "//a[contains(., 'Login') or contains(., 'login')]",
                "//input[@type='submit' and contains(@value, 'Login')]",
                "//div[contains(@class, 'login')]",
                "//*[@id='login']",
                "//*[contains(@onclick, 'login')]"
            ],
            "telegram_elements": [
                "//*[contains(., 'Telegram') or contains(., 'telegram')]",
                "//a[contains(@href, 'telegram')]",
                "//img[contains(@src, 'telegram')]",
                "//button[contains(., 'Telegram')]"
            ],
            "channels": [
                "//*[contains(., 'Sky')]",
                "//*[contains(., 'Willow')]",
                "//*[contains(., 'STARZ')]",
                "//*[contains(., 'Cric')]",
                "//div[contains(@class, 'channel')]",
                "//li[contains(@class, 'channel')]",
                "//*[contains(@class, 'item')]",
                "//div[@class='channel-item']",
                "//div[contains(@id, 'channel')]"
            ],
            "video_elements": [
                "//video",
                "//iframe",
                "//*[contains(@class, 'player')]",
                "//*[@id='player']",
                "//*[contains(@class, 'video')]",
                "//*[contains(@id, 'video')]"
            ],
            "navigation": [
                "//nav",
                "//ul[contains(@class, 'menu')]",
                "//div[contains(@class, 'navbar')]",
                "//header",
                "//footer"
            ]
        }
        
        print("\n🔎 Testing selectors...")
        for category, selectors in test_selectors.items():
            print(f"\n📋 Category: {category}")
            category_findings = []
            
            for selector in selectors:
                try:
                    elements = driver.find_elements(By.XPATH, selector)
                    if elements:
                        element_count = len(elements)
                        print(f"   ✓ Found {element_count} element(s) with: {selector}")
                        
                        # Get details of first element
                        first_element = elements[0]
                        try:
                            element_info = {
                                "selector": selector,
                                "count": element_count,
                                "tag": first_element.tag_name,
                                "text": first_element.text.strip()[:100] if first_element.text else "",
                                "classes": first_element.get_attribute("class") or "",
                                "id": first_element.get_attribute("id") or "",
                                "href": first_element.get_attribute("href") or "",
                                "visible": first_element.is_displayed(),
                                "location": first_element.location
                            }
                            category_findings.append(element_info)
                        except:
                            # Basic info if detailed fails
                            category_findings.append({
                                "selector": selector,
                                "count": element_count
                            })
                except Exception as e:
                    # Skip selector errors
                    continue
            
            findings["elements"][category] = category_findings
        
        # 5. Check for common IPTV patterns
        print("\n🔍 Checking for IPTV patterns...")
        patterns = {
            "mpd_links": r'https?://[^\s"\']+\.mpd',
            "m3u_links": r'https?://[^\s"\']+\.m3u8?',
            "stream_links": r'https?://[^\s"\']+/stream/',
            "iframe_src": r'<iframe[^>]+src="([^"]+)"'
        }
        
        pattern_findings = {}
        for pattern_name, pattern in patterns.items():
            matches = re.findall(pattern, page_source, re.IGNORECASE)
            if matches:
                pattern_findings[pattern_name] = {
                    "count": len(matches),
                    "examples": matches[:3]  # First 3 examples
                }
                print(f"   ✓ Found {len(matches)} {pattern_name}")
        
        findings["patterns"] = pattern_findings
        
        # 6. Save findings
        with open("site_findings.json", "w", encoding="utf-8") as f:
            json.dump(findings, f, indent=2, ensure_ascii=False)
        
        print("\n" + "=" * 50)
        print("📊 Analysis Complete!")
        print(f"📄 Page source: {source_length:,} characters")
        print(f"📋 Total elements tested: {sum(len(v) for v in findings['elements'].values())}")
        
        # Print summary
        print("\n📈 Summary of findings:")
        for category, items in findings["elements"].items():
            if items:
                print(f"  • {category}: {len(items)} selector(s) worked")
        
        if pattern_findings:
            print(f"\n🎯 Streaming patterns found:")
            for pattern, data in pattern_findings.items():
                print(f"  • {pattern}: {data['count']} match(es)")
        
        return findings
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        
        # Save error info
        error_info = {
            "error": str(e),
            "error_type": type(e).__name__,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        with open("site_findings.json", "w", encoding="utf-8") as f:
            json.dump(error_info, f, indent=2)
        return None

def main():
    """Main function"""
    print("🚀 WebIPTV Site Analysis Tool")
    print("=" * 40)
    
    driver = None
    try:
        driver = setup_driver()
        if not driver:
            print("❌ Failed to initialize browser driver")
            sys.exit(1)
        
        findings = analyze_site_structure(driver)
        
        if findings:
            print("\n✅ Analysis successful!")
            print("📁 Files created:")
            print("  • site_analysis.html - Full page HTML")
            print("  • site_homepage.png - Screenshot")
            print("  • site_findings.json - Element analysis")
        else:
            print("\n❌ Analysis failed or incomplete")
            
    except KeyboardInterrupt:
        print("\n⚠️  Analysis interrupted by user")
    except Exception as e:
        print(f"\n💥 Fatal error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
        print("\n🏁 Analysis script finished")

if __name__ == "__main__":
    main()
