#!/usr/bin/env python3
"""
WebIPTV Site Analysis Tool
This script analyzes the structure of webiptv.site
"""
import os
import json
import time
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
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
    else:
        chrome_options.add_argument("--start-maximized")
    
    # Common options
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    # Disable automation flags
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver

def analyze_site_structure(driver):
    """Analyze the structure of webiptv.site"""
    print("🔍 Starting WebIPTV Site Analysis")
    print("=" * 50)
    
    try:
        # 1. Load the site
        print("📡 Loading https://webiptv.site/")
        driver.get("https://webiptv.site/")
        time.sleep(10)  # Wait longer for full load
        
        # 2. Get page info
        page_title = driver.title
        current_url = driver.current_url
        print(f"📄 Page Title: {page_title}")
        print(f"🔗 Current URL: {current_url}")
        
        # 3. Save page source
        page_source = driver.page_source
        with open("site_analysis.html", "w", encoding="utf-8") as f:
            f.write(page_source)
        print("✅ Saved: site_analysis.html")
        
        # 4. Take screenshot
        driver.save_screenshot("site_homepage.png")
        print("✅ Saved: site_homepage.png")
        
        # 5. Look for specific elements
        findings = {
            "page_info": {
                "title": page_title,
                "url": current_url,
                "source_length": len(page_source)
            },
            "elements": {}
        }
        
        # Test selectors for different elements
        test_selectors = {
            "login_buttons": [
                "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'login')]",
                "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'login')]",
                "//*[contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'login')]",
                "//*[contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'login')]",
                "//input[contains(translate(@type, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'submit') and contains(translate(@value, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'login')]"
            ],
            "telegram_elements": [
                "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'telegram')]",
                "//*[contains(translate(@href, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'telegram')]",
                "//*[contains(translate(@onclick, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'telegram')]",
                "//img[contains(translate(@src, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'telegram')]"
            ],
            "channels": [
                "//*[contains(text(), 'Sky SPORT')]",
                "//*[contains(text(), 'Willow')]",
                "//*[contains(text(), 'STARZ')]",
                "//*[contains(text(), 'Cric')]",
                "//*[contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'channel')]",
                "//*[contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'item')]",
                "//div[contains(@class, 'item')]",
                "//li[contains(@class, 'item')]",
                "//div[@class='channel-item']",
                "//div[@class='channel-list']//div"
            ],
            "video_elements": [
                "//video",
                "//iframe",
                "//*[contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'player')]",
                "//*[contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'player')]",
                "//*[contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'video')]"
            ],
            "navigation": [
                "//nav",
                "//*[contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'menu')]",
                "//*[contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'navbar')]",
                "//ul[contains(@class, 'menu')]"
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
                        for i, element in enumerate(elements[:3]):  # Limit to first 3
                            try:
                                element_info = {
                                    "selector": selector,
                                    "count": len(elements),
                                    "index": i,
                                    "tag": element.tag_name,
                                    "text": element.text[:100] if element.text else "",
                                    "classes": element.get_attribute("class") or "",
                                    "id": element.get_attribute("id") or "",
                                    "href": element.get_attribute("href") or "",
                                    "visible": element.is_displayed()
                                }
                                category_findings.append(element_info)
                                print(f"   ✓ Found: {selector}")
                                print(f"     Text: {element.text[:50] if element.text else 'No text'}")
                            except:
                                continue
                except Exception as e:
                    print(f"   ✗ Error with {selector}: {str(e)[:50]}")
                    continue
            
            findings["elements"][category] = category_findings
        
        # 6. Save findings
        with open("site_findings.json", "w", encoding="utf-8") as f:
            json.dump(findings, f, indent=2, ensure_ascii=False)
        
        print("\n" + "=" * 50)
        print("📊 Analysis Complete!")
        print(f"📄 Page source saved: {len(page_source)} characters")
        print(f"📋 Findings saved: site_findings.json")
        
        # Print summary
        print("\n📈 Summary of findings:")
        for category, items in findings["elements"].items():
            print(f"  {category}: {len(items)} element(s) found")
        
        return findings
        
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        # Save error info
        error_info = {
            "error": str(e),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        with open("site_findings.json", "w", encoding="utf-8") as f:
            json.dump(error_info, f, indent=2)
        return None

def main():
    """Main function"""
    driver = None
    try:
        driver = setup_driver()
        findings = analyze_site_structure(driver)
        
        if findings:
            print("\n✅ Analysis successful!")
            print("📁 Files created:")
            print("  • site_analysis.html - Full page HTML")
            print("  • site_homepage.png - Screenshot")
            print("  • site_findings.json - Element analysis")
        else:
            print("\n❌ Analysis failed!")
            
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        
    finally:
        if driver:
            driver.quit()
        print("\n🏁 Analysis script finished")

if __name__ == "__main__":
    main()
