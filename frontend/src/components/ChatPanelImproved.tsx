

'use client'

import { useState, useRef, useEffect } from 'react'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface Message {
    role: 'user' | 'assistant'
    content: string
    sources?: any[]
}

interface ChatPanelProps {
    conversation: Message[]
    onConversationChange: (conversation: Message[]) => void
    videoIds: string[]
}

export default function ChatPanelImproved({
    conversation,
    onConversationChange,
    videoIds,
}: ChatPanelProps) {
    const [input, setInput] = useState('')
    const [loading, setLoading] = useState(false)
    const messagesEndRef = useRef<HTMLDivElement>(null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }

    useEffect(() => {
        scrollToBottom()
    }, [conversation])

    const handleSendMessage = async (e: React.FormEvent) => {
        e.preventDefault()
        if (!input.trim()) return

        const userMessage: Message = { role: 'user', content: input }
        const updatedConversation = [...conversation, userMessage]
        onConversationChange(updatedConversation)
        setInput('')
        setLoading(true)

        try {
            const response = await fetch(`${API_URL}/api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: input,
                    video_ids: videoIds,
                    conversation_history: conversation,
                }),
            })

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)

            const reader = response.body?.getReader()
            if (!reader) throw new Error('No response body')

            const decoder = new TextDecoder()
            let fullResponse = ''
            let assistantMessage: Message = { role: 'assistant', content: '', sources: [] }

            while (true) {
                const { done, value } = await reader.read()
                if (done) break

                const text = decoder.decode(value, { stream: true })
                const lines = text.split('\n')

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        try {
                            const data = JSON.parse(line.slice(6))
                            if (data.content) {
                                fullResponse += data.content
                            } else if (data.error) {
                                fullResponse = data.error
                            }
                            assistantMessage.content = fullResponse
                            onConversationChange([...updatedConversation, assistantMessage])
                        } catch (e) {
                            // Ignore JSON parse errors
                        }
                    }
                }
            }
        } catch (error) {
            console.error('Chat error:', error)
            const errorMessage: Message = {
                role: 'assistant',
                content: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
            }
            onConversationChange([...updatedConversation, errorMessage])
        } finally {
            setLoading(false)
        }
    }

    const suggestedQuestions = [
        'Why did Video A get more engagement than Video B?',
        "What's the engagement rate of each video?",
        'Compare the hooks in the first 5 seconds',
        'Who is the creator of Video B and what is their follower count?',
        'Suggest improvements for B based on what worked in A',
    ]

    return (
        <div className="bg-slate-800 rounded-lg shadow-xl border border-purple-500/30 flex flex-col h-[600px]">
            <div className="bg-gradient-to-r from-purple-600 to-pink-600 px-6 py-4 rounded-t-lg">
                <h3 className="text-xl font-bold text-white">Chat with AI</h3>
            </div>

            <div className="flex-1 overflow-y-auto p-6 space-y-4">
                {conversation.length === 0 ? (
                    <div className="h-full flex flex-col items-center justify-center text-center">
                        <p className="text-gray-400 mb-6">Start by asking a question about the videos</p>
                        <div className="space-y-2">
                            {suggestedQuestions.map((q, i) => (
                                <button
                                    key={i}
                                    onClick={() => setInput(q)}
                                    className="block w-full text-left px-4 py-2 rounded-lg bg-slate-700 hover:bg-slate-600 text-gray-300 text-sm transition"
                                >
                                    {q}
                                </button>
                            ))}
                        </div>
                    </div>
                ) : (
                    conversation.map((msg, i) => (
                        <div
                            key={i}
                            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                        >
                            <div
                                className={`max-w-xs lg:max-w-md px-4 py-3 rounded-lg ${msg.role === 'user'
                                    ? 'bg-purple-600 text-white'
                                    : 'bg-slate-700 text-gray-100'
                                    }`}
                            >
                                <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                                {msg.sources && msg.sources.length > 0 && (
                                    <div className="mt-2 pt-2 border-t border-slate-600 text-xs opacity-75">
                                        Sources: {msg.sources.map((s) => `Video ${s.video_id}`).join(', ')}
                                    </div>
                                )}
                            </div>
                        </div>
                    ))
                )}
                <div ref={messagesEndRef} />
            </div>

            <form onSubmit={handleSendMessage} className="border-t border-slate-700 p-4 rounded-b-lg bg-slate-900">
                <div className="flex gap-2">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask about the videos..."
                        disabled={loading}
                        className="flex-1 px-4 py-2 rounded-lg bg-slate-700 text-white placeholder-gray-400 border border-slate-600 focus:outline-none focus:ring-2 focus:ring-purple-500 disabled:opacity-50"
                    />
                    <button
                        type="submit"
                        disabled={loading || !input.trim()}
                        className="px-6 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed font-semibold"
                    >
                        {loading ? '...' : 'Send'}
                    </button>
                </div>
            </form>
        </div>
    )
}
