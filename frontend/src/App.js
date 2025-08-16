import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Button } from './components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './components/ui/card';
import { Input } from './components/ui/input';
import { Label } from './components/ui/label';
import { Textarea } from './components/ui/textarea';
import { Badge } from './components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs';
import { Progress } from './components/ui/progress';
import { Alert, AlertDescription } from './components/ui/alert';
import { 
  Upload, 
  Users, 
  Calendar, 
  TrendingUp, 
  Target, 
  Brain,
  Building2,
  Mail,
  Clock,
  Star,
  ArrowRight,
  CheckCircle,
  AlertCircle,
  BarChart3
} from 'lucide-react';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

function App() {
  const [currentStep, setCurrentStep] = useState(0);
  const [userProfile, setUserProfile] = useState({
    name: '',
    email: '',
    company: '',
    industry: '',
    role: '',
    goals: []
  });
  const [conferences, setConferences] = useState([]);
  const [selectedConference, setSelectedConference] = useState(null);
  const [contacts, setContacts] = useState([]);
  const [analyzedContacts, setAnalyzedContacts] = useState([]);
  const [meetingSuggestions, setMeetingSuggestions] = useState([]);
  const [dashboardStats, setDashboardStats] = useState({});
  const [loading, setLoading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState('');

  const steps = [
    'Profile Setup',
    'Conference Discovery', 
    'Contact Upload',
    'AI Analysis',
    'Meeting Planning',
    'Dashboard'
  ];

  // Save user profile
  const handleProfileSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/api/user/profile`, {
        ...userProfile,
        id: userProfile.id || 'user-001'
      });
      
      if (response.data.success) {
        setCurrentStep(1);
        fetchConferences();
      }
    } catch (error) {
      console.error('Error saving profile:', error);
    }
    setLoading(false);
  };

  // Fetch conferences
  const fetchConferences = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/api/conferences?industry=${userProfile.industry}`);
      setConferences(response.data.conferences || []);
    } catch (error) {
      console.error('Error fetching conferences:', error);
    }
    setLoading(false);
  };

  // Handle file upload
  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setLoading(true);
    setUploadStatus('Uploading...');
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', 'user-001');

    try {
      const response = await axios.post(`${API_BASE_URL}/api/contacts/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      setUploadStatus(`✓ ${response.data.message}`);
      setCurrentStep(3);
    } catch (error) {
      setUploadStatus('Upload failed. Please try again.');
      console.error('Upload error:', error);
    }
    setLoading(false);
  };

  // Analyze contacts with AI
  const analyzeContacts = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/api/contacts/analyze`, null, {
        params: { user_id: 'user-001', conference_id: selectedConference?.id || 'himss-2025' }
      });
      
      setAnalyzedContacts(response.data.analyzed_contacts || []);
      setCurrentStep(4);
    } catch (error) {
      console.error('Error analyzing contacts:', error);
    }
    setLoading(false);
  };

  // Generate meeting suggestions
  const generateMeetingSuggestions = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/api/meetings/suggest`, null, {
        params: { user_id: 'user-001', conference_id: selectedConference?.id || 'himss-2025' }
      });
      
      setMeetingSuggestions(response.data.meeting_suggestions || []);
      setCurrentStep(5);
      fetchDashboardStats();
    } catch (error) {
      console.error('Error generating meetings:', error);
    }
    setLoading(false);
  };

  // Fetch dashboard stats
  const fetchDashboardStats = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/dashboard/stats?user_id=user-001`);
      setDashboardStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-800 border-red-200';
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low': return 'bg-green-100 text-green-800 border-green-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-blue-100">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center">
                <Target className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">HealthConnect Pro</h1>
                <p className="text-sm text-gray-600">AI-Powered Conference Targeting</p>
              </div>
            </div>
            
            {/* Progress Steps */}
            <div className="hidden md:flex items-center space-x-4">
              {steps.map((step, index) => (
                <div key={index} className="flex items-center">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium
                    ${index <= currentStep 
                      ? 'bg-blue-600 text-white' 
                      : 'bg-gray-200 text-gray-600'
                    }`}>
                    {index < currentStep ? <CheckCircle className="w-4 h-4" /> : index + 1}
                  </div>
                  {index < steps.length - 1 && (
                    <div className={`w-16 h-0.5 mx-2 ${index < currentStep ? 'bg-blue-600' : 'bg-gray-200'}`} />
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Step 0: Profile Setup */}
        {currentStep === 0 && (
          <Card className="max-w-2xl mx-auto">
            <CardHeader className="text-center">
              <CardTitle className="text-3xl font-bold text-gray-900 mb-2">
                Welcome to HealthConnect Pro
              </CardTitle>
              <p className="text-gray-600">
                Let's set up your profile to maximize your healthcare conference networking
              </p>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleProfileSubmit} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="name">Full Name *</Label>
                    <Input
                      id="name"
                      value={userProfile.name}
                      onChange={(e) => setUserProfile({...userProfile, name: e.target.value})}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="email">Email *</Label>
                    <Input
                      id="email"
                      type="email"
                      value={userProfile.email}
                      onChange={(e) => setUserProfile({...userProfile, email: e.target.value})}
                      required
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="company">Company *</Label>
                    <Input
                      id="company"
                      value={userProfile.company}
                      onChange={(e) => setUserProfile({...userProfile, company: e.target.value})}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="role">Role *</Label>
                    <Input
                      id="role"
                      value={userProfile.role}
                      onChange={(e) => setUserProfile({...userProfile, role: e.target.value})}
                      required
                    />
                  </div>
                </div>

                <div>
                  <Label htmlFor="industry">Industry *</Label>
                  <select
                    className="w-full p-2 border border-gray-300 rounded-md"
                    value={userProfile.industry}
                    onChange={(e) => setUserProfile({...userProfile, industry: e.target.value})}
                    required
                  >
                    <option value="">Select Industry</option>
                    <option value="Healthcare Technology">Healthcare Technology</option>
                    <option value="Medical Devices">Medical Devices</option>
                    <option value="Pharmaceuticals">Pharmaceuticals</option>
                    <option value="Hospital Systems">Hospital Systems</option>
                    <option value="Health Insurance">Health Insurance</option>
                    <option value="Digital Health">Digital Health</option>
                    <option value="Biotechnology">Biotechnology</option>
                  </select>
                </div>

                <div>
                  <Label htmlFor="goals">Conference Goals</Label>
                  <Textarea
                    id="goals"
                    placeholder="What do you hope to achieve at healthcare conferences? (e.g., find new partners, showcase products, learn trends)"
                    value={userProfile.goals.join('\n')}
                    onChange={(e) => setUserProfile({...userProfile, goals: e.target.value.split('\n')})}
                    rows={3}
                  />
                </div>

                <Button type="submit" className="w-full" size="lg" disabled={loading}>
                  {loading ? 'Setting up...' : 'Continue to Conference Discovery'}
                  <ArrowRight className="w-4 h-4 ml-2" />
                </Button>
              </form>
            </CardContent>
          </Card>
        )}

        {/* Step 1: Conference Discovery */}
        {currentStep === 1 && (
          <div>
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">Discover Relevant Conferences</h2>
              <p className="text-gray-600">AI-curated conferences based on your industry and goals</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {conferences.map((conference) => (
                <Card 
                  key={conference.id} 
                  className={`cursor-pointer transition-all duration-200 hover:shadow-lg border-2
                    ${selectedConference?.id === conference.id 
                      ? 'border-blue-500 bg-blue-50' 
                      : 'border-gray-200 hover:border-blue-300'
                    }`}
                  onClick={() => setSelectedConference(conference)}
                >
                  <CardHeader>
                    <div className="flex justify-between items-start">
                      <CardTitle className="text-xl">{conference.name}</CardTitle>
                      {conference.relevance_score && (
                        <Badge className="bg-green-100 text-green-800">
                          {conference.relevance_score}% Match
                        </Badge>
                      )}
                    </div>
                    <p className="text-gray-600">{conference.date} • {conference.location}</p>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <p className="text-sm text-gray-700">{conference.description}</p>
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          <Users className="w-4 h-4 text-gray-500" />
                          <span className="text-sm">{conference.attendees.toLocaleString()} attendees</span>
                        </div>
                        <Badge variant="outline">{conference.focus}</Badge>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            {selectedConference && (
              <div className="text-center mt-8">
                <Button 
                  onClick={() => setCurrentStep(2)} 
                  size="lg"
                  className="px-8"
                >
                  Continue with {selectedConference.name}
                  <ArrowRight className="w-4 h-4 ml-2" />
                </Button>
              </div>
            )}
          </div>
        )}

        {/* Step 2: Contact Upload */}
        {currentStep === 2 && (
          <Card className="max-w-2xl mx-auto">
            <CardHeader className="text-center">
              <CardTitle className="text-3xl font-bold text-gray-900 mb-2">
                Upload Attendee List
              </CardTitle>
              <p className="text-gray-600">
                Upload your CSV file with conference attendees and vendors
              </p>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <div className="space-y-2">
                  <p className="text-lg font-medium">Drop your CSV file here</p>
                  <p className="text-sm text-gray-500">
                    Required columns: name, email, company, title, industry
                  </p>
                </div>
                <div className="mt-4">
                  <Input
                    type="file"
                    accept=".csv"
                    onChange={handleFileUpload}
                    className="file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                  />
                </div>
              </div>

              {uploadStatus && (
                <Alert className={uploadStatus.includes('✓') ? 'border-green-200 bg-green-50' : 'border-yellow-200 bg-yellow-50'}>
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription>{uploadStatus}</AlertDescription>
                </Alert>
              )}

              {/* Sample data download */}
              <div className="bg-blue-50 p-4 rounded-lg">
                <h4 className="font-medium text-blue-900 mb-2">Need sample data?</h4>
                <p className="text-sm text-blue-700 mb-3">
                  Download our sample CSV template to see the expected format
                </p>
                <Button variant="outline" size="sm">
                  Download Sample CSV
                </Button>
              </div>

              {loading && (
                <div className="flex items-center justify-center py-4">
                  <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
                  <span className="ml-2">Processing upload...</span>
                </div>
              )}
            </CardContent>
          </Card>
        )}

        {/* Step 3: AI Analysis */}
        {currentStep === 3 && (
          <Card className="max-w-2xl mx-auto">
            <CardHeader className="text-center">
              <CardTitle className="flex items-center justify-center text-3xl font-bold text-gray-900 mb-2">
                <Brain className="w-8 h-8 mr-3 text-blue-600" />
                AI Contact Analysis
              </CardTitle>
              <p className="text-gray-600">
                Let our AI analyze and score your contacts for maximum networking ROI
              </p>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-lg">
                <h3 className="font-semibold text-gray-900 mb-3">What our AI analyzes:</h3>
                <ul className="space-y-2 text-sm text-gray-700">
                  <li className="flex items-center">
                    <CheckCircle className="w-4 h-4 text-green-600 mr-2" />
                    Company relevance to your industry
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="w-4 h-4 text-green-600 mr-2" />
                    Decision-maker identification
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="w-4 h-4 text-green-600 mr-2" />
                    Strategic partnership potential
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="w-4 h-4 text-green-600 mr-2" />
                    Networking priority scoring
                  </li>
                </ul>
              </div>

              <Button 
                onClick={analyzeContacts} 
                size="lg" 
                className="w-full"
                disabled={loading}
              >
                {loading ? (
                  <div className="flex items-center">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Analyzing Contacts...
                  </div>
                ) : (
                  <>
                    Start AI Analysis
                    <Brain className="w-4 h-4 ml-2" />
                  </>
                )}
              </Button>
            </CardContent>
          </Card>
        )}

        {/* Step 4: Analysis Results & Meeting Planning */}
        {currentStep === 4 && analyzedContacts.length > 0 && (
          <div>
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">Analysis Complete!</h2>
              <p className="text-gray-600">Here are your top networking opportunities</p>
            </div>

            <div className="space-y-6">
              {analyzedContacts.slice(0, 10).map((contact, index) => (
                <Card key={contact.id} className="border border-gray-200">
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center space-x-4">
                        <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                          <Building2 className="w-6 h-6 text-blue-600" />
                        </div>
                        <div>
                          <h3 className="font-semibold text-lg">{contact.name}</h3>
                          <p className="text-gray-600">{contact.title} at {contact.company}</p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-3">
                        <Badge className={getPriorityColor(contact.priority)}>
                          {contact.priority.toUpperCase()}
                        </Badge>
                        <div className="text-right">
                          <div className="font-bold text-lg text-blue-600">{contact.score}/100</div>
                          <div className="text-sm text-gray-500">AI Score</div>
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-6 text-sm text-gray-600 mb-3">
                      <span className="flex items-center">
                        <Mail className="w-4 h-4 mr-1" />
                        {contact.email}
                      </span>
                      <span className="flex items-center">
                        <Badge variant="outline">{contact.industry}</Badge>
                      </span>
                    </div>
                    
                    {contact.ai_notes && (
                      <p className="text-sm text-gray-700 bg-gray-50 p-3 rounded-md">
                        {contact.ai_notes}
                      </p>
                    )}
                  </CardContent>
                </Card>
              ))}

              <div className="text-center">
                <Button 
                  onClick={generateMeetingSuggestions} 
                  size="lg"
                  disabled={loading}
                  className="px-8"
                >
                  {loading ? 'Generating Meeting Suggestions...' : 'Generate Meeting Plan'}
                  <Calendar className="w-4 h-4 ml-2" />
                </Button>
              </div>
            </div>
          </div>
        )}

        {/* Step 5: Dashboard */}
        {currentStep === 5 && (
          <div>
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">Your Conference Success Dashboard</h2>
              <p className="text-gray-600">Track your networking progress and ROI</p>
            </div>

            <Tabs defaultValue="meetings" className="space-y-6">
              <TabsList className="grid w-full grid-cols-3">
                <TabsTrigger value="meetings">Meeting Suggestions</TabsTrigger>
                <TabsTrigger value="analytics">Analytics</TabsTrigger>
                <TabsTrigger value="outreach">Outreach Templates</TabsTrigger>
              </TabsList>

              <TabsContent value="meetings" className="space-y-4">
                {meetingSuggestions.map((meeting, index) => (
                  <Card key={meeting.id} className="border border-gray-200">
                    <CardContent className="p-6">
                      <div className="flex justify-between items-start mb-4">
                        <div>
                          <h3 className="font-semibold text-lg">{meeting.contact_name}</h3>
                          <p className="text-gray-600">{meeting.contact_company}</p>
                        </div>
                        <Badge className={getPriorityColor(meeting.priority)}>
                          {meeting.priority.toUpperCase()}
                        </Badge>
                      </div>
                      
                      <div className="space-y-3">
                        <div className="flex items-center text-sm text-gray-600">
                          <Clock className="w-4 h-4 mr-2" />
                          Suggested Time: {meeting.suggested_time}
                        </div>
                        
                        <div>
                          <h4 className="font-medium mb-2">Meeting Purpose:</h4>
                          <p className="text-sm text-gray-700">{meeting.reason}</p>
                        </div>
                        
                        <div>
                          <h4 className="font-medium mb-2">Personalized Outreach:</h4>
                          <div className="bg-gray-50 p-3 rounded-md text-sm">
                            {meeting.personalized_message}
                          </div>
                        </div>
                        
                        <div className="flex space-x-3 pt-3">
                          <Button size="sm" variant="outline">
                            <Mail className="w-4 h-4 mr-2" />
                            Send Email
                          </Button>
                          <Button size="sm" variant="outline">
                            <Calendar className="w-4 h-4 mr-2" />
                            Schedule
                          </Button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </TabsContent>

              <TabsContent value="analytics">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  <Card>
                    <CardContent className="p-6 text-center">
                      <Users className="w-8 h-8 text-blue-600 mx-auto mb-2" />
                      <div className="text-2xl font-bold">{dashboardStats.total_contacts || 0}</div>
                      <div className="text-sm text-gray-600">Total Contacts</div>
                    </CardContent>
                  </Card>
                  
                  <Card>
                    <CardContent className="p-6 text-center">
                      <Star className="w-8 h-8 text-yellow-600 mx-auto mb-2" />
                      <div className="text-2xl font-bold">{dashboardStats.high_priority_contacts || 0}</div>
                      <div className="text-sm text-gray-600">High Priority</div>
                    </CardContent>
                  </Card>
                  
                  <Card>
                    <CardContent className="p-6 text-center">
                      <Calendar className="w-8 h-8 text-green-600 mx-auto mb-2" />
                      <div className="text-2xl font-bold">{dashboardStats.meeting_suggestions || 0}</div>
                      <div className="text-sm text-gray-600">Meeting Suggestions</div>
                    </CardContent>
                  </Card>
                  
                  <Card>
                    <CardContent className="p-6 text-center">
                      <TrendingUp className="w-8 h-8 text-purple-600 mx-auto mb-2" />
                      <div className="text-2xl font-bold">85%</div>
                      <div className="text-sm text-gray-600">Success Rate</div>
                    </CardContent>
                  </Card>
                </div>
                
                <Card className="mt-6">
                  <CardHeader>
                    <CardTitle className="flex items-center">
                      <BarChart3 className="w-5 h-5 mr-2" />
                      ROI Projection
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div>
                        <div className="flex justify-between mb-2">
                          <span>Conference ROI</span>
                          <span className="font-semibold">{dashboardStats.roi_projection || '45% increase in qualified leads'}</span>
                        </div>
                        <Progress value={75} className="h-2" />
                      </div>
                      <p className="text-sm text-gray-600">
                        Based on your high-priority meetings and historical conference data
                      </p>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="outreach">
                <Card>
                  <CardHeader>
                    <CardTitle>AI-Generated Outreach Templates</CardTitle>
                    <p className="text-gray-600">Personalized templates for different contact types</p>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="border rounded-lg p-4">
                      <h4 className="font-medium mb-2">C-Level Executive Template</h4>
                      <div className="bg-gray-50 p-3 rounded text-sm">
                        "Hi [Name], I'm reaching out because [Company] and [Their Company] share similar challenges in [Industry]. 
                        I'd love to discuss how we might collaborate. Are you available for a brief coffee at [Conference]?"
                      </div>
                    </div>
                    
                    <div className="border rounded-lg p-4">
                      <h4 className="font-medium mb-2">Product Manager Template</h4>
                      <div className="bg-gray-50 p-3 rounded text-sm">
                        "Hello [Name], I noticed your work on [Specific Project] at [Company]. 
                        We're building solutions that could complement your initiatives. 
                        Would you be interested in a quick demo during [Conference]?"
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;