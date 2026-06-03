import type { Metadata } from 'next'
import '../globals.css'

export const metadata: Metadata = {
    title: 'RAG Video Chatbot',
    description: 'Compare videos with AI-powered RAG chatbot',
}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="en">
            <body>{children}</body>
        </html>
    )
}
