'use client'

interface VideoCardsProps {
    videos: {
        A: {
            title: string
            platform: string
            creator: string
            engagement_rate: number
            views: number
            likes: number
        }
        B: {
            title: string
            platform: string
            creator: string
            engagement_rate: number
            views: number
            likes: number
        }
    }
}

export default function VideoCards({ videos }: VideoCardsProps) {
    const getMetrics = (video: any) => [
        { label: 'Views', value: video.views.toLocaleString() },
        { label: 'Likes', value: video.likes.toLocaleString() },
        { label: 'Engagement', value: `${video.engagement_rate.toFixed(2)}%` },
    ]

    return (
        <div className="space-y-6">
            {Object.entries(videos).map(([videoId, video]: [string, any]) => (
                <div
                    key={videoId}
                    className="bg-slate-800 rounded-lg overflow-hidden shadow-xl border border-purple-500/30 hover:border-purple-500 transition"
                >
                    <div className="bg-gradient-to-r from-purple-600 to-pink-600 px-4 py-3">
                        <h3 className="text-2xl font-bold text-white">Video {videoId}</h3>
                    </div>

                    <div className="p-6 space-y-4">
                        {/* Title */}
                        <div>
                            <h4 className="text-lg font-semibold text-white truncate">
                                {video.title || 'N/A'}
                            </h4>
                            <p className="text-sm text-gray-400">{video.platform.toUpperCase()}</p>
                        </div>

                        {/* Creator */}
                        <div>
                            <p className="text-sm text-gray-300">
                                <span className="font-semibold">Creator:</span> {video.creator}
                            </p>
                        </div>

                        {/* Metrics */}
                        <div className="grid grid-cols-3 gap-3">
                            {getMetrics(video).map((metric) => (
                                <div
                                    key={metric.label}
                                    className="bg-slate-700 rounded-lg p-3 text-center"
                                >
                                    <p className="text-xs text-gray-400 uppercase font-semibold">
                                        {metric.label}
                                    </p>
                                    <p className="text-lg font-bold text-purple-400 mt-1">
                                        {metric.value}
                                    </p>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            ))}

            {/* Comparison Summary */}
            <div className="bg-slate-800 rounded-lg p-6 border border-purple-500/30">
                <h4 className="text-lg font-semibold text-white mb-4">Quick Comparison</h4>
                <div className="space-y-3">
                    <div className="flex justify-between items-center">
                        <span className="text-gray-300">Better Engagement:</span>
                        <span className="font-bold text-purple-400">
                            Video {
                                videos.A.engagement_rate > videos.B.engagement_rate ? 'A' : 'B'
                            }
                        </span>
                    </div>
                    <div className="flex justify-between items-center">
                        <span className="text-gray-300">More Views:</span>
                        <span className="font-bold text-purple-400">
                            Video {videos.A.views > videos.B.views ? 'A' : 'B'}
                        </span>
                    </div>
                    <div className="flex justify-between items-center">
                        <span className="text-gray-300">More Likes:</span>
                        <span className="font-bold text-purple-400">
                            Video {videos.A.likes > videos.B.likes ? 'A' : 'B'}
                        </span>
                    </div>
                </div>
            </div>
        </div>
    )
}
