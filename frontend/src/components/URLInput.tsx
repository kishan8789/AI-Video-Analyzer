'use client'

import { useState } from 'react'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface URLInputProps {
    onAnalyze: (youtubeUrl: string, instagramUrl: string) => void
    loading: boolean
    error: string | null
}

export default function URLInput({ onAnalyze, loading, error }: URLInputProps) {
    const [youtubeUrl, setYoutubeUrl] = useState('')
    const [instagramUrl, setInstagramUrl] = useState('')

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        if (youtubeUrl.trim() && instagramUrl.trim()) {
            onAnalyze(youtubeUrl, instagramUrl)
        }
    }

    return (
        <div className="max-w-2xl mx-auto mb-12">
            <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                    <label className="block text-white font-medium mb-2">YouTube Video URL</label>
                    <input
                        type="url"
                        value={youtubeUrl}
                        onChange={(e) => setYoutubeUrl(e.target.value)}
                        placeholder="https://www.youtube.com/watch?v=..."
                        disabled={loading}
                        className="w-full px-4 py-3 rounded-lg bg-slate-800 text-white placeholder-gray-400 border border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-500 disabled:opacity-50"
                        required
                    />
                </div>

                <div>
                    <label className="block text-white font-medium mb-2">Instagram Reels URL</label>
                    <input
                        type="url"
                        value={instagramUrl}
                        onChange={(e) => setInstagramUrl(e.target.value)}
                        placeholder="https://www.instagram.com/reels/..."
                        disabled={loading}
                        className="w-full px-4 py-3 rounded-lg bg-slate-800 text-white placeholder-gray-400 border border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-500 disabled:opacity-50"
                        required
                    />
                </div>

                {error && (
                    <div className="p-4 bg-red-900 text-red-100 rounded-lg">
                        {error}
                    </div>
                )}

                <button
                    type="submit"
                    disabled={loading || !youtubeUrl.trim() || !instagramUrl.trim()}
                    className="w-full py-3 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-semibold rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    {loading ? 'Analyzing...' : 'Analyze Videos'}
                </button>
            </form>
        </div>
    )
}
