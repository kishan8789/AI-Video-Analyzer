'use client'

import { useState } from 'react'
import axios from 'axios'
import VideoCards from '@/components/VideoCards'
import ChatPanel from '@/components/ChatPanel'
import URLInput from '@/components/URLInput'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function Home() {
    const [videos, setVideos] = useState<any>(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [analyzed, setAnalyzed] = useState(false)
    const [conversation, setConversation] = useState<any[]>([])

    const handleAnalyze = async (youtubeUrl: string, instagramUrl: string) => {
        setLoading(true)
        setError(null)

        try {
            const response = await axios.post(`${API_URL}/api/videos/analyze`, {
                youtube_url: youtubeUrl,
                instagram_url: instagramUrl,
            })

            if (response.data.status === 'success') {
                setVideos(response.data.videos)
                setAnalyzed(true)
                setConversation([])
            }
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Error analyzing videos. Please check the URLs.')
            console.error(err)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-4 md:p-8">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="text-center mb-12">
                    <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
                        🎥 RAG Video Chatbot
                    </h1>
                    <p className="text-xl text-purple-200">
                        Compare YouTube & Instagram videos with AI-powered insights
                    </p>
                </div>

                {/* Input Section */}
                {!analyzed ? (
                    <URLInput onAnalyze={handleAnalyze} loading={loading} error={error} />
                ) : (
                    <button
                        onClick={() => setAnalyzed(false)}
                        className="mb-8 px-6 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition"
                    >
                        Analyze Different Videos
                    </button>
                )}

                {/* Main Content */}
                {analyzed && videos && (
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                        {/* Videos Section */}
                        <div className="lg:col-span-1">
                            <VideoCards videos={videos} />
                        </div>

                        {/* Chat Section */}
                        <div className="lg:col-span-2">
                            <ChatPanel
                                conversation={conversation}
                                onConversationChange={setConversation}
                                videoIds={['A', 'B']}
                            />
                        </div>
                    </div>
                )}

                {/* Loading State */}
                {loading && (
                    <div className="flex items-center justify-center min-h-96">
                        <div className="text-center">
                            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-purple-500 mx-auto mb-4"></div>
                            <p className="text-white text-lg">Analyzing videos...</p>
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}
