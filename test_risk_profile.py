#!/usr/bin/env python3
"""
Test script for the risk-profile API endpoint
"""

import requests
import json
import os

def test_risk_profile():
    """Test the risk profile endpoint"""
    
    # API endpoint
    url = "http://localhost:8000/api/risk-profile"
    
    # Test data based on the example provided
    test_data = {
        "json_data": {
            "nodes": [
                {
                    "name": "bid",
                    "type": "decision",
                    "branches": [
                        {
                            "label": "low",
                            "next": "competitor_bid",
                            "value": 300
                        },
                        {
                            "label": "medium",
                            "next": "competitor_bid",
                            "value": 500
                        },
                        {
                            "label": "high",
                            "next": "competitor_bid",
                            "value": 700
                        },
                        {
                            "label": "no-bid",
                            "next": "profit",
                            "value": "0"
                        }
                    ]
                },
                {
                    "name": "competitor_bid",
                    "type": "chance",
                    "branches": [
                        {
                            "label": "low",
                            "next": "cost",
                            "value": 400,
                            "probability": 0.35
                        },
                        {
                            "label": "medium",
                            "next": "cost",
                            "value": 600,
                            "probability": 0.5
                        },
                        {
                            "label": "high",
                            "next": "cost",
                            "value": 800,
                            "probability": 0.15
                        }
                    ]
                },
                {
                    "name": "cost",
                    "type": "chance",
                    "branches": [
                        {
                            "label": "low",
                            "next": "profit",
                            "value": 200,
                            "probability": 0.25
                        },
                        {
                            "label": "medium",
                            "next": "profit",
                            "value": 400,
                            "probability": 0.5
                        },
                        {
                            "label": "high",
                            "next": "profit",
                            "value": 600,
                            "probability": 0.25
                        }
                    ]
                },
                {
                    "name": "profit",
                    "type": "terminal",
                    "branches": []
                }
            ]
        },
        "payoff_fn_code": """def payoff_fn(values, probabilities, branches):
    bid = values["bid"] if "bid" in values.keys() else 0
    competitor_bid = (
        values["competitor_bid"] 
        if "competitor_bid" in values.keys() else 0
    )
    cost = values["cost"] if "cost" in values.keys() else 0
    return (bid - cost) * (1 if bid < competitor_bid else 0)""",
        "idx": 0,
        "cumulative": False,
        "single": True
    }
    
    try:
        print("Testing risk profile endpoint...")
        print(f"URL: {url}")
        print(f"Node Index: {test_data['idx']}")
        print(f"Cumulative: {test_data['cumulative']}")
        print(f"Single: {test_data['single']}")
        print()
        
        # Make the request
        response = requests.post(url, json=test_data, headers={"Content-Type": "application/json"})
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print()
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            print(f"Message: {result.get('message', 'N/A')}")
            print(f"File URL: {result.get('file_url', 'N/A')}")
            
            # Test if the image file is accessible
            if result.get('file_url'):
                print(f"\nTesting image accessibility...")
                try:
                    img_response = requests.get(result['file_url'])
                    if img_response.status_code == 200:
                        print("✅ Image file is accessible!")
                        print(f"Image size: {len(img_response.content)} bytes")
                        print(f"Content type: {img_response.headers.get('content-type', 'N/A')}")
                        
                        # Check if output directory exists and contains the file
                        filename = result['file_url'].split('/')[-1]
                        output_path = f"output/{filename}"
                        if os.path.exists(output_path):
                            print(f"✅ Local file exists: {output_path}")
                            print(f"File size: {os.path.getsize(output_path)} bytes")
                        else:
                            print(f"❌ Local file not found: {output_path}")
                            
                    else:
                        print(f"❌ Image file not accessible: {img_response.status_code}")
                        print(f"Response: {img_response.text}")
                except Exception as e:
                    print(f"❌ Error accessing image: {str(e)}")
            else:
                print("❌ No file_url in response")
            
        else:
            print("❌ Error!")
            print(f"Error Detail: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")

def test_health_check():
    """Test the health check endpoint"""
    try:
        response = requests.get("http://localhost:8000/api/health")
        if response.status_code == 200:
            print("✅ Server is running and healthy")
            return True
        else:
            print(f"❌ Server health check failed: {response.status_code}")
            return False
    except:
        print("❌ Server is not running")
        return False

def test_output_directory():
    """Test if output directory exists and is accessible"""
    output_dir = "output"
    if os.path.exists(output_dir):
        print(f"✅ Output directory exists: {output_dir}")
        files = os.listdir(output_dir)
        print(f"Files in output directory: {files}")
        return True
    else:
        print(f"❌ Output directory not found: {output_dir}")
        return False

if __name__ == "__main__":
    print("=== Risk Profile API Test ===\n")
    
    # First check if server is running
    if test_health_check():
        print()
        # Check output directory
        test_output_directory()
        print()
        # Test risk profile
        test_risk_profile()
    else:
        print("\nPlease start the server first:")
        print("cd smart_server && python server.py") 