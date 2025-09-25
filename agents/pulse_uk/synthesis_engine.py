"""
Advanced Synthesis Engine for PULSE UK Agent
Novel research and insight generation from cumulative data
"""

import json
import numpy as np
from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import re
from textblob import TextBlob
import hashlib


class UKCulturalSynthesizer:
    """Advanced synthesis engine for UK cultural intelligence"""

    def __init__(self):
        """Initialize the synthesis engine"""
        self.pattern_cache = {}
        self.trend_history = []
        self.semantic_clusters = defaultdict(list)

    def cross_platform_pattern_recognition(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect patterns across Reddit, YouTube, and Guardian data
        Returns cross-platform insights
        """
        patterns = {
            "timestamp": datetime.now().isoformat(),
            "emerging_themes": [],
            "cross_platform_trends": [],
            "platform_divergence": [],
            "viral_candidates": []
        }

        # Extract all text content for analysis
        all_content = self._extract_all_content(data)

        # Find common themes across platforms
        reddit_themes = self._extract_themes(data.get("reddit", {}))
        youtube_themes = self._extract_themes(data.get("youtube", {}))
        news_themes = self._extract_themes(data.get("guardian", {}))

        # Identify cross-platform patterns
        common_themes = set(reddit_themes) & set(youtube_themes) & set(news_themes)
        patterns["cross_platform_trends"] = list(common_themes)

        # Identify platform-specific trends
        reddit_only = set(reddit_themes) - set(youtube_themes) - set(news_themes)
        youtube_only = set(youtube_themes) - set(reddit_themes) - set(news_themes)
        news_only = set(news_themes) - set(reddit_themes) - set(youtube_themes)

        patterns["platform_divergence"] = {
            "reddit_unique": list(reddit_only)[:5],
            "youtube_unique": list(youtube_only)[:5],
            "guardian_unique": list(news_only)[:5]
        }

        # Detect viral candidates based on engagement velocity
        patterns["viral_candidates"] = self._detect_viral_patterns(data)

        # Identify emerging themes using frequency analysis
        patterns["emerging_themes"] = self._identify_emerging_themes(all_content)

        return patterns

    def temporal_trend_analysis(self, current_data: Dict, historical_data: List[Dict] = None) -> Dict[str, Any]:
        """
        Analyze trends over time to identify patterns and predict future movements
        """
        analysis = {
            "trend_lifecycle": {},
            "velocity_analysis": {},
            "predicted_peaks": [],
            "declining_trends": [],
            "sleeping_giants": []
        }

        if historical_data:
            self.trend_history.extend(historical_data)

        self.trend_history.append(current_data)

        # Analyze trend velocity (rate of change)
        if len(self.trend_history) >= 2:
            current_topics = self._extract_all_topics(current_data)
            previous_topics = self._extract_all_topics(self.trend_history[-2]) if len(self.trend_history) > 1 else {}

            for topic in current_topics:
                current_score = current_topics[topic]
                previous_score = previous_topics.get(topic, 0)

                velocity = (current_score - previous_score) / max(previous_score, 1)

                analysis["velocity_analysis"][topic] = {
                    "current_score": current_score,
                    "velocity": velocity,
                    "trend": "rising" if velocity > 0.1 else "falling" if velocity < -0.1 else "stable"
                }

                # Identify sleeping giants (low current score but high velocity)
                if current_score < 100 and velocity > 0.5:
                    analysis["sleeping_giants"].append({
                        "topic": topic,
                        "velocity": velocity,
                        "prediction": "Likely to trend within 24-48 hours"
                    })

        return analysis

    def semantic_network_mapping(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map relationships between topics, people, and concepts
        """
        network = {
            "nodes": [],
            "edges": [],
            "clusters": {},
            "bridge_concepts": [],
            "influencer_network": {}
        }

        # Extract entities and concepts
        entities = self._extract_entities(data)

        # Build semantic relationships
        for entity_type, entity_list in entities.items():
            for entity in entity_list:
                node_id = hashlib.md5(entity.encode()).hexdigest()[:8]
                network["nodes"].append({
                    "id": node_id,
                    "label": entity,
                    "type": entity_type,
                    "weight": entity_list[entity]
                })

        # Identify co-occurrences to create edges
        network["edges"] = self._build_semantic_edges(data)

        # Find bridge concepts that connect different communities
        network["bridge_concepts"] = self._identify_bridge_concepts(network["edges"])

        # Map influencer networks from Reddit and YouTube
        network["influencer_network"] = self._map_influencer_network(data)

        return network

    def generate_novel_insights(self, data: Dict[str, Any], patterns: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate truly novel insights and hypotheses from the data
        """
        insights = {
            "cultural_hypotheses": [],
            "trend_dna": {},
            "counter_trends": [],
            "white_spaces": [],
            "cultural_collisions": [],
            "memetic_velocity_index": {}
        }

        # Generate cultural hypotheses - predictions about what will trend next
        insights["cultural_hypotheses"] = self._generate_cultural_hypotheses(data, patterns)

        # Create Trend DNA - why certain content succeeds
        insights["trend_dna"] = self._analyze_trend_dna(data)

        # Identify counter-trend opportunities
        insights["counter_trends"] = self._identify_counter_trends(patterns)

        # Find white spaces - unaddressed opportunities
        insights["white_spaces"] = self._find_white_spaces(data, patterns)

        # Predict cultural collisions - when trends merge
        insights["cultural_collisions"] = self._predict_cultural_collisions(patterns)

        # Calculate memetic velocity index
        insights["memetic_velocity_index"] = self._calculate_memetic_velocity(data)

        return insights

    def regional_cultural_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze regional and demographic variations in UK culture
        """
        regional_analysis = {
            "london_vs_regional": {},
            "nation_specific": {
                "scotland": [],
                "wales": [],
                "northern_ireland": []
            },
            "north_south_divide": {},
            "generational_gaps": {},
            "class_indicators": []
        }

        # Analyze London-centric vs regional trends
        london_keywords = ["tube", "london", "westminster", "city", "zone"]
        regional_keywords = ["manchester", "birmingham", "liverpool", "newcastle", "glasgow"]

        london_score = self._calculate_keyword_presence(data, london_keywords)
        regional_score = self._calculate_keyword_presence(data, regional_keywords)

        regional_analysis["london_vs_regional"] = {
            "london_focus": london_score,
            "regional_focus": regional_score,
            "balance": "London-centric" if london_score > regional_score * 1.5 else "Regionally balanced"
        }

        # Detect nation-specific content
        scottish_indicators = ["scotland", "scottish", "edinburgh", "glasgow", "snp", "independence"]
        welsh_indicators = ["wales", "welsh", "cardiff", "rugby", "cymru"]
        ni_indicators = ["northern ireland", "belfast", "stormont", "ulster"]

        for indicators, nation in [(scottish_indicators, "scotland"),
                                   (welsh_indicators, "wales"),
                                   (ni_indicators, "northern_ireland")]:
            regional_analysis["nation_specific"][nation] = self._extract_nation_specific_trends(data, indicators)

        # Analyze north-south divide
        regional_analysis["north_south_divide"] = self._analyze_north_south_divide(data)

        # Detect generational gaps
        regional_analysis["generational_gaps"] = self._detect_generational_gaps(data)

        return regional_analysis

    def brand_opportunity_scoring(self, data: Dict[str, Any], insights: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate brand participation opportunities with risk assessment
        """
        opportunities = {
            "high_confidence": [],
            "experimental": [],
            "avoid": [],
            "cultural_fit_matrix": {},
            "timing_recommendations": {}
        }

        # Analyze each trend for brand safety and opportunity
        trends = self._extract_all_topics(data)

        for trend, score in trends.items():
            safety_score = self._calculate_brand_safety(trend, data)
            opportunity_score = self._calculate_opportunity_score(trend, score, insights)

            opportunity = {
                "trend": trend,
                "safety_score": safety_score,
                "opportunity_score": opportunity_score,
                "combined_score": (safety_score * 0.4 + opportunity_score * 0.6),
                "recommended_approach": self._generate_brand_approach(trend, safety_score, opportunity_score)
            }

            if opportunity["combined_score"] > 70:
                opportunities["high_confidence"].append(opportunity)
            elif opportunity["combined_score"] > 40:
                opportunities["experimental"].append(opportunity)
            else:
                opportunities["avoid"].append(opportunity)

        # Generate optimal timing recommendations
        opportunities["timing_recommendations"] = self._generate_timing_recommendations(data, insights)

        return opportunities

    # Helper methods
    def _extract_all_content(self, data: Dict) -> List[str]:
        """Extract all text content from the data"""
        content = []

        # Reddit content
        if "reddit" in data:
            for posts in data["reddit"].get("by_subreddit", {}).values():
                for post in posts:
                    if isinstance(post, dict):
                        content.append(post.get("title", ""))
                        if post.get("text"):
                            content.append(post["text"])

        # YouTube content
        if "youtube" in data:
            for video in data["youtube"].get("trending_videos", []):
                if isinstance(video, dict):
                    content.append(video.get("title", ""))
                    content.append(video.get("description", ""))

        # Guardian content
        if "guardian" in data:
            for articles in data["guardian"].get("by_category", {}).values():
                for article in articles:
                    if isinstance(article, dict):
                        content.append(article.get("title", ""))
                        content.append(article.get("description", ""))

        return content

    def _extract_themes(self, platform_data: Dict) -> List[str]:
        """Extract themes from platform data"""
        themes = []
        content = []

        if isinstance(platform_data, dict):
            # Handle different data structures
            if "by_subreddit" in platform_data:  # Reddit
                for posts in platform_data["by_subreddit"].values():
                    for post in posts:
                        if isinstance(post, dict):
                            content.append(post.get("title", ""))
            elif "trending_videos" in platform_data:  # YouTube
                for video in platform_data["trending_videos"]:
                    if isinstance(video, dict):
                        content.append(video.get("title", ""))
            elif "by_category" in platform_data:  # Guardian
                for articles in platform_data["by_category"].values():
                    for article in articles:
                        if isinstance(article, dict):
                            content.append(article.get("title", ""))

        # Extract themes using word frequency
        all_text = " ".join(content).lower()
        words = re.findall(r'\b[a-z]{4,}\b', all_text)

        # Filter out common words
        stop_words = {"that", "this", "with", "from", "have", "been", "what", "when", "where", "which", "their", "would", "could", "should"}
        words = [w for w in words if w not in stop_words]

        word_freq = Counter(words)
        themes = [word for word, _ in word_freq.most_common(10)]

        return themes

    def _detect_viral_patterns(self, data: Dict) -> List[Dict]:
        """Detect content with viral potential"""
        viral_candidates = []

        # Check Reddit posts
        if "reddit" in data:
            for posts in data["reddit"].get("by_subreddit", {}).values():
                for post in posts:
                    if isinstance(post, dict):
                        score = post.get("score", 0)
                        comments = post.get("comments", 0)

                        # High engagement ratio suggests viral potential
                        if comments > 0 and score / max(comments, 1) > 10:
                            viral_candidates.append({
                                "platform": "Reddit",
                                "title": post.get("title", ""),
                                "engagement_ratio": score / max(comments, 1),
                                "url": post.get("url", "")
                            })

        # Check YouTube videos
        if "youtube" in data:
            for video in data["youtube"].get("trending_videos", []):
                if isinstance(video, dict):
                    views = video.get("views", 0)
                    likes = video.get("likes", 0)

                    # High like ratio suggests viral potential
                    if views > 0 and likes / max(views, 1) > 0.05:
                        viral_candidates.append({
                            "platform": "YouTube",
                            "title": video.get("title", ""),
                            "engagement_ratio": likes / max(views, 1),
                            "views": views
                        })

        return sorted(viral_candidates, key=lambda x: x.get("engagement_ratio", 0), reverse=True)[:5]

    def _identify_emerging_themes(self, content: List[str]) -> List[Dict]:
        """Identify emerging themes from content"""
        all_text = " ".join(content).lower()

        # Extract phrases (2-3 word combinations)
        bigrams = re.findall(r'\b[a-z]+\s+[a-z]+\b', all_text)
        trigrams = re.findall(r'\b[a-z]+\s+[a-z]+\s+[a-z]+\b', all_text)

        phrase_freq = Counter(bigrams + trigrams)

        emerging = []
        for phrase, count in phrase_freq.most_common(10):
            if count > 2:  # Mentioned multiple times
                emerging.append({
                    "theme": phrase,
                    "frequency": count,
                    "classification": "emerging" if count < 10 else "established"
                })

        return emerging

    def _extract_all_topics(self, data: Dict) -> Dict[str, int]:
        """Extract all topics with their scores"""
        topics = defaultdict(int)

        content = self._extract_all_content(data)
        all_text = " ".join(content).lower()

        words = re.findall(r'\b[a-z]{4,}\b', all_text)
        word_freq = Counter(words)

        for word, freq in word_freq.most_common(50):
            topics[word] = freq

        return dict(topics)

    def _extract_entities(self, data: Dict) -> Dict[str, Dict[str, int]]:
        """Extract entities (people, places, organizations) from data"""
        entities = {
            "people": defaultdict(int),
            "places": defaultdict(int),
            "organizations": defaultdict(int)
        }

        content = self._extract_all_content(data)

        for text in content:
            # Simple entity extraction using capitalization patterns
            capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)

            for entity in capitalized:
                if entity.lower() in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
                    continue

                # Classify entity type (simplified)
                if entity in ["London", "Manchester", "Scotland", "Wales", "England", "UK", "Birmingham", "Glasgow"]:
                    entities["places"][entity] += 1
                elif entity in ["BBC", "NHS", "Guardian", "Reddit", "YouTube", "Twitter"]:
                    entities["organizations"][entity] += 1
                else:
                    entities["people"][entity] += 1

        return {k: dict(v) for k, v in entities.items()}

    def _build_semantic_edges(self, data: Dict) -> List[Dict]:
        """Build edges between semantically related concepts"""
        edges = []
        # Simplified edge building - would use more sophisticated NLP in production
        return edges

    def _identify_bridge_concepts(self, edges: List[Dict]) -> List[str]:
        """Identify concepts that bridge different communities"""
        # Simplified - would use graph algorithms in production
        return ["technology", "culture", "politics", "entertainment", "sports"]

    def _map_influencer_network(self, data: Dict) -> Dict:
        """Map influencer networks from social data"""
        network = {
            "top_reddit_users": [],
            "top_youtube_channels": []
        }

        # Extract Reddit users
        if "reddit" in data:
            authors = defaultdict(int)
            for posts in data["reddit"].get("by_subreddit", {}).values():
                for post in posts:
                    if isinstance(post, dict) and post.get("author"):
                        authors[post["author"]] += post.get("score", 0)

            network["top_reddit_users"] = sorted(authors.items(), key=lambda x: x[1], reverse=True)[:5]

        # Extract YouTube channels
        if "youtube" in data:
            channels = defaultdict(int)
            for video in data["youtube"].get("trending_videos", []):
                if isinstance(video, dict) and video.get("channel"):
                    channels[video["channel"]] += video.get("views", 0)

            network["top_youtube_channels"] = sorted(channels.items(), key=lambda x: x[1], reverse=True)[:5]

        return network

    def _generate_cultural_hypotheses(self, data: Dict, patterns: Dict) -> List[Dict]:
        """Generate hypotheses about future cultural trends"""
        hypotheses = []

        # Based on cross-platform trends
        for trend in patterns.get("cross_platform_trends", [])[:3]:
            hypotheses.append({
                "hypothesis": f"'{trend}' will become mainstream UK discourse within 7 days",
                "confidence": 75,
                "reasoning": "Strong presence across all platforms",
                "recommended_action": f"Prepare content around {trend} theme"
            })

        # Based on viral candidates
        for candidate in patterns.get("viral_candidates", [])[:2]:
            hypotheses.append({
                "hypothesis": f"Content similar to '{candidate.get('title', '')[:50]}' will proliferate",
                "confidence": 60,
                "reasoning": f"High engagement ratio of {candidate.get('engagement_ratio', 0):.2f}",
                "recommended_action": "Monitor and prepare derivative content"
            })

        return hypotheses

    def _analyze_trend_dna(self, data: Dict) -> Dict:
        """Analyze what makes trends successful"""
        dna = {
            "successful_patterns": [],
            "engagement_drivers": [],
            "format_preferences": {}
        }

        # Analyze high-performing content
        high_performers = []

        if "reddit" in data:
            for posts in data["reddit"].get("by_subreddit", {}).values():
                for post in posts:
                    if isinstance(post, dict) and post.get("score", 0) > 1000:
                        high_performers.append({
                            "platform": "Reddit",
                            "title": post.get("title", ""),
                            "score": post.get("score", 0)
                        })

        # Extract patterns from high performers
        if high_performers:
            # Check for question formats
            questions = [p for p in high_performers if "?" in p["title"]]
            if len(questions) / len(high_performers) > 0.3:
                dna["successful_patterns"].append("Question-based titles drive engagement")

            # Check for personal stories
            personal = [p for p in high_performers if any(word in p["title"].lower() for word in ["i", "my", "me"])]
            if len(personal) / len(high_performers) > 0.4:
                dna["successful_patterns"].append("Personal narratives resonate strongly")

        return dna

    def _identify_counter_trends(self, patterns: Dict) -> List[Dict]:
        """Identify opportunities to go against prevailing trends"""
        counter_trends = []

        # If everyone is serious, humor opportunity exists
        if "politics" in patterns.get("cross_platform_trends", []):
            counter_trends.append({
                "opportunity": "Light-hearted content",
                "reasoning": "Heavy news cycle creates demand for escapism",
                "confidence": 70
            })

        # If tech dominates, nature/traditional content opportunity
        if "technology" in patterns.get("cross_platform_trends", []):
            counter_trends.append({
                "opportunity": "Traditional/nostalgic content",
                "reasoning": "Digital fatigue creates nostalgia demand",
                "confidence": 65
            })

        return counter_trends

    def _find_white_spaces(self, data: Dict, patterns: Dict) -> List[Dict]:
        """Find unaddressed content opportunities"""
        white_spaces = []

        # Check for underserved demographics
        content = self._extract_all_content(data)
        all_text = " ".join(content).lower()

        # Check for age group mentions
        if "pensioner" not in all_text and "elderly" not in all_text:
            white_spaces.append({
                "opportunity": "Senior-focused content",
                "gap": "Minimal content addressing 65+ demographic",
                "potential": "High - underserved large demographic"
            })

        # Check for regional gaps
        if "wales" not in all_text and "welsh" not in all_text:
            white_spaces.append({
                "opportunity": "Welsh cultural content",
                "gap": "Wales underrepresented in trending content",
                "potential": "Medium - engaged but smaller audience"
            })

        return white_spaces

    def _predict_cultural_collisions(self, patterns: Dict) -> List[Dict]:
        """Predict when different trends will merge"""
        collisions = []

        trends = patterns.get("cross_platform_trends", [])

        # Simple collision prediction based on co-occurrence potential
        if len(trends) >= 2:
            collisions.append({
                "collision": f"{trends[0]} meets {trends[1]}",
                "prediction": "These themes will merge in content within 48 hours",
                "opportunity": f"Create content combining {trends[0]} and {trends[1]} themes"
            })

        return collisions

    def _calculate_memetic_velocity(self, data: Dict) -> Dict[str, float]:
        """Calculate how fast memes/trends are spreading"""
        velocity_index = {}

        # Calculate based on engagement metrics
        if "reddit" in data:
            reddit_engagement = 0
            post_count = 0

            for posts in data["reddit"].get("by_subreddit", {}).values():
                for post in posts:
                    if isinstance(post, dict):
                        reddit_engagement += post.get("score", 0) + post.get("comments", 0)
                        post_count += 1

            if post_count > 0:
                velocity_index["reddit_velocity"] = reddit_engagement / post_count

        if "youtube" in data:
            youtube_engagement = 0
            video_count = 0

            for video in data["youtube"].get("trending_videos", []):
                if isinstance(video, dict):
                    youtube_engagement += video.get("views", 0) + video.get("likes", 0)
                    video_count += 1

            if video_count > 0:
                velocity_index["youtube_velocity"] = youtube_engagement / video_count

        return velocity_index

    def _calculate_keyword_presence(self, data: Dict, keywords: List[str]) -> int:
        """Calculate presence of keywords in data"""
        score = 0
        content = self._extract_all_content(data)
        all_text = " ".join(content).lower()

        for keyword in keywords:
            score += all_text.count(keyword.lower())

        return score

    def _extract_nation_specific_trends(self, data: Dict, indicators: List[str]) -> List[str]:
        """Extract nation-specific trends"""
        trends = []
        content = self._extract_all_content(data)

        for text in content:
            text_lower = text.lower()
            for indicator in indicators:
                if indicator.lower() in text_lower:
                    trends.append(text[:100])
                    break

        return trends[:5]

    def _analyze_north_south_divide(self, data: Dict) -> Dict:
        """Analyze north-south divide in content"""
        north_keywords = ["manchester", "liverpool", "leeds", "newcastle", "sheffield", "yorkshire"]
        south_keywords = ["london", "brighton", "oxford", "cambridge", "kent", "surrey"]

        north_score = self._calculate_keyword_presence(data, north_keywords)
        south_score = self._calculate_keyword_presence(data, south_keywords)

        return {
            "north_representation": north_score,
            "south_representation": south_score,
            "balance": "Balanced" if abs(north_score - south_score) < 10 else "South-heavy" if south_score > north_score else "North-heavy"
        }

    def _detect_generational_gaps(self, data: Dict) -> Dict:
        """Detect generational differences in content"""
        gen_z_keywords = ["tiktok", "vibe", "aesthetic", "stan", "sus", "bussin", "rizz"]
        millennial_keywords = ["adulting", "netflix", "brunch", "90s", "nostalgia"]
        gen_x_keywords = ["mortgage", "pension", "school", "career", "family"]

        content = self._extract_all_content(data)
        all_text = " ".join(content).lower()

        return {
            "gen_z_score": sum(1 for k in gen_z_keywords if k in all_text),
            "millennial_score": sum(1 for k in millennial_keywords if k in all_text),
            "gen_x_score": sum(1 for k in gen_x_keywords if k in all_text)
        }

    def _calculate_brand_safety(self, trend: str, data: Dict) -> float:
        """Calculate brand safety score for a trend"""
        # Simplified sentiment analysis
        try:
            blob = TextBlob(trend)
            sentiment = blob.sentiment.polarity

            # Convert sentiment to safety score (0-100)
            safety_score = 50 + (sentiment * 50)

            # Check for controversial keywords
            controversial = ["politics", "brexit", "covid", "scandal", "crisis", "protest"]
            if any(word in trend.lower() for word in controversial):
                safety_score -= 20

            return max(0, min(100, safety_score))
        except:
            return 50  # Default neutral score

    def _calculate_opportunity_score(self, trend: str, score: int, insights: Dict) -> float:
        """Calculate opportunity score for a trend"""
        opportunity = 50  # Base score

        # Higher engagement = higher opportunity
        if score > 100:
            opportunity += 20
        if score > 500:
            opportunity += 10

        # Emerging themes = higher opportunity
        emerging_themes = insights.get("emerging_themes", [])
        if any(trend in theme.get("theme", "") for theme in emerging_themes):
            opportunity += 15

        # White space = highest opportunity
        white_spaces = insights.get("white_spaces", [])
        if any(trend in space.get("opportunity", "") for space in white_spaces):
            opportunity += 25

        return min(100, opportunity)

    def _generate_brand_approach(self, trend: str, safety_score: float, opportunity_score: float) -> str:
        """Generate recommended brand approach for a trend"""
        if safety_score > 70 and opportunity_score > 70:
            return "Aggressive participation - high confidence opportunity"
        elif safety_score > 50 and opportunity_score > 50:
            return "Cautious participation - test with small campaign"
        elif opportunity_score > 70 and safety_score < 50:
            return "High risk/reward - only for bold brands"
        else:
            return "Monitor only - not recommended for brand participation"

    def _generate_timing_recommendations(self, data: Dict, insights: Dict) -> Dict:
        """Generate optimal timing for brand participation"""
        current_time = datetime.now()

        recommendations = {
            "immediate": [],
            "next_24h": [],
            "next_week": [],
            "watch_list": []
        }

        # Check memetic velocity
        velocity = insights.get("memetic_velocity_index", {})

        if velocity.get("reddit_velocity", 0) > 1000:
            recommendations["immediate"].append("High Reddit velocity - engage within 2 hours")

        if velocity.get("youtube_velocity", 0) > 10000:
            recommendations["next_24h"].append("YouTube trend building - prepare content for tomorrow")

        # Check for sleeping giants
        for giant in insights.get("sleeping_giants", []):
            recommendations["next_week"].append(f"Prepare for '{giant['topic']}' - predicted to peak soon")

        return recommendations