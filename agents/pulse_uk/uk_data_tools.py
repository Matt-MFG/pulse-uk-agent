"""
UK Data Collection Tools for PULSE Agent
Real-time data fetching from Reddit, YouTube, and Guardian APIs
"""

import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import praw
from googleapiclient.discovery import build
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class UKDataCollector:
    """Collector for real UK cultural data"""

    def __init__(self):
        """Initialize API clients"""
        # Reddit client
        self.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT")
        )

        # YouTube client
        self.youtube = build('youtube', 'v3', developerKey=os.getenv("YOUTUBE_API_KEY"))

        # Guardian API key
        self.guardian_key = os.getenv("GUARDIAN_API_KEY")

    def get_reddit_trends(self, subreddit: str = "CasualUK", limit: int = 10) -> List[Dict]:
        """Get trending posts from UK subreddits"""
        try:
            posts = []
            for submission in self.reddit.subreddit(subreddit).hot(limit=limit):
                posts.append({
                    "title": submission.title,
                    "subreddit": submission.subreddit.display_name,
                    "score": submission.score,
                    "comments": submission.num_comments,
                    "created": datetime.fromtimestamp(submission.created_utc).isoformat(),
                    "url": f"https://reddit.com{submission.permalink}",
                    "author": str(submission.author),
                    "text": submission.selftext[:500] if submission.selftext else None,
                    "source": f"Reddit r/{submission.subreddit.display_name}",
                    "source_type": "social_media"
                })
            return posts
        except Exception as e:
            return [{"error": f"Reddit API error: {str(e)}"}]

    def get_uk_subreddits_trends(self) -> Dict[str, List[Dict]]:
        """Get trends from multiple UK subreddits"""
        uk_subreddits = [
            "CasualUK",
            "unitedkingdom",
            "britishproblems",
            "AskUK",
            "London"
        ]

        all_trends = {}
        for sub in uk_subreddits:
            try:
                all_trends[sub] = self.get_reddit_trends(sub, limit=5)
            except:
                all_trends[sub] = []

        return all_trends

    def get_youtube_trends(self, max_results: int = 10) -> List[Dict]:
        """Get trending YouTube videos in UK"""
        try:
            request = self.youtube.videos().list(
                part="snippet,statistics",
                chart="mostPopular",
                regionCode="GB",
                maxResults=max_results
            )
            response = request.execute()

            videos = []
            for item in response.get('items', []):
                videos.append({
                    "title": item['snippet']['title'],
                    "channel": item['snippet']['channelTitle'],
                    "views": int(item['statistics'].get('viewCount', 0)),
                    "likes": int(item['statistics'].get('likeCount', 0)),
                    "comments": int(item['statistics'].get('commentCount', 0)),
                    "published": item['snippet']['publishedAt'],
                    "description": item['snippet']['description'][:300],
                    "tags": item['snippet'].get('tags', [])[:5],
                    "category": item['snippet'].get('categoryId'),
                    "url": f"https://youtube.com/watch?v={item['id']}",
                    "source": f"YouTube - {item['snippet']['channelTitle']}",
                    "source_type": "video_platform"
                })
            return videos
        except Exception as e:
            return [{"error": f"YouTube API error: {str(e)}"}]

    def get_guardian_news(self, query: str = "UK", section: Optional[str] = None, page_size: int = 10) -> List[Dict]:
        """Get latest UK news from The Guardian"""
        try:
            params = {
                "api-key": self.guardian_key,
                "q": query,
                "page-size": page_size,
                "order-by": "newest",
                "show-fields": "headline,trailText,thumbnail"
            }

            if section:
                params["section"] = section

            response = requests.get(
                "https://content.guardianapis.com/search",
                params=params
            )

            if response.status_code == 200:
                data = response.json()
                articles = []
                for article in data['response']['results']:
                    articles.append({
                        "title": article['webTitle'],
                        "section": article['sectionName'],
                        "published": article['webPublicationDate'],
                        "url": article['webUrl'],
                        "type": article['type'],
                        "pillar": article.get('pillarName', 'News'),
                        "description": article.get('fields', {}).get('trailText', ''),
                        "thumbnail": article.get('fields', {}).get('thumbnail', ''),
                        "source": f"The Guardian - {article['sectionName']}",
                        "source_type": "news_media"
                    })
                return articles
            else:
                return [{"error": f"Guardian API returned status {response.status_code}"}]
        except Exception as e:
            return [{"error": f"Guardian API error: {str(e)}"}]

    def get_uk_news_by_category(self) -> Dict[str, List[Dict]]:
        """Get UK news organized by category"""
        categories = {
            "politics": "politics",
            "business": "business",
            "culture": "culture",
            "sport": "sport",
            "technology": "technology"
        }

        news_by_category = {}
        for name, section in categories.items():
            news_by_category[name] = self.get_guardian_news(
                query="UK",
                section=section,
                page_size=5
            )

        return news_by_category

    def get_comprehensive_uk_trends(self) -> Dict[str, Any]:
        """Get comprehensive UK trends from all sources"""
        print("Fetching comprehensive UK trends...")

        trends = {
            "timestamp": datetime.now().isoformat(),
            "reddit": {
                "top_posts": self.get_reddit_trends("CasualUK", 10),
                "by_subreddit": self.get_uk_subreddits_trends()
            },
            "youtube": {
                "trending_videos": self.get_youtube_trends(10)
            },
            "guardian": {
                "latest_news": self.get_guardian_news("UK", page_size=10),
                "by_category": self.get_uk_news_by_category()
            }
        }

        # Add summary statistics
        trends["summary"] = {
            "total_reddit_posts": sum(len(posts) for posts in trends["reddit"]["by_subreddit"].values()),
            "total_youtube_videos": len(trends["youtube"]["trending_videos"]),
            "total_news_articles": sum(len(articles) for articles in trends["guardian"]["by_category"].values()),
            "data_sources": ["Reddit", "YouTube", "The Guardian"],
            "region": "United Kingdom"
        }

        return trends


# ADK Tool Functions
def fetch_uk_reddit_trends(subreddit: str = "CasualUK", limit: int = 10) -> str:
    """Fetch trending posts from UK subreddits.

    Args:
        subreddit: Name of the subreddit (default: CasualUK)
        limit: Number of posts to fetch (default: 10)

    Returns:
        JSON string of trending posts
    """
    collector = UKDataCollector()
    trends = collector.get_reddit_trends(subreddit, limit)
    return json.dumps(trends, indent=2)


def fetch_uk_youtube_trends(max_results: int = 10) -> str:
    """Fetch trending YouTube videos in the UK.

    Args:
        max_results: Number of videos to fetch (default: 10)

    Returns:
        JSON string of trending videos
    """
    collector = UKDataCollector()
    trends = collector.get_youtube_trends(max_results)
    return json.dumps(trends, indent=2)


def fetch_uk_news(query: str = "UK", section: Optional[str] = None, limit: int = 10) -> str:
    """Fetch latest UK news from The Guardian.

    Args:
        query: Search query (default: UK)
        section: News section to filter by (optional)
        limit: Number of articles to fetch (default: 10)

    Returns:
        JSON string of news articles
    """
    collector = UKDataCollector()
    news = collector.get_guardian_news(query, section, limit)
    return json.dumps(news, indent=2)


def fetch_comprehensive_uk_trends() -> str:
    """Fetch comprehensive UK trends from all sources (Reddit, YouTube, Guardian).

    Returns:
        JSON string of all UK trends
    """
    collector = UKDataCollector()
    trends = collector.get_comprehensive_uk_trends()
    return json.dumps(trends, indent=2)


# COMMENTED OUT - This is just for testing, not used by the agent
# if __name__ == "__main__":
#     # Test the collector
#     collector = UKDataCollector()
#
#     print("\n=== Reddit Trends (CasualUK) ===")
#     reddit_trends = collector.get_reddit_trends("CasualUK", 3)
#     for post in reddit_trends:
#         if "error" not in post:
#             print(f"- {post['title']} (Score: {post['score']})")
#
#     print("\n=== YouTube Trending ===")
#     youtube_trends = collector.get_youtube_trends(3)
#     for video in youtube_trends:
#         if "error" not in video:
#             print(f"- {video['title']} (Views: {video['views']:,})")
#
#     print("\n=== Guardian News ===")
#     news = collector.get_guardian_news("UK", page_size=3)
#     for article in news:
#         if "error" not in article:
#             print(f"- {article['title']}")