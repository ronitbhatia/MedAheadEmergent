import requests
import sys
import json
import io
from datetime import datetime

class HealthcareConferenceAPITester:
    def __init__(self, base_url="https://confprep.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.user_id = "test-user-001"

    def run_test(self, name, method, endpoint, expected_status, data=None, files=None, params=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'} if not files else {}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params)
            elif method == 'POST':
                if files:
                    response = requests.post(url, files=files, data=data)
                else:
                    response = requests.post(url, json=data, headers=headers, params=params)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
                except:
                    print(f"   Response: {response.text[:200]}...")
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:300]}...")

            return success, response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_health_check(self):
        """Test health endpoint"""
        return self.run_test(
            "Health Check",
            "GET",
            "api/health",
            200
        )

    def test_save_user_profile(self):
        """Test saving user profile"""
        profile_data = {
            "id": self.user_id,
            "name": "John Doe",
            "email": "john.doe@example.com",
            "company": "HealthTech Solutions",
            "industry": "Healthcare Technology",
            "role": "VP of Sales",
            "goals": ["Find new partners", "Showcase products", "Learn industry trends"]
        }
        
        success, response = self.run_test(
            "Save User Profile",
            "POST",
            "api/user/profile",
            200,
            data=profile_data
        )
        return success, response

    def test_get_user_profile(self):
        """Test getting user profile"""
        return self.run_test(
            "Get User Profile",
            "GET",
            f"api/user/profile/{self.user_id}",
            200
        )

    def test_get_conferences(self):
        """Test getting conferences without industry filter"""
        return self.run_test(
            "Get Conferences (No Filter)",
            "GET",
            "api/conferences",
            200
        )

    def test_get_conferences_with_industry(self):
        """Test getting conferences with industry filter"""
        return self.run_test(
            "Get Conferences (With Industry Filter)",
            "GET",
            "api/conferences",
            200,
            params={"industry": "Healthcare Technology"}
        )

    def test_upload_contacts(self):
        """Test uploading contacts CSV"""
        # Create a sample CSV content
        csv_content = """name,email,company,title,industry,conference
Dr. Sarah Johnson,sarah.johnson@medicorp.com,MediCorp,Chief Medical Officer,Healthcare,HIMSS 2025
Mike Chen,mike.chen@healthtech.com,HealthTech Inc,VP Engineering,Healthcare Technology,HIMSS 2025
Lisa Rodriguez,lisa.r@pharmaplus.com,PharmaPlus,Director of Operations,Pharmaceuticals,BIO 2025"""
        
        # Create a file-like object
        csv_file = io.StringIO(csv_content)
        files = {'file': ('test_contacts.csv', csv_content, 'text/csv')}
        data = {'user_id': self.user_id}
        
        return self.run_test(
            "Upload Contacts CSV",
            "POST",
            "api/contacts/upload",
            200,
            data=data,
            files=files
        )

    def test_analyze_contacts(self):
        """Test AI contact analysis"""
        return self.run_test(
            "Analyze Contacts with AI",
            "POST",
            "api/contacts/analyze",
            200,
            params={"user_id": self.user_id, "conference_id": "himss-2025"}
        )

    def test_suggest_meetings(self):
        """Test AI meeting suggestions"""
        return self.run_test(
            "Generate Meeting Suggestions",
            "POST",
            "api/meetings/suggest",
            200,
            params={"user_id": self.user_id, "conference_id": "himss-2025"}
        )

    def test_dashboard_stats(self):
        """Test dashboard statistics"""
        return self.run_test(
            "Get Dashboard Stats",
            "GET",
            "api/dashboard/stats",
            200,
            params={"user_id": self.user_id}
        )

def main():
    print("🚀 Starting Healthcare Conference Targeting API Tests")
    print("=" * 60)
    
    tester = HealthcareConferenceAPITester()
    
    # Test sequence
    tests = [
        ("Health Check", tester.test_health_check),
        ("Save User Profile", tester.test_save_user_profile),
        ("Get User Profile", tester.test_get_user_profile),
        ("Get Conferences", tester.test_get_conferences),
        ("Get Conferences with Industry", tester.test_get_conferences_with_industry),
        ("Upload Contacts", tester.test_upload_contacts),
        ("Analyze Contacts", tester.test_analyze_contacts),
        ("Suggest Meetings", tester.test_suggest_meetings),
        ("Dashboard Stats", tester.test_dashboard_stats)
    ]
    
    for test_name, test_func in tests:
        try:
            test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {str(e)}")
    
    # Print final results
    print("\n" + "=" * 60)
    print(f"📊 FINAL RESULTS:")
    print(f"   Tests Run: {tester.tests_run}")
    print(f"   Tests Passed: {tester.tests_passed}")
    print(f"   Tests Failed: {tester.tests_run - tester.tests_passed}")
    print(f"   Success Rate: {(tester.tests_passed/tester.tests_run)*100:.1f}%")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed. Check the details above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())