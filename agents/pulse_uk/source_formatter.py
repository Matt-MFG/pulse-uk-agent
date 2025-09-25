"""
Source Citation Formatter for PULSE UK Agent
Provides proper references and citations for all data sources
"""

from typing import List, Dict, Any
from datetime import datetime


class SourceCitationFormatter:
    """Formats and tracks sources for proper citation"""

    def __init__(self):
        self.sources_used = []
        self.citation_style = "harvard"  # UK academic standard

    def extract_and_format_sources(self, data: Any) -> Dict[str, Any]:
        """
        Extract sources from data and format them for citation
        Returns both inline citations and reference list
        """
        sources = {
            "inline_citations": [],
            "references": [],
            "source_summary": {
                "total_sources": 0,
                "by_type": {
                    "social_media": 0,
                    "news_media": 0,
                    "video_platform": 0
                }
            }
        }

        # Process different data structures
        if isinstance(data, dict):
            sources = self._process_dict_sources(data, sources)
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and item.get("source"):
                    sources = self._add_source(item, sources)

        # Generate reference list
        sources["references"] = self._generate_reference_list(sources["inline_citations"])

        return sources

    def _process_dict_sources(self, data: Dict, sources: Dict) -> Dict:
        """Process dictionary data for sources"""

        # Check for Reddit data
        if "reddit" in data:
            if "by_subreddit" in data["reddit"]:
                for subreddit, posts in data["reddit"]["by_subreddit"].items():
                    for post in posts:
                        if isinstance(post, dict):
                            post["source"] = f"Reddit r/{subreddit}"
                            post["source_type"] = "social_media"
                            sources = self._add_source(post, sources)

            if "top_posts" in data["reddit"]:
                for post in data["reddit"]["top_posts"]:
                    if isinstance(post, dict):
                        sources = self._add_source(post, sources)

        # Check for YouTube data
        if "youtube" in data:
            if "trending_videos" in data["youtube"]:
                for video in data["youtube"]["trending_videos"]:
                    if isinstance(video, dict):
                        sources = self._add_source(video, sources)

        # Check for Guardian data
        if "guardian" in data:
            if "latest_news" in data["guardian"]:
                for article in data["guardian"]["latest_news"]:
                    if isinstance(article, dict):
                        sources = self._add_source(article, sources)

            if "by_category" in data["guardian"]:
                for category, articles in data["guardian"]["by_category"].items():
                    for article in articles:
                        if isinstance(article, dict):
                            sources = self._add_source(article, sources)

        return sources

    def _add_source(self, item: Dict, sources: Dict) -> Dict:
        """Add a source to the citation list"""

        source_type = item.get("source_type", "unknown")

        # Create inline citation
        if source_type == "social_media":
            citation = self._format_social_media_citation(item)
        elif source_type == "news_media":
            citation = self._format_news_citation(item)
        elif source_type == "video_platform":
            citation = self._format_video_citation(item)
        else:
            citation = self._format_generic_citation(item)

        if citation:
            sources["inline_citations"].append(citation)
            sources["source_summary"]["total_sources"] += 1
            sources["source_summary"]["by_type"][source_type] = sources["source_summary"]["by_type"].get(source_type, 0) + 1

        return sources

    def _format_social_media_citation(self, item: Dict) -> Dict:
        """Format citation for social media source"""
        return {
            "type": "social_media",
            "platform": "Reddit",
            "author": item.get("author", "Anonymous"),
            "title": item.get("title", "Untitled")[:50] + "..." if len(item.get("title", "")) > 50 else item.get("title", ""),
            "subreddit": item.get("subreddit", "Unknown"),
            "date": item.get("created", datetime.now().isoformat())[:10],
            "url": item.get("url", ""),
            "engagement": f"{item.get('score', 0)} upvotes, {item.get('comments', 0)} comments",
            "inline": f"(r/{item.get('subreddit', 'Unknown')}, {item.get('created', '')[:10]})"
        }

    def _format_news_citation(self, item: Dict) -> Dict:
        """Format citation for news media source"""
        return {
            "type": "news_media",
            "publication": "The Guardian",
            "title": item.get("title", "Untitled")[:50] + "..." if len(item.get("title", "")) > 50 else item.get("title", ""),
            "section": item.get("section", "News"),
            "date": item.get("published", datetime.now().isoformat())[:10],
            "url": item.get("url", ""),
            "inline": f"(Guardian {item.get('section', 'News')}, {item.get('published', '')[:10]})"
        }

    def _format_video_citation(self, item: Dict) -> Dict:
        """Format citation for video platform source"""
        return {
            "type": "video_platform",
            "platform": "YouTube",
            "channel": item.get("channel", "Unknown Channel"),
            "title": item.get("title", "Untitled")[:50] + "..." if len(item.get("title", "")) > 50 else item.get("title", ""),
            "views": f"{item.get('views', 0):,}",
            "date": item.get("published", datetime.now().isoformat())[:10],
            "url": item.get("url", ""),
            "engagement": f"{item.get('likes', 0):,} likes",
            "inline": f"(YouTube: {item.get('channel', 'Unknown')}, {item.get('views', 0):,} views)"
        }

    def _format_generic_citation(self, item: Dict) -> Dict:
        """Format generic citation"""
        return {
            "type": "generic",
            "source": item.get("source", "Unknown Source"),
            "title": item.get("title", "Untitled")[:50] + "..." if len(item.get("title", "")) > 50 else item.get("title", ""),
            "date": datetime.now().isoformat()[:10],
            "url": item.get("url", ""),
            "inline": f"({item.get('source', 'Source')}, {datetime.now().isoformat()[:10]})"
        }

    def _generate_reference_list(self, citations: List[Dict]) -> List[str]:
        """Generate formatted reference list"""
        references = []

        # Remove duplicates based on URL
        seen_urls = set()
        unique_citations = []
        for citation in citations:
            if citation.get("url") and citation["url"] not in seen_urls:
                seen_urls.add(citation["url"])
                unique_citations.append(citation)
            elif not citation.get("url"):
                unique_citations.append(citation)

        # Format each unique citation
        for citation in unique_citations[:20]:  # Limit to 20 references
            if citation["type"] == "social_media":
                ref = f"{citation['author']} ({citation['date']}). '{citation['title']}'. r/{citation['subreddit']}, Reddit. Available at: {citation['url']}"
            elif citation["type"] == "news_media":
                ref = f"The Guardian ({citation['date']}). '{citation['title']}'. {citation['section']} Section. Available at: {citation['url']}"
            elif citation["type"] == "video_platform":
                ref = f"{citation['channel']} ({citation['date']}). '{citation['title']}'. YouTube. {citation['views']} views. Available at: {citation['url']}"
            else:
                ref = f"{citation['source']} ({citation['date']}). '{citation['title']}'. Available at: {citation['url']}"

            references.append(ref)

        return references

    def format_inline_citation_text(self, text: str, sources: Dict) -> str:
        """
        Add inline citations to text
        Returns text with proper citations inserted
        """
        # This would intelligently insert citations into the text
        # For now, we'll append them at the end

        if sources.get("inline_citations"):
            citations_text = " ".join([c["inline"] for c in sources["inline_citations"][:5]])
            return f"{text} {citations_text}"

        return text

    def generate_source_summary(self, sources: Dict) -> str:
        """Generate a summary of sources used"""
        summary = sources.get("source_summary", {})

        return f"""
Data Sources Summary:
- Total sources analyzed: {summary.get('total_sources', 0)}
- Social media posts: {summary.get('by_type', {}).get('social_media', 0)} (Reddit)
- News articles: {summary.get('by_type', {}).get('news_media', 0)} (The Guardian)
- Video content: {summary.get('by_type', {}).get('video_platform', 0)} (YouTube)
- Data freshness: Real-time API calls as of {datetime.now().strftime('%Y-%m-%d %H:%M GMT')}
"""

    def format_methodology_note(self) -> str:
        """Generate a methodology note for transparency"""
        return """
Methodology Note:
This analysis synthesizes real-time data from multiple UK sources:
- Reddit API: Trending posts from UK-focused subreddits (r/CasualUK, r/unitedkingdom, r/britishproblems, r/AskUK, r/London)
- YouTube Data API v3: Currently trending videos in the UK region
- Guardian Open Platform API: Latest UK news articles across multiple sections
- Analysis applies cross-platform pattern recognition, semantic network mapping, and temporal trend analysis
- Confidence scores based on data convergence across multiple sources
"""