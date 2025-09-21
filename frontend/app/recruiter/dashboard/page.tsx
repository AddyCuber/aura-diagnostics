"use client"

import { useState, useEffect, useRef } from "react"
import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Textarea } from "@/components/ui/textarea"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { 
  Users, 
  Briefcase, 
  TrendingUp, 
  Star, 
  Clock, 
  MapPin, 
  Mail, 
  Phone,
  Github,
  ExternalLink,
  Plus,
  Search,
  Filter,
  BarChart3,
  PieChart,
  Target
} from "lucide-react"
import { SharedHeader } from "@/components/shared-header"

interface JobPosting {
  id: string
  title: string
  department: string
  location: string
  type: string
  salary: string
  postedDate: string
  applicants: number
  status: 'active' | 'paused' | 'closed'
  description: string
  requirements: string[]
  candidates: Candidate[]
}

interface Candidate {
  id: string
  name: string
  email: string
  phone: string
  location: string
  title: string
  experience: string
  skills: string[]
  matchScore: number
  resumeUrl?: string
  githubUrl?: string
  linkedinUrl?: string
  appliedDate: string
  status: 'new' | 'reviewing' | 'shortlisted' | 'interviewed' | 'rejected' | 'hired'
}

export default function RecruiterDashboard() {
  const [activeSection, setActiveSection] = useState('overview')
  const [selectedJob, setSelectedJob] = useState<string | null>(null)
  const [searchTerm, setSearchTerm] = useState('')
  const sectionsRef = useRef<(HTMLElement | null)[]>([])

  // Mock data for demonstration
  const [jobPostings] = useState<JobPosting[]>([
    {
      id: 'job-1',
      title: 'Senior Frontend Developer',
      department: 'Engineering',
      location: 'San Francisco, CA',
      type: 'Full-time',
      salary: '$120k - $160k',
      postedDate: '2024-01-15',
      applicants: 24,
      status: 'active',
      description: 'We are looking for a Senior Frontend Developer to join our engineering team...',
      requirements: ['React', 'TypeScript', 'Next.js', '5+ years experience'],
      candidates: [
        {
          id: 'candidate-1',
          name: 'Alex Johnson',
          email: 'alex.johnson@email.com',
          phone: '+1 (555) 123-4567',
          location: 'San Francisco, CA',
          title: 'Frontend Developer',
          experience: '6 years',
          skills: ['React', 'TypeScript', 'Next.js', 'Node.js', 'GraphQL'],
          matchScore: 92,
          githubUrl: 'https://github.com/alexjohnson',
          appliedDate: '2024-01-16',
          status: 'shortlisted'
        },
        {
          id: 'candidate-2',
          name: 'Sarah Chen',
          email: 'sarah.chen@email.com',
          phone: '+1 (555) 987-6543',
          location: 'Seattle, WA',
          title: 'Full Stack Developer',
          experience: '4 years',
          skills: ['React', 'JavaScript', 'Python', 'AWS', 'Docker'],
          matchScore: 85,
          appliedDate: '2024-01-17',
          status: 'reviewing'
        },
        {
          id: 'candidate-3',
          name: 'Michael Rodriguez',
          email: 'michael.r@email.com',
          phone: '+1 (555) 456-7890',
          location: 'Austin, TX',
          title: 'React Developer',
          experience: '3 years',
          skills: ['React', 'TypeScript', 'Redux', 'Jest', 'CSS'],
          matchScore: 78,
          appliedDate: '2024-01-18',
          status: 'new'
        }
      ]
    },
    {
      id: 'job-2',
      title: 'Backend Engineer',
      department: 'Engineering',
      location: 'Remote',
      type: 'Full-time',
      salary: '$110k - $150k',
      postedDate: '2024-01-10',
      applicants: 18,
      status: 'active',
      description: 'Join our backend team to build scalable microservices...',
      requirements: ['Python', 'Django', 'PostgreSQL', '4+ years experience'],
      candidates: [
        {
          id: 'candidate-4',
          name: 'David Kim',
          email: 'david.kim@email.com',
          phone: '+1 (555) 321-9876',
          location: 'New York, NY',
          title: 'Backend Developer',
          experience: '5 years',
          skills: ['Python', 'Django', 'PostgreSQL', 'Redis', 'Docker'],
          matchScore: 88,
          appliedDate: '2024-01-11',
          status: 'interviewed'
        }
      ]
    },
    {
      id: 'job-3',
      title: 'Product Designer',
      department: 'Design',
      location: 'Los Angeles, CA',
      type: 'Full-time',
      salary: '$90k - $130k',
      postedDate: '2024-01-12',
      applicants: 31,
      status: 'active',
      description: 'We need a creative Product Designer to enhance user experience...',
      requirements: ['Figma', 'UI/UX Design', 'Prototyping', '3+ years experience'],
      candidates: []
    }
  ])

  const analytics = {
    totalJobs: jobPostings.length,
    activeJobs: jobPostings.filter(job => job.status === 'active').length,
    totalApplicants: jobPostings.reduce((sum, job) => sum + job.applicants, 0),
    avgMatchScore: 84,
    hireRate: 12,
    timeToHire: 18
  }

  useEffect(() => {
    const observerOptions = {
      threshold: 0.3,
      rootMargin: '-20% 0px -20% 0px'
    }

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const sectionId = entry.target.id
          setActiveSection(sectionId)
          
          // Animate section on scroll
          entry.target.style.opacity = '1'
          entry.target.style.transform = 'translateY(0)'
        }
      })
    }, observerOptions)

    sectionsRef.current.forEach((section) => {
      if (section) {
        section.style.opacity = '0'
        section.style.transform = 'translateY(20px)'
        section.style.transition = 'opacity 0.8s ease, transform 0.8s ease'
        observer.observe(section)
      }
    })

    return () => observer.disconnect()
  }, [])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'new': return 'bg-blue-100 text-blue-800'
      case 'reviewing': return 'bg-yellow-100 text-yellow-800'
      case 'shortlisted': return 'bg-green-100 text-green-800'
      case 'interviewed': return 'bg-purple-100 text-purple-800'
      case 'rejected': return 'bg-red-100 text-red-800'
      case 'hired': return 'bg-emerald-100 text-emerald-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getJobStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800'
      case 'paused': return 'bg-yellow-100 text-yellow-800'
      case 'closed': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="min-h-screen bg-background text-foreground relative">
      <SharedHeader 
        showAuth={false} 
        contextText="Streamline your hiring process with AI-powered candidate matching and analytics"
      />
      
      {/* Right-side Navigation */}
      <nav className="fixed right-8 top-1/2 -translate-y-1/2 z-10 hidden lg:block">
        <div className="flex flex-col gap-4">
          {['overview', 'jobs', 'candidates', 'analytics'].map((section) => (
            <button
              key={section}
              onClick={() => document.getElementById(section)?.scrollIntoView({ behavior: 'smooth' })}
              className={`w-2 h-8 rounded-full transition-all duration-500 ${
                activeSection === section ? 'bg-foreground' : 'bg-muted-foreground/30 hover:bg-muted-foreground/60'
              }`}
              aria-label={`Navigate to ${section}`}
            />
          ))}
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-8 lg:px-16">
        {/* Overview Section */}
        <header
          id="overview"
          ref={(el) => (sectionsRef.current[0] = el)}
          className="min-h-screen flex items-center opacity-0"
        >
          <div className="grid lg:grid-cols-5 gap-16 w-full">
            <div className="lg:col-span-3 space-y-8">
              <div className="space-y-2">
                <div className="text-sm text-muted-foreground font-mono tracking-wider">RECRUITER DASHBOARD / 2025</div>
                <h1 className="text-6xl lg:text-7xl font-light tracking-tight">
                  Talent
                  <br />
                  <span className="text-muted-foreground">Pipeline</span>
                </h1>
              </div>

              <div className="space-y-6 max-w-md">
                <p className="text-xl text-muted-foreground leading-relaxed">
                  Discover exceptional talent through
                  <span className="text-foreground"> AI-powered matching</span> and
                  <span className="text-foreground"> data-driven insights</span> that streamline your hiring process.
                </p>

                <div className="flex items-center gap-4 text-sm text-muted-foreground">
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                    {analytics.activeJobs} active positions
                  </div>
                  <div>{analytics.totalApplicants} total applicants</div>
                </div>
              </div>
            </div>

            <div className="lg:col-span-2 flex flex-col justify-end space-y-8">
              {/* Bento Grid - Analytics Overview */}
              <div className="grid grid-cols-2 gap-4">
                <Card className="p-4 hover:shadow-lg transition-all duration-300">
                  <div className="space-y-2">
                    <div className="text-2xl font-bold text-foreground">{analytics.avgMatchScore}%</div>
                    <div className="text-xs text-muted-foreground">Avg Match Score</div>
                  </div>
                </Card>
                
                <Card className="p-4 hover:shadow-lg transition-all duration-300">
                  <div className="space-y-2">
                    <div className="text-2xl font-bold text-foreground">{analytics.hireRate}%</div>
                    <div className="text-xs text-muted-foreground">Hire Rate</div>
                  </div>
                </Card>
                
                <Card className="p-4 hover:shadow-lg transition-all duration-300">
                  <div className="space-y-2">
                    <div className="text-2xl font-bold text-foreground">{analytics.timeToHire}</div>
                    <div className="text-xs text-muted-foreground">Days to Hire</div>
                  </div>
                </Card>
                
                <Card className="p-4 hover:shadow-lg transition-all duration-300">
                  <div className="space-y-2">
                    <div className="text-2xl font-bold text-foreground">{analytics.totalJobs}</div>
                    <div className="text-xs text-muted-foreground">Total Jobs</div>
                  </div>
                </Card>
              </div>

              <div className="space-y-4">
                <div className="text-sm text-muted-foreground font-mono">QUICK ACTIONS</div>
                <div className="flex flex-wrap gap-2">
                  <Button size="sm" className="text-xs">
                    <Plus className="w-3 h-3 mr-1" />
                    New Job
                  </Button>
                  <Button size="sm" variant="outline" className="text-xs">
                    <Search className="w-3 h-3 mr-1" />
                    Find Talent
                  </Button>
                  <Button size="sm" variant="outline" className="text-xs">
                    <BarChart3 className="w-3 h-3 mr-1" />
                    Reports
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Jobs Section */}
        <section
          id="jobs"
          ref={(el) => (sectionsRef.current[1] = el)}
          className="min-h-screen py-32 opacity-0"
        >
          <div className="space-y-16">
            <div className="flex items-end justify-between">
              <h2 className="text-4xl font-light">Job Postings</h2>
              <div className="text-sm text-muted-foreground font-mono flex items-center gap-2">
                <Briefcase className="w-4 h-4" />
                TALENT ACQUISITION
              </div>
            </div>

            <div className="grid gap-6">
              {jobPostings.map((job) => (
                <Card key={job.id} className="group hover:shadow-lg transition-all duration-300">
                  <CardContent className="p-6">
                    <div className="flex justify-between items-start mb-4">
                      <div className="space-y-2">
                        <div className="flex items-center gap-3">
                          <h3 className="text-xl font-semibold">{job.title}</h3>
                          <Badge className={getJobStatusColor(job.status)}>
                            {job.status}
                          </Badge>
                        </div>
                        <div className="flex items-center gap-4 text-sm text-muted-foreground">
                          <span className="flex items-center gap-1">
                            <MapPin className="w-3 h-3" />
                            {job.location}
                          </span>
                          <span className="flex items-center gap-1">
                            <Clock className="w-3 h-3" />
                            {job.type}
                          </span>
                          <span className="flex items-center gap-1">
                            <Users className="w-3 h-3" />
                            {job.applicants} applicants
                          </span>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-lg font-semibold">{job.salary}</div>
                        <div className="text-sm text-muted-foreground">Posted {new Date(job.postedDate).toLocaleDateString()}</div>
                      </div>
                    </div>
                    
                    <div className="flex flex-wrap gap-2 mb-4">
                      {job.requirements.map((req, index) => (
                        <Badge key={index} variant="outline" className="text-xs">
                          {req}
                        </Badge>
                      ))}
                    </div>
                    
                    <div className="flex justify-between items-center">
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={() => setSelectedJob(selectedJob === job.id ? null : job.id)}
                      >
                        {selectedJob === job.id ? 'Hide' : 'View'} Candidates
                      </Button>
                      <div className="flex gap-2">
                        <Button size="sm" variant="outline">
                          Edit
                        </Button>
                        <Button size="sm">
                          Manage
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </section>

        {/* Candidates Section */}
        <section
          id="candidates"
          ref={(el) => (sectionsRef.current[2] = el)}
          className="min-h-screen py-32 opacity-0"
        >
          <div className="space-y-16">
            <div className="flex items-end justify-between">
              <h2 className="text-4xl font-light">Candidate Pipeline</h2>
              <div className="text-sm text-muted-foreground font-mono flex items-center gap-2">
                <Users className="w-4 h-4" />
                TALENT POOL
              </div>
            </div>

            {selectedJob && (
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <h3 className="text-2xl font-semibold">
                    Candidates for {jobPostings.find(job => job.id === selectedJob)?.title}
                  </h3>
                  <div className="flex items-center gap-2">
                    <Input 
                      placeholder="Search candidates..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="w-64"
                    />
                    <Button size="sm" variant="outline">
                      <Filter className="w-4 h-4" />
                    </Button>
                  </div>
                </div>

                <div className="grid gap-4">
                  {jobPostings
                    .find(job => job.id === selectedJob)?.candidates
                    .sort((a, b) => b.matchScore - a.matchScore)
                    .map((candidate) => (
                    <Card key={candidate.id} className="group hover:shadow-lg transition-all duration-300">
                      <CardContent className="p-6">
                        <div className="flex justify-between items-start">
                          <div className="flex-1 space-y-3">
                            <div className="flex items-center gap-4">
                              <div>
                                <h4 className="text-lg font-semibold">{candidate.name}</h4>
                                <p className="text-muted-foreground">{candidate.title}</p>
                              </div>
                              <Badge className={getStatusColor(candidate.status)}>
                                {candidate.status}
                              </Badge>
                            </div>
                            
                            <div className="flex items-center gap-6 text-sm text-muted-foreground">
                              <span className="flex items-center gap-1">
                                <Mail className="w-3 h-3" />
                                {candidate.email}
                              </span>
                              <span className="flex items-center gap-1">
                                <Phone className="w-3 h-3" />
                                {candidate.phone}
                              </span>
                              <span className="flex items-center gap-1">
                                <MapPin className="w-3 h-3" />
                                {candidate.location}
                              </span>
                            </div>
                            
                            <div className="flex flex-wrap gap-2">
                              {candidate.skills.map((skill, index) => (
                                <Badge key={index} variant="outline" className="text-xs">
                                  {skill}
                                </Badge>
                              ))}
                            </div>
                          </div>
                          
                          <div className="text-right space-y-3">
                            <div className="space-y-1">
                              <div className="text-2xl font-bold text-primary">{candidate.matchScore}%</div>
                              <div className="text-xs text-muted-foreground">Match Score</div>
                            </div>
                            
                            <div className="flex gap-2">
                              {candidate.githubUrl && (
                                <Button size="sm" variant="outline">
                                  <Github className="w-3 h-3" />
                                </Button>
                              )}
                              <Button size="sm" variant="outline">
                                <ExternalLink className="w-3 h-3" />
                              </Button>
                            </div>
                            
                            <div className="flex gap-2">
                              <Button size="sm" variant="outline">
                                Contact
                              </Button>
                              <Button size="sm">
                                Review
                              </Button>
                            </div>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>
            )}

            {!selectedJob && (
              <div className="text-center py-16">
                <Users className="w-16 h-16 mx-auto text-muted-foreground mb-4" />
                <h3 className="text-xl font-semibold mb-2">Select a Job to View Candidates</h3>
                <p className="text-muted-foreground">Choose a job posting above to see ranked candidates and their match scores</p>
              </div>
            )}
          </div>
        </section>

        {/* Analytics Section */}
        <section
          id="analytics"
          ref={(el) => (sectionsRef.current[3] = el)}
          className="min-h-screen py-32 opacity-0"
        >
          <div className="space-y-16">
            <div className="flex items-end justify-between">
              <h2 className="text-4xl font-light">Analytics & Insights</h2>
              <div className="text-sm text-muted-foreground font-mono flex items-center gap-2">
                <TrendingUp className="w-4 h-4" />
                PERFORMANCE METRICS
              </div>
            </div>

            {/* Bento Grid Layout for Analytics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {/* Large metric cards */}
              <Card className="md:col-span-2 lg:col-span-2 p-6 hover:shadow-lg transition-all duration-300">
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-semibold">Hiring Funnel</h3>
                    <TrendingUp className="w-5 h-5 text-muted-foreground" />
                  </div>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-muted-foreground">Applications</span>
                      <span className="font-semibold">{analytics.totalApplicants}</span>
                    </div>
                    <Progress value={100} className="h-2" />
                    
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-muted-foreground">Screening</span>
                      <span className="font-semibold">{Math.round(analytics.totalApplicants * 0.6)}</span>
                    </div>
                    <Progress value={60} className="h-2" />
                    
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-muted-foreground">Interviews</span>
                      <span className="font-semibold">{Math.round(analytics.totalApplicants * 0.3)}</span>
                    </div>
                    <Progress value={30} className="h-2" />
                    
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-muted-foreground">Offers</span>
                      <span className="font-semibold">{Math.round(analytics.totalApplicants * 0.12)}</span>
                    </div>
                    <Progress value={12} className="h-2" />
                  </div>
                </div>
              </Card>

              <Card className="p-6 hover:shadow-lg transition-all duration-300">
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-semibold">Time to Hire</h3>
                    <Clock className="w-5 h-5 text-muted-foreground" />
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-primary">{analytics.timeToHire}</div>
                    <div className="text-sm text-muted-foreground">days average</div>
                  </div>
                  <div className="text-xs text-green-600 text-center">↓ 15% from last month</div>
                </div>
              </Card>

              <Card className="p-6 hover:shadow-lg transition-all duration-300">
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-semibold">Success Rate</h3>
                    <Target className="w-5 h-5 text-muted-foreground" />
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-primary">{analytics.hireRate}%</div>
                    <div className="text-sm text-muted-foreground">hire rate</div>
                  </div>
                  <div className="text-xs text-green-600 text-center">↑ 8% from last month</div>
                </div>
              </Card>

              <Card className="md:col-span-2 lg:col-span-2 p-6 hover:shadow-lg transition-all duration-300">
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-semibold">Top Skills in Demand</h3>
                    <Star className="w-5 h-5 text-muted-foreground" />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    {[
                      { skill: 'React', demand: 85 },
                      { skill: 'TypeScript', demand: 78 },
                      { skill: 'Python', demand: 72 },
                      { skill: 'Node.js', demand: 68 },
                      { skill: 'AWS', demand: 65 },
                      { skill: 'Docker', demand: 58 }
                    ].map((item, index) => (
                      <div key={index} className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span>{item.skill}</span>
                          <span className="text-muted-foreground">{item.demand}%</span>
                        </div>
                        <Progress value={item.demand} className="h-1" />
                      </div>
                    ))}
                  </div>
                </div>
              </Card>

              <Card className="p-6 hover:shadow-lg transition-all duration-300">
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-semibold">Quality Score</h3>
                    <PieChart className="w-5 h-5 text-muted-foreground" />
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-primary">{analytics.avgMatchScore}%</div>
                    <div className="text-sm text-muted-foreground">avg match</div>
                  </div>
                  <div className="text-xs text-green-600 text-center">↑ 12% from last month</div>
                </div>
              </Card>

              <Card className="p-6 hover:shadow-lg transition-all duration-300">
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-semibold">Active Jobs</h3>
                    <Briefcase className="w-5 h-5 text-muted-foreground" />
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-primary">{analytics.activeJobs}</div>
                    <div className="text-sm text-muted-foreground">positions open</div>
                  </div>
                  <div className="text-xs text-blue-600 text-center">2 new this week</div>
                </div>
              </Card>
            </div>
          </div>
        </section>
      </main>
    </div>
  )
}