import { useState } from 'react'

export interface GitHubUser {
  username: string
  name: string | null
  bio: string | null
  avatar: string
  profileUrl: string
  joinDate: string
}

export interface GitHubStats {
  totalRepos: number
  followers: number
  following: number
  recentActivity: number
}

export interface GitHubRepo {
  name: string
  description: string | null
  language: string | null
  stars: number
  forks: number
  url: string
  topics: string[]
}

export interface GitHubAnalysis {
  user: GitHubUser
  stats: GitHubStats
  languages: string[]
  topRepositories: GitHubRepo[]
  languageStats: { [key: string]: number }
}

export interface UseGitHubReturn {
  analysis: GitHubAnalysis | null
  loading: boolean
  error: string | null
  analyzeGitHub: (username: string, token?: string) => Promise<void>
  clearAnalysis: () => void
}

export function useGitHub(): UseGitHubReturn {
  const [analysis, setAnalysis] = useState<GitHubAnalysis | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const analyzeGitHub = async (username: string, token?: string) => {
    if (!username.trim()) {
      setError('Please enter a GitHub username')
      return
    }

    setLoading(true)
    setError(null)
    setAnalysis(null)

    try {
      const response = await fetch('/api/github', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: username.trim(), token: token?.trim() || '' }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'Failed to analyze GitHub profile')
      }

      setAnalysis(data)
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unexpected error occurred'
      setError(errorMessage)
      console.error('GitHub analysis error:', err)
    } finally {
      setLoading(false)
    }
  }

  const clearAnalysis = () => {
    setAnalysis(null)
    setError(null)
  }

  return {
    analysis,
    loading,
    error,
    analyzeGitHub,
    clearAnalysis,
  }
}